"""Fuente: empleos del PNUD (portal UNDP Careers, Oracle HCM), para Sergio como persona.

No son licitaciones: son contratos de personal (NPSA, IPSA, plazo fijo, pasantía) a los
que TL no puede postular como empresa. Van en una sección aparte del correo.
Los consultores individuales del PNUD no salen aquí: van por procurement-notices
(fuente undp.py). Medido el 26-oct-2026: 113 avisos en el sitio, ningún tipo IC.

Listado: recruitingCEJobRequisitions (finder findReqs, sin token ni cookie).
Detalle por aviso: recruitingCEJobRequisitionDetails (trae cierre y tipo de contrato).
Sin filtro de keywords: son pocos (1 en Chile y 7 remotos el 26-oct) y decide Sergio.
"""

import logging
import re
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import requests

logger = logging.getLogger(__name__)

TIMEOUT = 40
USER_AGENT = "RadarLicitaciones-TerceraLetra/1.0 (+https://terceraletra.cl)"
BASE = "https://estm.fa.em2.oraclecloud.com"
FUENTE = "Para Sergio: empleos PNUD (personas, no empresa)"
MAX_DETALLES = 30
try:
    CHILE_TZ = ZoneInfo("America/Santiago")
except ZoneInfoNotFoundError:  # Windows sin tzdata; el runner de GitHub (Ubuntu) la trae
    CHILE_TZ = timezone(timedelta(hours=-3))

# Ids de ubicación del portal (facet LOCATIONS, leídos el 26-oct-2026).
UBICACIONES = {
    "Chile": 300000000440503,
    "Home Based": 300000351810609,
}


def _get(path: str) -> dict:
    resp = requests.get(BASE + path, headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
                        timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def _listado(location_id: int) -> list[dict]:
    path = ("/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true"
            "&expand=requisitionList.secondaryLocations"
            f"&finder=findReqs;siteNumber=CX_1,limit=25,locationId={location_id},sortBy=POSTING_DATES_DESC")
    items = _get(path).get("items") or []
    return (items[0].get("requisitionList") or []) if items else []


def _detalle(job_id: str) -> dict:
    path = ("/hcmRestApi/resources/latest/recruitingCEJobRequisitionDetails?expand=requisitionFlexFields"
            f"&onlyData=true&finder=ById;Id=%22{job_id}%22,siteNumber=CX_1")
    items = _get(path).get("items") or []
    return items[0] if items else {}


def _cierre_chile(iso: str | None) -> str:
    """'2026-10-28T03:59:00+00:00' -> '2026-10-28' en hora de Chile (00:59). Vacío si no viene."""
    if not iso:
        return ""
    try:
        return datetime.fromisoformat(iso).astimezone(CHILE_TZ).date().isoformat()
    except ValueError:
        return ""


def _postulable(req: dict, det: dict) -> bool:
    """Lo de Chile pasa siempre. Lo remoto, solo si un externo en Chile puede postular:
    fuera los contratos nacionales de otro país, los restringidos a nacionales o a
    personal interno (Tier 1 y 2) y las pasantías. Medido el 26-oct-2026: de 7 remotos
    pasaba 1 (IPSA, abierto a externos)."""
    if req.get("PrimaryLocationCountry") == "CL":
        return True
    flex = {f.get("Prompt"): f.get("Value") for f in (det.get("requisitionFlexFields") or [])}
    titulo = (req.get("Title") or "").lower()
    tipo = (flex.get("Vacancy Type") or det.get("RequisitionType") or "").lower()
    # «intern» con borde de palabra: sin él, «Open to internal and external» quedaba fuera.
    if "nationals of" in titulo or "tier 1" in titulo or re.search(r"\bintern(ship)?\b", titulo):
        return False
    return not tipo.startswith(("national", "internship"))


def _item(req: dict, det: dict) -> dict:
    flex = {f.get("Prompt"): f.get("Value") for f in (det.get("requisitionFlexFields") or [])}
    extras = ", ".join(v for v in (flex.get("Vacancy Type"), flex.get("Contract Duration")) if v)
    titulo = f"{req.get('Title', '').strip()} — {req.get('PrimaryLocation', '')}"
    if extras:
        titulo += f" ({extras})"
    job_id = str(req.get("Id"))
    return {
        "fuente": FUENTE,
        "id": f"UNDPJOB::{job_id}",
        "codigo": job_id,
        "titulo": titulo,
        "estado": "Publicada",
        "fecha_cierre": _cierre_chile(det.get("ExternalPostedEndDate")),
        "link": f"{BASE}/hcmUI/CandidateExperience/en/sites/CX_1/job/{job_id}",
        "keywords_match": ["(empleo para persona natural)"],
    }


def fetch_empleos_undp() -> tuple[list[dict], list[str]]:
    """Retorna (items, fallas). `fallas` nombra lo que no se pudo revisar (ubicación o
    detalle); 0 avisos es posible y no es caída."""
    reqs: dict[str, dict] = {}
    fallas = []
    for nombre, loc in UBICACIONES.items():
        try:
            for r in _listado(loc):
                reqs.setdefault(str(r.get("Id")), r)
        except (requests.RequestException, ValueError) as e:
            logger.error(f"Empleos PNUD {nombre}: sin respuesta ({type(e).__name__})")
            fallas.append(nombre)
    if len(reqs) > MAX_DETALLES:
        fallas.append(f"más de {MAX_DETALLES} puestos (se revisaron los {MAX_DETALLES} más recientes)")
    items = []
    for job_id, req in list(reqs.items())[:MAX_DETALLES]:
        try:
            det = _detalle(job_id)
        except (requests.RequestException, ValueError) as e:
            if req.get("PrimaryLocationCountry") != "CL":
                # Sin detalle no se sabe si un remoto es postulable: no se avisa ni se
                # marca como visto, y se reintenta en la próxima corrida.
                logger.warning(f"Empleos PNUD {job_id}: detalle sin respuesta ({type(e).__name__}); se reintenta")
                fallas.append(f"detalle del puesto {job_id}")
                continue
            logger.warning(f"Empleos PNUD {job_id}: detalle sin respuesta ({type(e).__name__}); va sin cierre")
            det = {}
        if _postulable(req, det):
            items.append(_item(req, det))
    logger.info(f"Empleos PNUD: {len(items)} avisos (Chile + remotos)")
    return items, fallas
