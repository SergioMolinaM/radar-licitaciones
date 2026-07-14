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

Estrategia del radar: traer las Compras Ágiles con estado=publicada de los
últimos COMPRA_AGIL_DIAS_VENTANA días (cubre fin de semana en la corrida del
lunes), paginar hasta agotar, y filtrar por keywords. La deduplicación por
state.json evita re-notificar día tras día.

Nota de cuota: el límite es por ticket y por día calendario, y se devuelve 429
al agotarlo (§4). Con estado=publicada + ventana de 3 días el universo ronda las
~800 Compras Ágiles, es decir ~16 páginas de 50. MAX_PAGINAS es el tope de
seguridad. Ante 429 se detiene y retorna lo acumulado (no revienta la corrida).
"""

import os
import logging
from datetime import datetime, timedelta, timezone

import requests

from ..config import (
    COMPRA_AGIL_API_URL,
    COMPRA_AGIL_ESTADOS,
    COMPRA_AGIL_DIAS_VENTANA,
    COMPRA_AGIL_WEB_URL_TEMPLATE,
)
from ..filters import matches_keywords

logger = logging.getLogger(__name__)

TIMEOUT = 60
TAMANO_PAGINA = 50          # máximo permitido por la API (default 15)  [guía §5.1 Grupo 6]
MAX_PAGINAS = 80            # tope de seguridad (80 * 50 = 4.000 registros/corrida)


def _get_ticket() -> str | None:
    ticket = os.getenv("MERCADO_PUBLICO_TOKEN")
    if not ticket:
        logger.error("MERCADO_PUBLICO_TOKEN no configurado (Compra Ágil)")
    return ticket


def _fetch_pagina(ticket: str, publicado_desde: str, numero_pagina: int) -> dict | None:
    """Consulta una página del listado. Retorna el payload o None si falla."""
    params = {
        "estado": COMPRA_AGIL_ESTADOS,
        "publicado_desde": publicado_desde,
        "ordenar_por": "FechaPublicacion",  # valor válido según guía §5.1 Grupo 7
        "tamano_pagina": TAMANO_PAGINA,
        "numero_pagina": numero_pagina,
    }
    try:
        resp = requests.get(
            COMPRA_AGIL_API_URL,
            headers={"ticket": ticket},
            params=params,
            timeout=TIMEOUT,
        )
    except requests.RequestException as e:
        logger.error(f"Compra Ágil: error de red (pág {numero_pagina}) — {e}")
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


def _item_to_dict(item: dict) -> dict | None:
    """Transforma un item del listado al esquema interno. None si no matchea."""
    nombre = item.get("nombre", "") or ""
    codigo = item.get("codigo")
    if not codigo:
        return None

    match, kws = matches_keywords(nombre)
    if not match:
        return None

    fechas = item.get("fechas") or {}
    montos = item.get("montos") or {}
    institucion = item.get("institucion") or {}

    return {
        "fuente": "Compra Ágil",
        "id": f"CA::{codigo}",
        "codigo": codigo,
        "titulo": nombre,
        "estado": (item.get("estado") or {}).get("glosa", "Publicada"),
        "fecha_cierre": fechas.get("fecha_cierre", ""),
        "link": COMPRA_AGIL_WEB_URL_TEMPLATE.format(codigo=codigo),
        "keywords_match": kws,
        # Extras útiles para el correo (no usados por el dedupe):
        "organismo": institucion.get("organismo_comprador", ""),
        "monto_clp": montos.get("monto_disponible_clp"),
    }


def fetch_raw_publicadas(dias_ventana: int = COMPRA_AGIL_DIAS_VENTANA) -> list[dict]:
    """Recorre el listado paginado y retorna los items crudos, sin filtrar.

    Uso: fuente para fetch_compra_agil y para la auditoría de keywords
    (src/audit_compra_agil.py). Retorna [] si el ticket falla o la API responde
    mal. Ante 429 retorna lo acumulado hasta ese punto.
    """
    ticket = _get_ticket()
    if not ticket:
        return []

    desde = datetime.now(timezone.utc) - timedelta(days=dias_ventana)
    publicado_desde = desde.strftime("%Y-%m-%dT%H:%M:%SZ")

    items: list[dict] = []
    numero_pagina = 1

    while numero_pagina <= MAX_PAGINAS:
        payload = _fetch_pagina(ticket, publicado_desde, numero_pagina)
        if payload is None:
            break

        items.extend(payload.get("items") or [])

        paginacion = payload.get("paginacion") or {}
        total_paginas = paginacion.get("total_paginas", numero_pagina)
        if numero_pagina >= total_paginas:
            break
        numero_pagina += 1
    else:
        logger.warning(
            f"Compra Ágil: se alcanzó MAX_PAGINAS ({MAX_PAGINAS}). "
            "El barrido quedó truncado — revisar si el universo creció."
        )

    return items


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


def fetch_compra_agil() -> tuple[list[dict], int]:
    """Consulta Compras Ágiles publicadas recientes y filtra por keywords.

    Retorna (matches, universo_total). `universo_total` es el nº de Compras
    Ágiles recorridas (antes del filtro), para el heartbeat semanal.
    """
    items = fetch_raw_publicadas()
    universo = len(items)

    resultados: list[dict] = []
    for item in items:
        d = _item_to_dict(item)
        if d:
            resultados.append(d)

    logger.info(
        f"Compra Ágil: {universo} publicadas recorridas, "
        f"{len(resultados)} matches tras filtro keywords"
    )
    return resultados, universo
