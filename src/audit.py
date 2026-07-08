"""Auditoría de keywords contra el universo real de Mercado Público.

Uso:
  # PowerShell — en la raíz del repo, con .venv activado y token cargado
  $env:MERCADO_PUBLICO_TOKEN = "tu-ticket"
  python -m src.audit

Salida:
  data/audit-YYYY-MM-DD.csv  — todas las licitaciones activas de MP, con marca
                               de si matchearon las keywords actuales y con
                               cuáles. Sin filtrar por PNUD (foco: Chile).

Objetivo:
  Detectar formulaciones que se están escapando ("asesoría comunicacional
  integral" en vez de "comunicación estratégica"). Se revisa manualmente el
  CSV en Excel filtrando por matched=FALSE y ordenando por título.
"""

import csv
import logging
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

from .sources.mercado_publico import fetch_raw_activas
from .filters import matches_keywords
from .config import KEYWORDS_INCLUDE, KEYWORDS_EXCLUDE

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path("data")


def _classify(nombre: str) -> tuple[str, str, str]:
    """Retorna (estado, keywords_match, motivo_exclusion) para una licitación.

    estado ∈ {'MATCH', 'EXCLUIDA', 'SIN_MATCH'}
    """
    if not nombre:
        return "SIN_MATCH", "", ""

    from .filters import _normalize, _EXCLUDE_NORM, _INCLUDE_NORM
    t = _normalize(nombre)

    # Detectar exclusión primero (mismo orden que matches_keywords)
    for kw_norm in _EXCLUDE_NORM:
        if kw_norm in t:
            # Recuperar la forma original
            idx = _EXCLUDE_NORM.index(kw_norm)
            return "EXCLUIDA", "", KEYWORDS_EXCLUDE[idx]

    encontradas = [kw_orig for kw_orig, kw_norm in _INCLUDE_NORM if kw_norm in t]
    if encontradas:
        return "MATCH", "; ".join(encontradas), ""
    return "SIN_MATCH", "", ""


def run() -> int:
    logger.info("Descargando universo activo de Mercado Público…")
    listado = fetch_raw_activas()
    if not listado:
        logger.error("No se recibió listado (revisa MERCADO_PUBLICO_TOKEN)")
        return 1

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fecha = datetime.now().strftime("%Y-%m-%d")
    out_path = OUTPUT_DIR / f"audit-{fecha}.csv"

    stats = Counter()
    kw_hits = Counter()
    excl_hits = Counter()

    with out_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        writer.writerow([
            "codigo", "estado_filtro", "keywords_match", "motivo_exclusion",
            "titulo", "fecha_cierre", "link"
        ])
        for lic in listado:
            codigo = lic.get("CodigoExterno") or ""
            nombre = lic.get("Nombre", "") or ""
            fecha_cierre = lic.get("FechaCierre", "") or ""
            link = (
                f"https://www.mercadopublico.cl/Procurement/Modules/RFB/"
                f"DetailsAcquisition.aspx?idlicitacion={codigo}"
            )
            estado, kws, motivo = _classify(nombre)
            stats[estado] += 1
            if estado == "MATCH":
                for kw in kws.split("; "):
                    kw_hits[kw] += 1
            elif estado == "EXCLUIDA":
                excl_hits[motivo] += 1
            writer.writerow([codigo, estado, kws, motivo, nombre, fecha_cierre, link])

    total = sum(stats.values())
    logger.info("=" * 60)
    logger.info(f"AUDITORÍA {fecha} — universo Mercado Público")
    logger.info("=" * 60)
    logger.info(f"Total licitaciones activas escaneadas: {total:,}")
    logger.info(f"  MATCH       : {stats['MATCH']:>6,}  ({stats['MATCH']/total*100:.1f}%)")
    logger.info(f"  EXCLUIDA    : {stats['EXCLUIDA']:>6,}  ({stats['EXCLUIDA']/total*100:.1f}%)")
    logger.info(f"  SIN_MATCH   : {stats['SIN_MATCH']:>6,}  ({stats['SIN_MATCH']/total*100:.1f}%)")
    logger.info("")
    logger.info("Top 15 keywords de inclusión que atraparon:")
    for kw, n in kw_hits.most_common(15):
        logger.info(f"  {n:>4}× {kw}")
    logger.info("")
    logger.info("Top 10 keywords de exclusión que descartaron:")
    for kw, n in excl_hits.most_common(10):
        logger.info(f"  {n:>4}× {kw}")
    logger.info("")
    logger.info(f"CSV generado: {out_path.resolve()}")
    logger.info(
        "Siguiente paso: abrir en Excel, filtrar estado_filtro=SIN_MATCH, "
        "ordenar por titulo y detectar formulaciones a agregar al filtro."
    )
    return 0


if __name__ == "__main__":
    sys.exit(run())
