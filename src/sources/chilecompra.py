"""ChileCompra: licitaciones de la plataforma nueva y consultas al mercado.

Hueco medido el 17-oct-2026: los procesos de la «nueva plataforma modular» de Mercado
Público (códigos como 869591-4-LE126) y las Consultas al Mercado (…-RFIPRI26) no salen
en la API v1 de Mercado Público, y la API de consulta-mercado.mercadopublico.cl exige
reCAPTCHA (no se automatiza). ChileCompra anuncia esos procesos en las noticias de
chilecompra.cl, que se leen por la API pública de WordPress (/wp-json/wp/v2/posts).

No pasa por el filtro de palabras clave: son pocas notas por semana y el Radar es amplio
(decide Sergio). Se descartan:
- la categoría «Normativa» (id 8): son los manuales de compras de cada organismo
  («Servicio Local de Educación Pública de Aysén – Octubre 5, 2026», solo un PDF);
- noticias institucionales, capacitaciones, Cosoc, adjudicaciones y compras coordinadas
  en que se inscriben organismos, no proveedores;
- los avisos cuyo cierre, leído del texto, ya pasó.
"""

import html
import logging
import re
import unicodedata
from datetime import datetime, timedelta, timezone

import requests

logger = logging.getLogger(__name__)

API = "https://www.chilecompra.cl/wp-json/wp/v2/posts"
CAMPOS = "id,date,date_gmt,link,title,content,categories"
POR_PAGINA = 50
MAX_PAGINAS = 5
TIMEOUT = 30
VENTANA_INICIAL_DIAS = 30  # primera corrida (sin marca en state)
MARGEN_HORAS = 48  # se relee hacia atrás; los repetidos los saca `seen`
FUENTE = "ChileCompra: plataforma nueva y consultas al mercado"
CATEGORIA_NORMATIVA = 8
# Las horas de las notas son de Chile. Se leen como UTC-4 (la más tardía posible del
# año): con horario de verano un aviso se descarta una hora después de cerrar, nunca antes.
_CHILE = timezone(timedelta(hours=-4))

_MESES = {m: i for i, m in enumerate(
    ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
     "septiembre", "octubre", "noviembre", "diciembre"], 1)}
_MESES["setiembre"] = 9

# Códigos de Mercado Público: organismo-número-tipo+año. Vistos en las notas: LE126 y
# LP26 (plataforma nueva), LR26 (convenio marco y compra coordinada), RFIPRI26,
# RFIPUB26, RFI26, COT26 (Compra Ágil). El tipo se acepta genérico: una lista cerrada
# perdía tipos no vistos (LS, R1), y LS son justo servicios especializados (verificador, 17-oct).
_ID = re.compile(r"(?<![\w-])(\d{1,8}-\d{1,5}-[A-Z]{1,6}1?\d{2})(?![\w-])")

_FECHA = re.compile(r"(?:(?:lunes|martes|miercoles|jueves|viernes|sabado|domingo)\s+)?"
                    r"(\d{1,2})\s+de\s+(" + "|".join(_MESES) + r")(?:\s+(?:de|del)\s+(\d{4}))?")
_FECHA_NUM = re.compile(r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})")  # «Cierre: 30/10/2026 a las 15:00»
_HORA = re.compile(r"(\d{1,2})[:.](\d{2})\s*(?:horas|hrs|h\b)")
# Dónde una nota dice hasta cuándo se puede ofertar o responder.
# «extiende/amplía/recibe» cubren «el plazo, que vencía el 16, se extiende al 30».
_ANCLA_CIERRE = re.compile(r"\bhasta\b|\bcierre\b|\bplazo\b|\bdisponible\b|\babierta?\b|extiend|\bamplia|\brecibe")
_VENTANA_CIERRE = 140

_ES_PROCESO = re.compile(r"licita|ofert|consultas? al mercado|\brfi\b|convenio marco|compra coordinada")
# El título tiene que invitar a ofertar o responder: «logra ahorros», «revisa el Convenio
# Marco» son notas de resultados de procesos ya cerrados.
_TITULO_INVITA = re.compile(r"ofert|licita|particip|se parte|invita|consultas? al mercado|plazo|extiend|ampli")
_NO_ES_PROCESO = re.compile(r"adjudic|organismos? (publicos? )?(pueden|deben|a sumarse)|instruye|inscribirse"
                            r"|cosoc|consejo de la sociedad civil|consulta ciudadana|declaracion jurada")
# Capacitaciones y eventos de ChileCompra; con un ID en la nota es una licitación de ese
# rubro («licita servicio de capacitación»), que es justo lo que busca TL: no se descarta.
_ES_EVENTO = re.compile(r"webinar|seminario|\bcursos?\b|taller|capacitaci|masterclass|orientaciones")


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    s = re.sub(r"\s+", " ", s)
    return re.sub(r"\b(\d) (\d) de\b", r"\1\2 de", s)  # «Hasta el 2 0 de octubre» (nota del 5-oct)


def _texto(rendered: str) -> str:
    """HTML de WordPress a texto plano (incluye los atajos [vc_*] del maquetador)."""
    t = re.sub(r"<[^>]+>|\[/?vc_[^\]]*\]", " ", rendered or "")
    t = html.unescape(t).replace(" ", " ")
    t = re.sub(r"[‐-―−]", "-", t)
    return re.sub(r"\s+", " ", t).strip()


def extraer_ids(texto: str) -> list[str]:
    """IDs en orden de frecuencia. Se descarta el que es cola de otro (la nota del 5-oct
    dice «ID 2317-3-RFIPRI26» y luego el correcto «1122317-3-RFIPRI26»)."""
    vistos: dict[str, int] = {}
    for m in _ID.finditer(texto):
        vistos[m.group(1)] = vistos.get(m.group(1), 0) + 1
    ids = [i for i in vistos if not any(o != i and o.endswith(i) and o[-len(i) - 1].isdigit() for o in vistos)]
    return sorted(ids, key=lambda i: -vistos[i])


def _anio_id(id_: str) -> int:
    return 2000 + int(id_[-2:])


def extraer_cierre(texto: str, publicada: datetime):
    """Fecha y hora de cierre según la nota (hora de Chile, sin tz) y si traía hora.
    Toma la más tardía de las fechas que siguen a «hasta», «cierre» o «plazo»: en una
    extensión de plazo la nueva fecha es la última. None si la nota no la dice."""
    t = _norm(texto)
    candidatos = []
    for a in _ANCLA_CIERRE.finditer(t):
        ventana = t[a.start(): a.start() + _VENTANA_CIERRE]
        f, fn = _FECHA.search(ventana), _FECHA_NUM.search(ventana)
        if fn and (not f or fn.start() < f.start()):
            f, dia, mes, anio_txt = fn, int(fn.group(1)), int(fn.group(2)), fn.group(3)
        elif f:
            dia, mes, anio_txt = int(f.group(1)), _MESES[f.group(2)], f.group(3)
        else:
            continue
        # «El plazo de adjudicación es hasta el 30 de noviembre» no es el cierre de ofertas.
        if "adjudic" in t[max(0, a.start() - 60): a.start() + f.end()]:
            continue
        anio = int(anio_txt) if anio_txt else publicada.year
        try:
            fecha = datetime(anio, mes, dia)
        except ValueError:
            continue
        if not anio_txt and fecha < publicada.replace(tzinfo=None) - timedelta(days=60):
            fecha = fecha.replace(year=anio + 1)  # nota de diciembre que dice «hasta el 5 de enero»
        h = _HORA.search(ventana)
        con_hora = bool(h and 0 <= int(h.group(1)) <= 23 and 0 <= int(h.group(2)) <= 59)
        fecha = fecha.replace(hour=int(h.group(1)), minute=int(h.group(2))) if con_hora \
            else fecha.replace(hour=23, minute=59)
        candidatos.append((fecha, con_hora))
    if not candidatos:
        return None
    # Si una fecha aparece con hora y sin ella («abierta hasta el 5 de junio» y «hasta las
    # 10:00 horas del 5 de junio»), vale la que trae hora.
    con_hora_por_dia = {f.date() for f, h in candidatos if h}
    candidatos = [(f, h) for f, h in candidatos if h or f.date() not in con_hora_por_dia]
    return max(candidatos)


def tipo_de_aviso(titulo: str, texto: str) -> str:
    t = _norm(titulo + " " + texto[:400])
    if re.search(r"consultas? al mercado|\brfi\b", t):
        tipo = "Consulta al mercado"
    elif "convenio marco" in t:
        tipo = "Licitación de convenio marco"
    elif "compra coordinada" in t:
        tipo = "Compra coordinada"
    else:
        tipo = "Licitación"
    if re.search(r"extiend|extension|ampli|nuevo plazo", _norm(titulo)):
        tipo += " (plazo extendido)"
    return tipo


def es_aviso_de_proceso(post: dict, titulo: str, texto: str, ids: list[str]) -> bool:
    if CATEGORIA_NORMATIVA in (post.get("categories") or []):
        return False
    tn = _norm(titulo)
    if _NO_ES_PROCESO.search(tn) or (_ES_EVENTO.search(tn) and not ids):
        return False
    # Título que no invita («Nuevo Convenio Marco de Aseo: conoce las bases»): pasa solo con
    # ID e invitación en el texto; post_a_item además le exige un cierre futuro.
    if not _TITULO_INVITA.search(tn) and not (ids and re.search(r"ofert|particip|invita", _norm(texto[:600]))):
        return False
    if not _ES_PROCESO.search(tn + " " + _norm(texto[:600])):
        return False
    return bool(ids) or bool(re.search(r"licita|consultas? al mercado", tn))


def _publicada(post: dict) -> datetime:
    gmt = post.get("date_gmt")
    if gmt:
        return datetime.fromisoformat(gmt).replace(tzinfo=timezone.utc)
    return datetime.fromisoformat(post["date"]).replace(tzinfo=_CHILE)


def post_a_item(post: dict, ahora: datetime):
    """Item del correo, o None si la nota no anuncia un proceso abierto."""
    titulo = _texto(post.get("title", {}).get("rendered", ""))
    texto = _texto(post.get("content", {}).get("rendered", ""))
    ids = extraer_ids(titulo + " " + texto)
    if not es_aviso_de_proceso(post, titulo, texto, ids):
        return None
    publicada = _publicada(post)
    # Un código de un año anterior al de la nota es una referencia («reemplaza al 2239-19-LR23»).
    actuales = [i for i in ids if _anio_id(i) >= publicada.year] or ids
    cierre = extraer_cierre(texto, publicada)
    if not cierre and not _TITULO_INVITA.search(_norm(titulo)):
        return None  # «logra ahorros», «revisa el Convenio Marco»: resultados, sin plazo abierto
    if cierre:
        fecha, con_hora = cierre
        if fecha.replace(tzinfo=_CHILE) < ahora:
            return None
        fecha_cierre = fecha.strftime("%d/%m/%Y %H:%M" if con_hora else "%d/%m/%Y")
    else:
        fecha_cierre = "no indicado en la nota"
    return {
        "fuente": FUENTE,
        "id": f"CC::{post['id']}",
        "codigo": ", ".join(actuales) if actuales else "sin ID en la nota",
        "titulo": html.escape(titulo),
        "estado": tipo_de_aviso(titulo, texto),
        "fecha_cierre": fecha_cierre,
        "link": post.get("link", ""),
        "keywords_match": [f"nota de chilecompra.cl del {publicada.astimezone(_CHILE).strftime('%d/%m/%Y')}"],
    }


def fetch_avisos_chilecompra(ultima: str | None = None, ahora: datetime | None = None, session=None):
    """Devuelve (items, resumen). resumen = {ok, leidas, ultima}. ok=False si la API no
    respondió bien en alguna página: es fuente caída y la marca `ultima` no avanza.
    Nunca lanza."""
    ahora = ahora or datetime.now(timezone.utc)
    http = session or requests
    try:
        desde = datetime.fromisoformat(ultima) - timedelta(hours=MARGEN_HORAS) if ultima \
            else ahora - timedelta(days=VENTANA_INICIAL_DIAS)
    except ValueError:
        desde = ahora - timedelta(days=VENTANA_INICIAL_DIAS)
    if desde.tzinfo is None:
        desde = desde.replace(tzinfo=timezone.utc)
    # `after` de WordPress compara con la fecha local del sitio (Chile): se pide en esa hora.
    after = desde.astimezone(_CHILE).replace(tzinfo=None).isoformat(timespec="seconds")

    posts, ok = [], True
    pagina, total_paginas = 1, 1
    while pagina <= min(total_paginas, MAX_PAGINAS):
        try:
            resp = http.get(API, params={"per_page": POR_PAGINA, "page": pagina, "after": after,
                                         "orderby": "date", "order": "desc", "_fields": CAMPOS},
                            headers={"User-Agent": "RadarLicitaciones-TerceraLetra/1.0 (+https://terceraletra.cl)"},
                            timeout=TIMEOUT)
            resp.raise_for_status()
            lote = resp.json()
            if not isinstance(lote, list):
                raise ValueError("la respuesta no es una lista")
            total_paginas = int(resp.headers.get("X-WP-TotalPages", "1") or 1)
        except Exception as e:  # red, HTTP, JSON: la fuente se informa caída
            logger.error(f"ChileCompra noticias, página {pagina}: sin respuesta ({e})")
            ok = False
            break
        posts.extend(p for p in lote if isinstance(p, dict))
        pagina += 1
    if ok and total_paginas > MAX_PAGINAS:
        logger.warning(f"ChileCompra noticias: {total_paginas} páginas desde {after}; se leyeron {MAX_PAGINAS}")

    items, ultima_nueva = [], ultima
    for p in posts:
        try:
            item = post_a_item(p, ahora)
            pub = _publicada(p).astimezone(timezone.utc).replace(tzinfo=None).isoformat(timespec="seconds")
        except Exception as e:
            logger.warning(f"ChileCompra noticias: nota {p.get('id')} ilegible ({e})")
            continue
        if ok and (not ultima_nueva or pub > ultima_nueva):
            ultima_nueva = pub
        if item:
            items.append(item)
    logger.info(f"ChileCompra noticias desde {after}: {len(posts)} leídas, {len(items)} avisos de procesos abiertos"
                + (f" ({', '.join(i['codigo'] for i in items)})" if items else ""))
    return items, {"ok": ok, "leidas": len(posts), "ultima": ultima_nueva if ok else ultima}
