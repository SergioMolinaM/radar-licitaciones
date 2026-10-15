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

Estrategia del radar (desde el 14-oct-2026): búsqueda por palabra clave en el
servidor (`q`) sobre las publicadas de los últimos COMPRA_AGIL_DIAS_VENTANA
días: los términos diarios en cada corrida y el resto en rotación
(fetch_compra_agil). El barrido completo del listado (fetch_raw_publicadas)
queda solo para la auditoría: con la API respondiendo en 23-29 s por página y
cortando a los 29 s, y ~5.400 publicadas en 3 días, no termina. La
deduplicación por state.json evita re-notificar día tras día.

Nota de cuota: el límite es por ticket y por día calendario, y se devuelve 429
al agotarlo (§4). Con estado=publicada + ventana de 3 días el universo ronda las
~800 Compras Ágiles, es decir ~16 páginas de 50. MAX_PAGINAS es el tope de
seguridad. Ante 429 se detiene y retorna lo acumulado (no revienta la corrida).
"""

import os
import time
import logging
from datetime import datetime, timedelta, timezone

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

logger = logging.getLogger(__name__)

TIMEOUT = 60
TAMANO_PAGINA = 50          # máximo permitido por la API (default 15, mínimo 10)  [guía §5.1 Grupo 6]
MAX_PAGINAS = 80            # tope de seguridad del barrido completo (solo auditoría)
MAX_PAGINAS_TERMINO = 5     # una búsqueda q trae 1-19 resultados (medido 14-oct); 5 páginas = 250
REINTENTOS_ESPERA_S = (20, 60)  # barrido completo: esperas entre intentos ante 5xx/red
PRESUPUESTO_BARRIDO_S = 15 * 60  # tope del barrido completo (auditoría)
PRESUPUESTO_BUSQUEDA_S = 20 * 60  # tope de la búsqueda diaria; el job tiene timeout-minutes: 40
RESERVA_POR_REINTENTO_S = 30  # un 504 tarda ~29 s; se aparta este tiempo por diario fallido


def _get_ticket() -> str | None:
    ticket = os.getenv("MERCADO_PUBLICO_TOKEN")
    if not ticket:
        logger.error("MERCADO_PUBLICO_TOKEN no configurado (Compra Ágil)")
    return ticket


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
        logger.warning("Compra Ágil: cuota diaria agotada (429). Se detiene el barrido.")
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
            logger.warning(f"Compra Ágil: cuota agotada (429) al pedir detalle de {codigo}")
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


def _buscar_termino(ticket: str, termino: str, publicado_desde: str) -> tuple[list[dict], bool] | None:
    """Un intento de búsqueda `q` (guía §5.1 Grupo 5), todas sus páginas.

    Retorna (items, truncado) o None si alguna página falla (504, 5xx, red,
    JSON o forma inesperada). Lanza _CuotaAgotada ante 429 y ante ticket
    rechazado: seguir no sirve.
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
            resp = requests.get(COMPRA_AGIL_API_URL, headers={"ticket": ticket}, params=params, timeout=TIMEOUT)
        except requests.RequestException as e:
            logger.warning(f"Compra Ágil q={termino!r}: error de red — {type(e).__name__}")
            return None
        if resp.status_code == 429:
            raise _CuotaAgotada("cuota diaria agotada (429)")
        if resp.status_code in (401, 403):
            raise _CuotaAgotada(f"ticket rechazado ({resp.status_code})")
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
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _desde_rotativo(ultima: str | None, ahora: datetime) -> str:
    """Desde la última búsqueda exitosa del término (con 1 h de traslape), con
    piso en la ventana diaria y techo en COMPRA_AGIL_DIAS_MAX_ROTATIVO días."""
    minimo = ahora - timedelta(days=COMPRA_AGIL_DIAS_MAX_ROTATIVO)
    por_defecto = ahora - timedelta(days=COMPRA_AGIL_DIAS_VENTANA)
    try:
        dt = datetime.strptime(ultima, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc) - timedelta(hours=1)
    except (TypeError, ValueError):
        return _iso(por_defecto)
    return _iso(max(minimo, min(dt, por_defecto)))


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
    }
    ticket = _get_ticket()
    if not ticket:
        resumen["diarios_fallidos"] = list(COMPRA_AGIL_TERMINOS_DIARIOS)
        resumen["cortado"] = "sin ticket"
        return [], resumen

    ahora = datetime.now(timezone.utc)
    inicio = time.monotonic()
    por_codigo: dict[str, dict] = {}
    devueltos: set[str] = set()

    def queda_tiempo(reserva_s: float = 0) -> bool:
        return time.monotonic() - inicio < presupuesto_s - reserva_s

    def procesar(termino: str) -> bool:
        r = _buscar_termino(ticket, termino, _desde_rotativo(ultima.get(termino), ahora))
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
        f"{resumen['devueltas']} devueltas, {len(por_codigo)} tras exclusiones"
    )
    if resumen["diarios_fallidos"]:
        logger.warning(f"Compra Ágil: diarios sin respuesta: {', '.join(resumen['diarios_fallidos'])}")
    return list(por_codigo.values()), resumen
