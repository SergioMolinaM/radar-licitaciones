"""Fuente: PNUD Procurement Notices vía RSS.

Endpoint base: https://procurement-notices.undp.org/rss_feeds/{CODIGO}.xml
- CODIGO = código propietario PNUD (no ISO3 estándar). Ej: BOL, PER, COL.
- Chile no tiene feed propio: usar Mercado Público para Chile.
- Feed global (rss.xml) atrapa licitaciones regionales/multipaís.
Formato: RSS 1.0 (RDF), actualizado cada hora.
"""

import logging
import feedparser
import requests

from ..config import UNDP_FEEDS, UNDP_GLOBAL_FEED, UNDP_GLOBAL_PAIS_FILTRO
from ..filters import matches_keywords

logger = logging.getLogger(__name__)

TIMEOUT = 30
USER_AGENT = "RadarLicitaciones-TerceraLetra/1.0 (+https://terceraletra.cl)"


def _entry_to_item(entry, fuente: str) -> dict | None:
    """Transforma una entrada RSS en el esquema interno."""
    titulo = entry.get("title", "") or ""
    descripcion = entry.get("description", "") or entry.get("summary", "") or ""
    texto_match = f"{titulo} {descripcion}"

    match, kws = matches_keywords(texto_match)
    if not match:
        return None

    link = entry.get("link", "")
    uid = entry.get("id") or link
    if not uid:
        return None

    return {
        "fuente": fuente,
        "id": f"UNDP::{uid}",
        "codigo": uid.split("/")[-1] if "/" in uid else uid,
        "titulo": titulo,
        "estado": "Publicada",
        "fecha_cierre": entry.get("updated", "") or entry.get("published", ""),
        "link": link,
        "keywords_match": kws,
    }


def _fetch_feed(url: str, fuente: str, pais_filtro: list[str] | None = None) -> tuple[list[dict], int]:
    """Descarga y parsea un feed RSS. Opcionalmente filtra por país en título.

    Retorna (matches, total_entries_del_feed). El segundo valor alimenta el
    universo total para el heartbeat.
    """
    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
        resp.raise_for_status()
        feed = feedparser.parse(resp.content)
    except requests.RequestException as e:
        logger.error(f"{fuente}: error de red — {e}")
        return [], 0

    entries = feed.entries or []
    logger.info(f"{fuente}: {len(entries)} entradas en feed")

    resultados = []
    for entry in entries:
        # Filtro geográfico opcional (para feed global)
        if pais_filtro:
            texto = (entry.get("title", "") + " " + entry.get("description", "")).lower()
            if not any(p in texto for p in pais_filtro):
                continue

        item = _entry_to_item(entry, fuente)
        if item:
            resultados.append(item)

    return resultados, len(entries)


def fetch_undp_notices() -> tuple[list[dict], int]:
    """Consulta todos los feeds PNUD (país + global) y dedupea por ID interno.

    Retorna (matches, universo_total). `universo_total` es la suma de entradas
    en todos los feeds (antes de filtro keywords), útil para el heartbeat.
    """
    resultados: dict[str, dict] = {}
    universo_total = 0

    # Feeds por país
    for pais, url in UNDP_FEEDS.items():
        matches, universo = _fetch_feed(url, f"PNUD {pais}")
        universo_total += universo
        for item in matches:
            resultados[item["id"]] = item

    # Feed global con filtro geográfico
    if UNDP_GLOBAL_FEED:
        matches, universo = _fetch_feed(
            UNDP_GLOBAL_FEED, "PNUD Global", pais_filtro=UNDP_GLOBAL_PAIS_FILTRO
        )
        universo_total += universo
        for item in matches:
            # No sobrescribir si ya vino por feed país
            resultados.setdefault(item["id"], item)

    items = list(resultados.values())
    logger.info(f"PNUD: {len(items)} matches únicos tras filtro keywords")
    return items, universo_total
