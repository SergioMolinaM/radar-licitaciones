"""Fuente: Compra Ágil (ChileCompra) — API v2.

Verificado contra la "Documentación API Compra Ágil" oficial de ChileCompra
(publicada mayo 2026, enlazada desde https://www.chilecompra.cl/api/):
  http://www.chilecompra.cl/wp-content/uploads/2026/05/Documentacion_API_Compra_Agil.pdf

Diferencias con la API de Licitaciones (importantes):
  - URL base distinta: api2.mercadopublico.cl (no api.mercadopublico.cl).  [§1]
  - Autenticación por HEADER `ticket`, no por query param. Sin el header la
    API responde 401; ticket inválido/bloqueado responde 403.              [§3, §7]
  - Respuesta anidada: {"success":"OK","payload":{"items":[],"paginacion":{}}}. [§6]
  - El listado NO trae `descripcion` (solo el endpoint de detalle la tiene).
    El match de keywords se hace sobre `nombre`, igual que en licitaciones.  [§6.1 vs §6.3]

Estrategia del radar (desde el 30-oct-2026, fetch_compra_agil): (0) el listado
completo sin q desde la última barrida completa, filtrado por título con todas
las keywords (_barrer_listado: 62 páginas de 1 día respondieron en la sonda del
30-oct); (1) búsqueda por palabra clave en el servidor (`q`), que también mira
la descripción, con los términos diarios y el resto en rotación. Del 14 al
29-oct solo existía (1), porque el listado caía en 504 y las frases que daban
504 dejaban temas ciegos. fetch_raw_publicadas es la versión antigua del
barrido, que sigue usando la auditoría. La deduplicación por state.json evita
re-notificar día tras día.

Nota de cuota: el límite es por ticket y por día calendario, y se devuelve 429
al agotarlo (§4). Con estado=publicada + ventana de 3 días el universo ronda las
~800 Compras Ágiles, es decir ~16 páginas de 50. MAX_PAGINAS es el tope de
seguridad. Ante 429 se detiene y retorna lo acumulado (no revienta la corrida).
"""

import time
import logging
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import requests

from ..config import (
    COMPRA_AGIL_API_URL,
    COMPRA_AGIL_ESTADOS,
    COMPRA_AGIL_DIAS_MAX_ROTATIVO,
    COMPRA_AGIL_DIAS_VENTANA,
    COMPRA_AGIL_EXCLUSIONES_OMITIDAS,
    COMPRA_AGIL_TERMINOS_DIARIOS,
    COMPRA_AGIL_WEB_URL_TEMPLATE,
    FUENTE_PALABRA_SUELTA,
    KEYWORDS_INCLUDE,
)
from ..filters import excluido, keywords_incluidas
from ._tickets import tickets

logger = logging.getLogger(__name__)
try:
    CHILE_TZ = ZoneInfo("America/Santiago")
except ZoneInfoNotFoundError:  # Windows sin tzdata; el runner de GitHub (Ubuntu) la trae
    CHILE_TZ = timezone(timedelta(hours=-3))

TIMEOUT = 60
TAMANO_PAGINA = 50          # máximo permitido por la API (default 15, mínimo 10)  [guía §5.1 Grupo 6]
MAX_PAGINAS = 80            # tope de seguridad del barrido completo (solo auditoría)
MAX_PAGINAS_TERMINO = 5     # una búsqueda q trae 1-19 resultados (medido 14-oct); 5 páginas = 250
REINTENTOS_ESPERA_S = (20, 60)  # barrido completo: esperas entre intentos ante 5xx/red
PRESUPUESTO_BARRIDO_S = 15 * 60  # tope del barrido completo (auditoría)
PRESUPUESTO_BUSQUEDA_S = 15 * 60  # tope de la búsqueda q, después del listado (18 min); el job tiene timeout-minutes: 50
RESERVA_POR_REINTENTO_S = 30  # un 504 tarda ~29 s; se aparta este tiempo por diario fallido
# Listado completo sin q (30-oct-2026, sonda run 41081425045): 62 páginas de 1 día
# respondieron todas, 0,9-7,3 s cada una, sin 429, con 5 s entre solicitudes. Esa
# tarde pasaron 88 solicitudes espaciadas sin 429; en la mañana, 5 seguidas lo
# dispararon («límite de tasa»): se espacia toda solicitud. No verificado que la
# pausa sea la causa.
PAUSA_ENTRE_SOLICITUDES_S = 4
PRESUPUESTO_LISTADO_S = 18 * 60
LISTADO_TRASLAPE = timedelta(hours=2)   # la paginación se corre si entran publicaciones mientras se recorre
LISTADO_DIAS_MAX = 4                    # más atrás no cabe en el presupuesto (~3.000 publicadas por día)
CLAVE_LISTADO = "__listado__"           # en state["ca_ultima"]: hasta dónde se leyó el listado sin hueco
MAX_PAGINAS_LISTADO = 300               # tope de seguridad: un recorte deja el barrido incompleto
# El listado viene de lo más nuevo a lo más viejo, con o sin ordenar_por (sonda --orden,
# run 41092789158). Un barrido abierto que no termina deja sin leer lo más antiguo y la
# marca no puede avanzar. Por eso se recorre en tramos cerrados (publicado_desde +
# publicado_hasta, guía §5.1 Grupo 2) del más antiguo al más nuevo: cada tramo leído
# entero mueve la marca a su fin, y lo que entra mientras se recorre no desplaza las
# páginas de un tramo ya cerrado.
LISTADO_TRAMO = timedelta(hours=6)


def _get_ticket() -> str | None:
    """Ticket principal (auditoría). El radar diario usa tickets() con respaldo."""
    disponibles = tickets()
    if not disponibles:
        logger.error("MERCADO_PUBLICO_TOKEN no configurado (Compra Ágil)")
        return None
    return disponibles[0][1]


def _get_con_reintentos(ticket: str, params: dict, numero_pagina: int) -> requests.Response | None:
    """GET con reintentos ante 5xx y errores de red.

    Desde mediados de agosto 2026 la API responde 504 (Gateway Timeout, ~29 s)
    en casi todas las corridas, casi siempre en la página 1; el 18-sep llegó a
    la 23 antes de caer. Es intermitente, así que se reintenta con espera.
    """
    for intento, espera in enumerate((*REINTENTOS_ESPERA_S, None), start=1):
        try:
            resp = requests.get(
                COMPRA_AGIL_API_URL,
                headers={"ticket": ticket},
                params=params,
                timeout=TIMEOUT,
            )
            if resp.status_code < 500:
                return resp
            motivo = f"HTTP {resp.status_code}"
        except requests.RequestException as e:
            resp, motivo = None, f"error de red — {e}"

        if espera is None:
            logger.error(f"Compra Ágil: {motivo} (pág {numero_pagina}), sin más reintentos")
            return resp
        logger.warning(
            f"Compra Ágil: {motivo} (pág {numero_pagina}, intento {intento}); reintento en {espera} s"
        )
        time.sleep(espera)
    return None


def _fetch_pagina(ticket: str, publicado_desde: str, numero_pagina: int) -> dict | None:
    """Consulta una página del listado. Retorna el payload o None si falla."""
    params = {
        "estado": COMPRA_AGIL_ESTADOS,
        "publicado_desde": publicado_desde,
        "ordenar_por": "FechaPublicacion",  # valor válido según guía §5.1 Grupo 7
        "tamano_pagina": TAMANO_PAGINA,
        "numero_pagina": numero_pagina,
    }
    resp = _get_con_reintentos(ticket, params, numero_pagina)
    if resp is None:
        return None

    if resp.status_code == 429:
        logger.warning("Compra Ágil: límite de la API (429). Se detiene el barrido.")
        return None
    if resp.status_code in (401, 403):
        logger.error(
            f"Compra Ágil: ticket rechazado ({resp.status_code}). "
            "Verificar que MERCADO_PUBLICO_TOKEN habilite la API v2 (api2.mercadopublico.cl)."
        )
        return None

    try:
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.error(f"Compra Ágil: respuesta inválida (pág {numero_pagina}) — {e}")
        return None

    if data.get("success") != "OK":
        logger.error(f"Compra Ágil: success != OK — {data.get('errors')}")
        return None

    return data.get("payload") or {}


def fetch_raw_publicadas(dias_ventana: int = COMPRA_AGIL_DIAS_VENTANA) -> tuple[list[dict], bool]:
    """Recorre el listado paginado y retorna (items crudos sin filtrar, completo).

    Uso: la auditoría de keywords (src/audit_compra_agil.py); el radar diario
    ya no barre el listado (ver fetch_compra_agil). Retorna ([], False) si el ticket falla o la API
    responde mal. Ante 429 o una página caída retorna lo acumulado con
    completo=False: un barrido cortado en la pág. 23 de 28 (18-sep) no es éxito.
    """
    ticket = _get_ticket()
    if not ticket:
        return [], False

    desde = datetime.now(timezone.utc) - timedelta(days=dias_ventana)
    publicado_desde = desde.strftime("%Y-%m-%dT%H:%M:%SZ")

    items: list[dict] = []
    numero_pagina = 1
    completo = False

    inicio = time.monotonic()
    while numero_pagina <= MAX_PAGINAS:
        if time.monotonic() - inicio > PRESUPUESTO_BARRIDO_S:
            logger.error(f"Compra Ágil: se agotó el presupuesto de {PRESUPUESTO_BARRIDO_S} s en la pág {numero_pagina}")
            break
        payload = _fetch_pagina(ticket, publicado_desde, numero_pagina)
        if payload is None:
            break

        items.extend(payload.get("items") or [])

        paginacion = payload.get("paginacion") or {}
        total_paginas = paginacion.get("total_paginas", numero_pagina)
        if numero_pagina >= total_paginas:
            completo = True
            break
        numero_pagina += 1
    else:
        logger.warning(
            f"Compra Ágil: se alcanzó MAX_PAGINAS ({MAX_PAGINAS}). "
            "El barrido quedó truncado — revisar si el universo creció."
        )

    if not completo:
        logger.error(f"Compra Ágil: barrido incompleto ({len(items)} items antes de cortar)")
    return items, completo


def fetch_detalle(codigo: str) -> dict | None:
    """Detalle de una Compra Ágil (GET /v2/compra-agil/{codigo}).

    Es el ÚNICO lugar donde la API entrega `descripcion`: el listado no la trae
    (guía §6.1 vs §6.3). Lo usa la auditoría; el radar diario NO lo llama, para
    no gastar una request por Compra Ágil en cada corrida.
    """
    ticket = _get_ticket()
    if not ticket:
        return None

    try:
        resp = requests.get(
            f"{COMPRA_AGIL_API_URL}/{codigo}",
            headers={"ticket": ticket},
            timeout=TIMEOUT,
        )
        if resp.status_code == 429:
            logger.warning(f"Compra Ágil: límite de la API (429) al pedir detalle de {codigo}")
            return None
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, ValueError) as e:
        logger.error(f"Compra Ágil: detalle {codigo} falló — {e}")
        return None

    if data.get("success") != "OK":
        logger.error(f"Compra Ágil: detalle {codigo} success != OK — {data.get('errors')}")
        return None

    return data.get("payload") or None


class _CuotaAgotada(Exception):
    pass


class _TicketRechazado(Exception):
    pass


# Solicitudes hechas por fetch_compra_agil en esta corrida, para saber con
# cuántas llega el 429: el 19 y el 22-oct llegó tras 15 a 17 y el 20 y 21-oct
# 45 a 51 pasaron sin él (estimado de los logs). El 27-oct llegó tras 3, un día
# después de 54 sin él, con el mensaje «Se ha superado el límite de tasa de
# solicitudes»: no calza con una cuota diaria fija.
_solicitudes = 0
_ultima_solicitud = 0.0


def _get_espaciado(ticket: str, params: dict) -> requests.Response:
    """GET a la API con PAUSA_ENTRE_SOLICITUDES_S desde la solicitud anterior."""
    global _solicitudes, _ultima_solicitud
    espera = PAUSA_ENTRE_SOLICITUDES_S - (time.monotonic() - _ultima_solicitud)
    if espera > 0:
        time.sleep(espera)
    _solicitudes += 1
    try:
        return requests.get(COMPRA_AGIL_API_URL, headers={"ticket": ticket}, params=params, timeout=TIMEOUT)
    finally:
        _ultima_solicitud = time.monotonic()


def _detalle_429(resp: requests.Response) -> str:
    """Retry-After y mensaje del 429 (guía §4.2 y §7), para medir el límite."""
    try:
        errores = (resp.json() or {}).get("errors") or []
        mensaje = errores[0].get("mensaje") if errores else None
    except (ValueError, AttributeError):
        mensaje = None
    return (f"límite de la API (429) tras {_solicitudes} solicitudes; "
            f"Retry-After={resp.headers.get('Retry-After')!r}; mensaje={mensaje!r}")


def _buscar_termino(ticket: str, termino: str, publicado_desde: str) -> tuple[list[dict], bool] | None:
    """Un intento de búsqueda `q` (guía §5.1 Grupo 5), todas sus páginas.

    Retorna (items, truncado) o None si alguna página falla (504, 5xx, red,
    JSON o forma inesperada). Lanza _CuotaAgotada ante 429 y _TicketRechazado
    ante 401/403.
    """
    items: list[dict] = []
    for numero_pagina in range(1, MAX_PAGINAS_TERMINO + 1):
        params = {
            "q": termino,
            "estado": COMPRA_AGIL_ESTADOS,
            "publicado_desde": publicado_desde,
            "tamano_pagina": TAMANO_PAGINA,
            "numero_pagina": numero_pagina,
        }
        try:
            resp = _get_espaciado(ticket, params)
        except requests.RequestException as e:
            logger.warning(f"Compra Ágil q={termino!r}: error de red — {type(e).__name__}")
            return None
        if resp.status_code == 429:
            raise _CuotaAgotada(_detalle_429(resp))
        if resp.status_code in (401, 403):
            raise _TicketRechazado(f"ticket rechazado ({resp.status_code})")
        if resp.status_code != 200:
            logger.warning(f"Compra Ágil q={termino!r}: HTTP {resp.status_code} (pág {numero_pagina})")
            return None
        try:
            data = resp.json()
        except ValueError:
            data = None
        if not isinstance(data, dict) or data.get("success") != "OK" or not isinstance(data.get("payload") or {}, dict):
            logger.warning(f"Compra Ágil q={termino!r}: respuesta inesperada (pág {numero_pagina})")
            return None
        payload = data.get("payload") or {}
        pagina = payload.get("items") or []
        if not isinstance(pagina, list):
            logger.warning(f"Compra Ágil q={termino!r}: items no es lista (pág {numero_pagina})")
            return None
        items.extend(i for i in pagina if isinstance(i, dict))
        total = (payload.get("paginacion") or {}).get("total_paginas")
        if not isinstance(total, int) or numero_pagina >= total:
            return items, False
    logger.warning(f"Compra Ágil q={termino!r}: más de {MAX_PAGINAS_TERMINO} páginas, se corta")
    return items, True


def _barrer_listado(disponibles: list, publicado_desde: str, limite: float, publicado_hasta: str | None = None) -> dict:
    """Todas las páginas del listado sin q desde `publicado_desde`.

    `disponibles` es la lista de tickets: ante 401/403 se pasa al siguiente y se
    repite la misma página. Nunca lanza. Retorna un dict con items, leidas, total
    (None si no se supo), prefijo (páginas 1..k leídas sin hueco) y corte (motivo
    si se detuvo antes del final: 429, tickets, presupuesto, total ilegible). Una
    página que falla dos veces se salta y se siguen las demás.
    """
    r = {"items": [], "leidas": 0, "total": None, "prefijo": 0, "corte": ""}
    pagina, sin_hueco = 1, True
    while r["total"] is None or pagina <= r["total"]:
        if time.monotonic() > limite:
            r["corte"] = f"se agotó el presupuesto de {PRESUPUESTO_LISTADO_S // 60} min en la pág {pagina}"
            break
        params = {"estado": COMPRA_AGIL_ESTADOS, "publicado_desde": publicado_desde,
                  "tamano_pagina": TAMANO_PAGINA, "numero_pagina": pagina}
        if publicado_hasta:
            params["publicado_hasta"] = publicado_hasta
        payload, intentos = None, 0
        while intentos < 2 and not r["corte"]:
            intentos += 1
            try:
                resp = _get_espaciado(disponibles[0][1], params)
            except requests.RequestException as e:
                logger.warning(f"Compra Ágil listado: error de red (pág {pagina}) — {type(e).__name__}")
                continue
            if resp.status_code == 429:
                r["corte"] = _detalle_429(resp)
                break
            if resp.status_code in (401, 403):
                nombre = disponibles.pop(0)[0]
                if not disponibles:
                    r["corte"] = f"ticket rechazado ({resp.status_code}), sin otro ticket"
                    break
                logger.error(f"Compra Ágil: ticket rechazado ({resp.status_code}) con el ticket {nombre}; "
                             f"se pasa al {disponibles[0][0]}")
                intentos -= 1  # el cambio de ticket no gasta intento
                continue
            if resp.status_code != 200:
                logger.warning(f"Compra Ágil listado: HTTP {resp.status_code} (pág {pagina})")
                continue
            try:
                data = resp.json()
            except ValueError:
                data = None
            p = data.get("payload") if isinstance(data, dict) and data.get("success") == "OK" else None
            if isinstance(p, dict) and isinstance(p.get("items") or [], list) \
                    and isinstance(p.get("paginacion") or {}, dict):
                payload = p
                break
            logger.warning(f"Compra Ágil listado: respuesta inesperada (pág {pagina})")
        if r["corte"]:
            break
        if payload is None:
            sin_hueco = False
            if r["total"] is None:
                r["corte"] = "no respondió la primera página"
                break
        else:
            r["leidas"] += 1
            r["items"].extend(i for i in payload.get("items") or [] if isinstance(i, dict))
            if sin_hueco:
                r["prefijo"] = pagina
            if r["total"] is None:
                t = (payload.get("paginacion") or {}).get("total_paginas")
                if t == 0 and not payload.get("items"):
                    r["total"] = r["prefijo"] = 1  # tramo vacío: leído completo
                    break
                if not isinstance(t, int) or t < 1:
                    r["corte"] = f"total de páginas ilegible ({t!r})"
                    break
                r["total"] = min(t, MAX_PAGINAS_LISTADO)
                if t > MAX_PAGINAS_LISTADO:
                    logger.error(f"Compra Ágil listado: {t} páginas, se leen {MAX_PAGINAS_LISTADO}")
                    r["recorte"] = f"{t} páginas, se leyeron las primeras {MAX_PAGINAS_LISTADO}"
        pagina += 1
    if r.get("recorte") and not r["corte"]:
        r["corte"] = r["recorte"]
    return r


def _parse_iso(s) -> datetime | None:
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return None


def _item_de_listado(item: dict) -> dict | None:
    """Item del listado completo: entra solo si el nombre trae una keyword (el
    listado no trae descripción). Exclusiones como en la búsqueda q."""
    nombre = item.get("nombre", "") or ""
    if not item.get("codigo") or excluido(nombre, omitir=COMPRA_AGIL_EXCLUSIONES_OMITIDAS):
        return None
    en_titulo = keywords_incluidas(nombre)
    if not en_titulo:
        return None
    d = _item_to_dict_sin_filtro(item)
    d["keywords_match"] = en_titulo
    return d


def _item_de_busqueda(item: dict, termino: str) -> dict | None:
    """Item ya filtrado por `q` en el servidor, al esquema interno.

    `q` calza cualquiera de las palabras del término, no la frase (corrida del
    15-oct: «economía circular» trajo «aguja circular»), y el listado no trae
    la descripción. Si el nombre no contiene ninguna keyword de inclusión, el
    ítem va a la sección aparte FUENTE_PALABRA_SUELTA: ahí salieron 10 de las
    19 candidatas del triage del 15-oct, así que no se descarta. Las
    exclusiones se aplican sobre el nombre, salvo COMPRA_AGIL_EXCLUSIONES_OMITIDAS.
    """
    nombre = item.get("nombre", "") or ""
    codigo = item.get("codigo")
    if not codigo or excluido(nombre, omitir=COMPRA_AGIL_EXCLUSIONES_OMITIDAS):
        return None
    d = _item_to_dict_sin_filtro(item)
    en_titulo = keywords_incluidas(nombre)
    if en_titulo:
        d["keywords_match"] = en_titulo
    else:
        d["fuente"] = FUENTE_PALABRA_SUELTA
        d["keywords_match"] = [f"búsqueda «{termino}»"]
    return d


def _item_to_dict_sin_filtro(item: dict) -> dict:
    codigo = item.get("codigo")
    fechas = item.get("fechas") or {}
    montos = item.get("montos") or {}
    institucion = item.get("institucion") or {}
    return {
        "fuente": "Compra Ágil",
        "id": f"CA::{codigo}",
        "codigo": codigo,
        "titulo": item.get("nombre", "") or "",
        "estado": (item.get("estado") or {}).get("glosa", "Publicada"),
        "fecha_cierre": fechas.get("fecha_cierre", ""),
        "link": COMPRA_AGIL_WEB_URL_TEMPLATE.format(codigo=codigo),
        "keywords_match": [],
        "organismo": institucion.get("organismo_comprador", ""),
        "monto_clp": montos.get("monto_disponible_clp"),
    }


def terminos_rotativos() -> list[str]:
    """KEYWORDS_INCLUDE menos los diarios, en el orden de config.py."""
    diarios = set(COMPRA_AGIL_TERMINOS_DIARIOS)
    return [kw for kw in KEYWORDS_INCLUDE if kw not in diarios]


def _iso(dt: datetime) -> str:
    """UTC, para state.json y el log."""
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _api_fecha(dt: datetime) -> str:
    """Fecha para publicado_desde/hasta: la API la lee como hora de Chile aunque lleve
    «Z». Sonda --hasta (run 41101204459, 30-oct): se pidió 13:44:48Z → 14:44:48Z y
    volvieron fecha_publicacion 13:45 a 14:40, que es hora de Chile (la sonda corrió
    a las 17:44 UTC). Con UTC el filtro quedaba 3 h corrido."""
    return dt.astimezone(CHILE_TZ).strftime("%Y-%m-%dT%H:%M:%SZ")


def _desde_rotativo(ultima: str | None, ahora: datetime) -> str:
    """Desde la última búsqueda exitosa del término (con 1 h de traslape), con
    piso en la ventana diaria y techo en COMPRA_AGIL_DIAS_MAX_ROTATIVO días.
    Devuelve la fecha para la API (_api_fecha)."""
    minimo = ahora - timedelta(days=COMPRA_AGIL_DIAS_MAX_ROTATIVO)
    por_defecto = ahora - timedelta(days=COMPRA_AGIL_DIAS_VENTANA)
    try:
        dt = datetime.strptime(ultima, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc) - timedelta(hours=1)
    except (TypeError, ValueError):
        return _api_fecha(por_defecto)
    return _api_fecha(max(minimo, min(dt, por_defecto)))


def fetch_compra_agil(cursor=0, ultima: dict | None = None,
                      presupuesto_s: float = PRESUPUESTO_BUSQUEDA_S) -> tuple[list[dict], dict]:
    """Busca en el servidor cada término (`q`) entre las Compras Ágiles publicadas.

    Orden: (1) una pasada por COMPRA_AGIL_TERMINOS_DIARIOS; (2) si respondió al
    menos un diario, los rotativos desde `cursor`, dejando
    RESERVA_POR_REINTENTO_S por diario fallido más un TIMEOUT; (3) un segundo
    intento de los diarios fallidos al final. Si en (1) no respondió ninguno,
    el segundo intento va antes de (2), porque decide si hay rotativos. El reintento inmediato del 15-oct recuperó 1 de 9
    y costó ~4 min de rotación; al final, la API tuvo más tiempo para
    recuperarse. Cada término, diario
    o rotativo, busca desde su última búsqueda exitosa y no truncada (`ultima`,
    término → ISO UTC), con piso de COMPRA_AGIL_DIAS_VENTANA días. Retorna (matches, resumen); el resumen trae
    `cursor` y `ultima` actualizados para guardarlos en state.json.
    """
    if not isinstance(cursor, int):
        cursor = 0
    ultima = dict(ultima) if isinstance(ultima, dict) else {}
    rotativos = terminos_rotativos()
    resumen = {
        "diarios_ok": [], "diarios_fallidos": [], "rotativos_ok": [], "rotativos_total": len(rotativos),
        "truncados": [], "cursor": cursor, "ultima": ultima, "devueltas": 0, "cortado": "",
        "listado_ok": False, "listado_paginas": 0, "listado_total": None, "listado_desde": "",
        "listado_corte": "", "listado_hueco": "", "listado_pendiente": "",
    }
    global _solicitudes, _ultima_solicitud
    _solicitudes = 0
    _ultima_solicitud = 0.0
    disponibles = tickets()
    if not disponibles:
        logger.error("MERCADO_PUBLICO_TOKEN no configurado (Compra Ágil)")
        resumen["diarios_fallidos"] = list(COMPRA_AGIL_TERMINOS_DIARIOS)
        resumen["cortado"] = "sin ticket"
        return [], resumen

    ahora = datetime.now(timezone.utc)
    por_codigo: dict[str, dict] = {}
    devueltos: set[str] = set()

    def con_respaldo(fn, *args):
        # Ante 401/403 se pasa al ticket de respaldo y se repite. Ante 429 no: ver _tickets.py.
        while True:
            nombre, ticket = disponibles[0]
            try:
                return fn(ticket, *args)
            except _TicketRechazado as e:
                disponibles.pop(0)
                if not disponibles:
                    alcance = "principal y respaldo" if nombre == "respaldo" else nombre
                    raise _CuotaAgotada(f"{e}: {alcance}, sin otro ticket")
                logger.error(f"Compra Ágil: {e} con el ticket {nombre}; se pasa al {disponibles[0][0]}")

    # (0) Listado completo desde donde se leyó sin hueco la última vez, filtrado por título.
    tope = ahora - timedelta(days=LISTADO_DIAS_MAX)
    marca = _parse_iso(ultima.get(CLAVE_LISTADO))
    if marca is None:
        desde_listado = ahora - timedelta(days=COMPRA_AGIL_DIAS_VENTANA)
    else:
        desde_listado = max(marca - LISTADO_TRASLAPE, tope)
        if marca < tope:
            # Lo publicado entre la marca y el tope no se leerá: se dice en el correo.
            resumen["listado_hueco"] = f"{_iso(marca)} a {_iso(tope)}"
            logger.error(f"Compra Ágil listado: hueco sin leer de {resumen['listado_hueco']} (tope {LISTADO_DIAS_MAX} d)")
    resumen["listado_desde"] = _iso(desde_listado)
    limite = time.monotonic() + PRESUPUESTO_LISTADO_S
    tramo_desde, n_publicadas, total_conocido, b = desde_listado, 0, True, {"corte": ""}
    resumen["listado_total"] = 0
    while tramo_desde < ahora:
        tramo_hasta = min(tramo_desde + LISTADO_TRAMO, ahora)
        # hasta + 1 min: la fecha_publicacion viene al minuto y no está medido si el
        # borde es inclusivo; el solape solo duplica, y se deduplica por código.
        b = _barrer_listado(disponibles, _api_fecha(tramo_desde), limite,
                            _api_fecha(tramo_hasta + timedelta(minutes=1)))
        resumen["listado_paginas"] += b["leidas"]
        if b["total"] is None:
            total_conocido = False
            resumen["listado_total"] += b["leidas"]  # al menos lo leído, para no quedar bajo las páginas
        else:
            resumen["listado_total"] += b["total"]
        n_publicadas += len(b["items"])
        for it in b["items"]:
            if it.get("codigo"):
                devueltos.add(it["codigo"])
            d = _item_de_listado(it)
            if d and d["codigo"] not in por_codigo:
                por_codigo[d["codigo"]] = d
        completo = bool(b["total"]) and b["prefijo"] == b["total"] and not b["corte"]
        logger.info(f"Compra Ágil listado {_iso(tramo_desde)} → {_iso(tramo_hasta)}: {b['leidas']}/{b['total']} "
                    f"páginas, {len(b['items'])} publicadas" + (f"; cortado: {b['corte']}" if b["corte"] else ""))
        if not completo:
            resumen["listado_corte"] = b["corte"] or "una página no respondió"
            break
        # Tramo leído entero: la marca pasa a su fin (con traslape en la próxima corrida).
        ultima[CLAVE_LISTADO] = _iso(tramo_hasta)
        tramo_desde = tramo_hasta
    resumen["listado_ok"] = tramo_desde >= ahora
    if not total_conocido and not resumen["listado_paginas"]:
        resumen["listado_total"] = None
    elif not resumen["listado_ok"]:
        # Total de los tramos recorridos; los que no se alcanzaron no se conocen.
        resumen["listado_pendiente"] = f"{_iso(tramo_desde)} a {_iso(ahora)}"
    logger.info(f"Compra Ágil listado desde {resumen['listado_desde']}: {resumen['listado_paginas']} páginas, "
                f"{n_publicadas} publicadas, {len(por_codigo)} con keyword en el título, "
                f"marca {ultima.get(CLAVE_LISTADO)}"
                + (f"; sin leer {resumen['listado_pendiente']}" if resumen["listado_pendiente"] else ""))
    if "429" in b["corte"] or "sin otro ticket" in b["corte"]:
        # La búsqueda q chocaría con lo mismo: se corta aquí y se guarda lo leído.
        resumen["cortado"] = b["corte"]
        resumen["diarios_fallidos"] = list(COMPRA_AGIL_TERMINOS_DIARIOS)
        resumen["devueltas"] = len(devueltos)
        return list(por_codigo.values()), resumen
    if not disponibles:
        resumen["cortado"] = "sin ticket"
        resumen["diarios_fallidos"] = list(COMPRA_AGIL_TERMINOS_DIARIOS)
        resumen["devueltas"] = len(devueltos)
        return list(por_codigo.values()), resumen

    inicio = time.monotonic()

    def queda_tiempo(reserva_s: float = 0) -> bool:
        return time.monotonic() - inicio < presupuesto_s - reserva_s

    def buscar(termino: str) -> tuple[list[dict], bool] | None:
        return con_respaldo(_buscar_termino, termino, _desde_rotativo(ultima.get(termino), ahora))

    def procesar(termino: str) -> bool:
        r = buscar(termino)
        if r is None:
            return False
        items, truncado = r
        if truncado:
            # No se avanza `ultima`: la próxima búsqueda vuelve a cubrir el tramo.
            resumen["truncados"].append(termino)
        else:
            ultima[termino] = _iso(ahora)
        for it in items:
            if it.get("codigo"):
                devueltos.add(it["codigo"])
            d = _item_de_busqueda(it, termino)
            if d and d["codigo"] not in por_codigo:
                por_codigo[d["codigo"]] = d
        return True

    pos = cursor % len(rotativos) if rotativos else cursor
    try:
        pendientes = []
        for termino in COMPRA_AGIL_TERMINOS_DIARIOS:
            if queda_tiempo() and procesar(termino):
                resumen["diarios_ok"].append(termino)
            else:
                pendientes.append(termino)

        # Si ningún diario respondió en la primera pasada, el reintento va de
        # inmediato: de él depende si se corren los rotativos.
        if not resumen["diarios_ok"]:
            for termino in pendientes:
                if queda_tiempo() and procesar(termino):
                    resumen["diarios_ok"].append(termino)
                else:
                    resumen["diarios_fallidos"].append(termino)
            pendientes = []

        # Si ningún diario respondió la API está caída: no se gastan los
        # rotativos y el aviso «no revisó esa fuente» del correo es exacto.
        # La reserva suma un TIMEOUT por el rotativo que esté en vuelo.
        reserva = len(pendientes) * RESERVA_POR_REINTENTO_S + (TIMEOUT if pendientes else 0)
        if rotativos and resumen["diarios_ok"]:
            for _ in range(len(rotativos)):
                if not queda_tiempo(reserva):
                    break
                termino = rotativos[pos]
                # Un rotativo que falla se salta; conserva su `ultima`, así la
                # próxima vez busca desde antes y no deja hueco.
                if procesar(termino):
                    resumen["rotativos_ok"].append(termino)
                pos = (pos + 1) % len(rotativos)

        for termino in pendientes:
            if queda_tiempo() and procesar(termino):
                resumen["diarios_ok"].append(termino)
            else:
                resumen["diarios_fallidos"].append(termino)
    except _CuotaAgotada as e:
        logger.error(f"Compra Ágil: {e}. Se detiene la búsqueda.")
        resumen["cortado"] = str(e)
        hechos = set(resumen["diarios_ok"])
        resumen["diarios_fallidos"] = [t for t in COMPRA_AGIL_TERMINOS_DIARIOS if t not in hechos]
    resumen["cursor"] = pos

    resumen["devueltas"] = len(devueltos)
    logger.info(
        f"Compra Ágil: diarios {len(resumen['diarios_ok'])}/{len(COMPRA_AGIL_TERMINOS_DIARIOS)} ok, "
        f"rotativos {len(resumen['rotativos_ok'])}/{len(rotativos)} ok (cursor {cursor}→{resumen['cursor']}), "
        f"{resumen['devueltas']} devueltas, {len(por_codigo)} tras exclusiones, "
        f"{_solicitudes} solicitudes, ticket {disponibles[0][0] if disponibles else 'ninguno'}"
    )
    if resumen["diarios_fallidos"]:
        logger.warning(f"Compra Ágil: diarios sin respuesta: {', '.join(resumen['diarios_fallidos'])}")
    return list(por_codigo.values()), resumen
