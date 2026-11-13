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


_ROMANOS = {"i": 1, "ii": 2, "iii": 3}
_ENLACES_TIER = {"tier", "tiers", "and", "or", "&", ",", "/", "+", ":"}
_RANGO_TIER = {"-", "–", "—", "to", "through", "thru"}
# Palabras con que termina una cláusula restringida conocida. Cualquier otra palabra
# deja la cláusula como no entendida y el aviso pasa al correo (perder un aviso
# postulable es peor que mostrar uno que no lo es).
_FIN_TIER = {"applicants", "applicant", "only", "staff", "personnel"}
# «3 positions», «2 posts»: el número es de vacantes, no de tier, y cierra la cláusula.
_VACANTES = ("position", "post", "opening", "vacanc", "seat")


def _tiers(titulo: str) -> set[int] | None:
    """Tiers a los que el título restringe, o None si no restringe o no se entiende.
    Lee la cláusula desde la primera «tier» hasta el «)» o «]» que la cierra:
    «Tier 0, 1 & 2» -> {0,1,2}; «Tiers 1-3», «1 through 3» -> {1,2,3}; «Tier 1 & Tier 3»
    -> {1,3}; «Tier1», «Tier(s) 1 & 2», «Tier I & II». «external» o «above» en la
    cláusula -> incluye a los externos (Tier 3)."""
    t = titulo.replace("tier(s)", "tiers")
    m = re.search(r"\btiers?(?=[\s\-\d:]|$)[^)\]]*", t)
    if not m:
        return None
    tokens = re.findall(r"\d+|[a-z]+|[&,/+:\-–—]", m.group(0))
    if "external" in tokens or "above" in tokens:
        return {3}
    nums: list[int] = []
    rango = False
    for i, tok in enumerate(tokens):
        if tok in _ENLACES_TIER:
            continue
        if tok in _RANGO_TIER:
            rango = True
            continue
        if tok in _FIN_TIER:
            break
        n = int(tok) if tok.isdigit() else _ROMANOS.get(tok)
        if n is None:
            return None
        if i + 1 < len(tokens) and tokens[i + 1].startswith(_VACANTES):
            break
        if rango and nums:
            nums.extend(range(nums[-1] + 1, n + 1))
        else:
            nums.append(n)
        rango = False
    return set(nums) or None


def _postulable(req: dict, det: dict) -> bool:
    """Solo lo que un externo en Chile puede postular. Fuera, en todo país: lo restringido
    a personal interno (Tier 0, 1 y 2 sin Tier 3; el portal dice «Tier 3 or no tier
    indicated: … other external candidates»). Lo de Chile pasa en lo demás. Lo remoto,
    además, sin contratos nacionales de otro país, restringidos a nacionales ni pasantías.
    Medido el 26-oct-2026: de 7 remotos pasaba 1 (IPSA, abierto a externos)."""
    titulo = (req.get("Title") or "").lower()
    # «Open to Tier 0 & 1 & 2» pasaba con el antiguo «"tier 1" in titulo» (aviso 38051, 13-nov-2026).
    tiers = _tiers(titulo)
    if tiers is not None and 3 not in tiers:
        return False
    if req.get("PrimaryLocationCountry") == "CL":
        return True
    flex = {f.get("Prompt"): f.get("Value") for f in (det.get("requisitionFlexFields") or [])}
    tipo = (flex.get("Vacancy Type") or det.get("RequisitionType") or "").lower()
    # «intern» con borde de palabra: sin él, «Open to internal and external» quedaba fuera.
    if "nationals of" in titulo or re.search(r"\bintern(ship)?\b", titulo):
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
