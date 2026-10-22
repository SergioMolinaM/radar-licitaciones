"""Fuente: Mercado Público (ChileCompra).

API correcta verificada en api.mercadopublico.cl:
  https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json
  ?estado=activas&ticket=XXX

Nota crítica: sin parámetro 'estado' la API solo devuelve ~20 licitaciones del día.
Con estado=activas devuelve ~5.000 licitaciones activas (universo real).
El campo Estado en la respuesta viene None aunque ya esté filtrado server-side.

Se consulta sin fecha para obtener TODAS las activas. La deduplicación
por state.json evita re-notificar las mismas licitaciones día tras día.
"""

import logging
import requests

from ..config import MP_API_URL
from ._tickets import tickets
from ..filters import matches_keywords

logger = logging.getLogger(__name__)

TIMEOUT = 60  # Subido porque el response es ~5MB


def fetch_raw_activas() -> list[dict]:
    """Consulta la API de MP y retorna el listado crudo, sin filtrar.

    Uso principal: auditoría de keywords (src/audit.py) y también fuente para
    fetch_licitaciones_dia. Retorna [] si el token falla o la API responde mal.
    """
    disponibles = tickets()
    if not disponibles:
        logger.error("MERCADO_PUBLICO_TOKEN no configurado")
        return []

    for nombre, ticket in disponibles:
        params = {"estado": "activas", "ticket": ticket}

        try:
            resp = requests.get(MP_API_URL, params=params, timeout=TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            # El mensaje de requests trae la URL y en ella el ticket: no se loguea.
            logger.error(f"Error consultando Mercado Público: {type(e).__name__}")
            return []
        except ValueError as e:
            logger.error(f"Respuesta no es JSON válido: {e}")
            return []

        # Los errores de la API v1 llegan como {"Codigo", "Mensaje"} sin Listado
        # y con HTTP 2xx (ticket inválido: 203; peticiones simultáneas: 200 con
        # Codigo 10500, medidos el 22-oct). Antes pasaban como 0 licitaciones.
        if not isinstance(data, dict):
            logger.error(f"Mercado Público: respuesta inesperada ({type(data).__name__})")
            return []
        if "Listado" not in data:
            codigo, mensaje = data.get("Codigo"), data.get("Mensaje")
            logger.error(f"Mercado Público: error de la API con ticket {nombre} — {codigo}: {mensaje}")
            if codigo == 203:
                continue  # ticket rechazado: se prueba el respaldo, si hay
            return []

        if nombre != "principal":
            logger.warning(f"Mercado Público: se usó el ticket {nombre}; revisar el principal")
        listado = data.get("Listado") or []
        cantidad = data.get("Cantidad", len(listado))
        logger.info(f"Mercado Público: {cantidad} licitaciones activas en total")
        return listado
    return []


def fetch_licitaciones_dia() -> tuple[list[dict], int]:
    """Consulta licitaciones activas y filtra por keywords.

    Retorna (matches, universo_total). `universo_total` es el nº de licitaciones
    activas que devolvió la API, útil para el heartbeat semanal.
    """
    listado = fetch_raw_activas()
    universo = len(listado)

    resultados = []
    for lic in listado:
        nombre = lic.get("Nombre", "") or ""
        codigo = lic.get("CodigoExterno")

        if not codigo:
            continue

        match, kws = matches_keywords(nombre)
        if not match:
            continue

        resultados.append({
            "fuente": "Mercado Público",
            "id": f"MP::{codigo}",
            "codigo": codigo,
            "titulo": nombre,
            "estado": "Activa",
            "fecha_cierre": lic.get("FechaCierre", ""),
            "link": f"https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?idlicitacion={codigo}",
            "keywords_match": kws,
        })

    logger.info(f"Mercado Público: {len(resultados)} matches tras filtro keywords")
    return resultados, universo
