"""Auditoría de keywords contra el universo real de Compra Ágil.

Responde UNA pregunta, con datos y no con supuestos: si el radar matcheara
también la descripción (y no solo el nombre), ¿cuántas oportunidades reales
ganaríamos y cuánta basura entraría al correo diario?

Hace falta porque las dos fuentes hoy matchean solo el título, y las
descripciones no están calibradas contra las keywords:
  - Las exclusiones ("compra de", "insumos", "materiales de") aparecen en casi
    cualquier descripción de Compra Ágil, así que aplicarlas ahí descartaría
    casi todo.
  - Las inclusiones anchas ("redacción", "encuesta", "infografía") son señal en
    un título, pero en una descripción larga aparecen de pasada.

Uso:
  # PowerShell — en la raíz del repo, con .venv activado y token cargado
  $env:MERCADO_PUBLICO_TOKEN = "tu-ticket"
  python -m src.audit_compra_agil            # ventana por defecto, hasta 300 detalles
  python -m src.audit_compra_agil 50         # muestra de 50 (más barato)

Costo de cuota: 1 request por página del listado (~16) + 1 por cada Compra Ágil
cuyo detalle se pide (ahí está la descripción). El tope es MAX_DETALLES. La
cuota es de 10.000/día por ticket, así que una corrida completa usa ~3%.

NO envía correo ni toca data/state.json. No corre en el cron: es manual.

Salida:
  data/audit-compra-agil-YYYY-MM-DD.csv

Cómo leerlo:
  Filtrar categoria=NUEVO_POR_DESCRIPCION y revisar a ojo cuántos sirven de
  verdad. Ese porcentaje es la decisión: si la mayoría es señal, conviene
  matchear la descripción; si es ruido, se queda como está. El log imprime
  además qué keywords traen esos candidatos — las que dominen la lista y no
  sirvan son las que habría que dejar fuera del match por descripción.
"""

import csv
import logging
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

from .sources.compra_agil import fetch_raw_publicadas, fetch_detalle
from .config import KEYWORDS_EXCLUDE, COMPRA_AGIL_WEB_URL_TEMPLATE, COMPRA_AGIL_DIAS_VENTANA
from .filters import _normalize, _EXCLUDE_NORM, _INCLUDE_NORM

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path("data")
MAX_DETALLES = 300  # tope de requests de detalle por corrida


def _exclusion(texto: str) -> str:
    """Primera keyword de exclusión que aparece en el texto, o '' si ninguna."""
    t = _normalize(texto)
    for i, kw_norm in enumerate(_EXCLUDE_NORM):
        if kw_norm in t:
            return KEYWORDS_EXCLUDE[i]
    return ""


def _inclusiones(texto: str) -> list[str]:
    """Keywords de inclusión presentes en el texto (sin aplicar exclusiones)."""
    t = _normalize(texto)
    return [kw_orig for kw_orig, kw_norm in _INCLUDE_NORM if kw_norm in t]


def _clasificar(nombre: str, descripcion: str) -> tuple[str, list[str], list[str], str]:
    """Retorna (categoria, kw_nombre, kw_desc_nuevas, motivo_exclusion_nombre).

    categoria ∈ {YA_MATCH_NOMBRE, EXCLUIDA_NOMBRE, NUEVO_POR_DESCRIPCION, SIN_MATCH}

    Replica el orden de matches_keywords (exclusión primero) sobre el NOMBRE,
    que es lo que hace el radar hoy. La descripción solo se usa para detectar
    qué entraría de nuevo.
    """
    motivo = _exclusion(nombre)
    kw_nombre = _inclusiones(nombre)
    kw_desc = _inclusiones(descripcion)
    # Lo que aporta la descripción y el nombre no tenía.
    kw_desc_nuevas = [k for k in kw_desc if k not in kw_nombre]

    if motivo:
        return "EXCLUIDA_NOMBRE", kw_nombre, kw_desc_nuevas, motivo
    if kw_nombre:
        return "YA_MATCH_NOMBRE", kw_nombre, kw_desc_nuevas, ""
    if kw_desc_nuevas:
        return "NUEVO_POR_DESCRIPCION", [], kw_desc_nuevas, ""
    return "SIN_MATCH", [], [], ""


def run(limite: int = MAX_DETALLES) -> int:
    logger.info(
        f"Descargando Compras Ágiles publicadas (ventana {COMPRA_AGIL_DIAS_VENTANA} días)…"
    )
    items = fetch_raw_publicadas()
    if not items:
        logger.error("No se recibió listado (revisa MERCADO_PUBLICO_TOKEN y la API v2)")
        return 1

    universo = len(items)
    a_revisar = items[:limite]
    if universo > limite:
        logger.warning(
            f"Universo de {universo:,}; se auditan solo los primeros {limite} "
            f"(tope MAX_DETALLES). Los {universo - limite:,} restantes NO se revisaron."
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fecha = datetime.now().strftime("%Y-%m-%d")
    out_path = OUTPUT_DIR / f"audit-compra-agil-{fecha}.csv"

    stats = Counter()
    kw_nuevas_hits = Counter()   # keywords que traen candidatos nuevos = ruido potencial
    excl_con_kw_desc = Counter() # excluidas por nombre pero con keyword en la descripción
    sin_detalle = 0

    with out_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        writer.writerow([
            "codigo", "categoria", "kw_nombre", "kw_descripcion_nuevas",
            "motivo_exclusion_nombre", "titulo", "descripcion",
            "organismo", "monto_clp", "fecha_cierre", "link",
        ])

        for i, item in enumerate(a_revisar, start=1):
            codigo = item.get("codigo") or ""
            nombre = item.get("nombre", "") or ""
            if not codigo:
                continue

            detalle = fetch_detalle(codigo)
            if detalle is None:
                sin_detalle += 1
                descripcion = ""
            else:
                descripcion = (detalle.get("descripcion") or "").strip()

            categoria, kw_nom, kw_desc, motivo = _clasificar(nombre, descripcion)
            stats[categoria] += 1
            if categoria == "NUEVO_POR_DESCRIPCION":
                for kw in kw_desc:
                    kw_nuevas_hits[kw] += 1
            elif categoria == "EXCLUIDA_NOMBRE" and kw_desc:
                # Caso clave: el nombre es genérico y cae por una exclusión
                # ("COMPRA INSUMOS 114219" cae por "insumos"), pero la descripción
                # sí habla de lo nuestro. Hoy se pierde, y matchear la descripción
                # NO lo rescataría: la exclusión sobre el nombre pega primero.
                excl_con_kw_desc[motivo] += 1

            fechas = item.get("fechas") or {}
            montos = item.get("montos") or {}
            institucion = item.get("institucion") or {}

            writer.writerow([
                codigo,
                categoria,
                "; ".join(kw_nom),
                "; ".join(kw_desc),
                motivo,
                nombre,
                " ".join(descripcion.split()),  # aplana saltos de línea para Excel
                institucion.get("organismo_comprador", ""),
                montos.get("monto_disponible_clp", ""),
                fechas.get("fecha_cierre", ""),
                COMPRA_AGIL_WEB_URL_TEMPLATE.format(codigo=codigo),
            ])

            if i % 50 == 0:
                logger.info(f"  {i}/{len(a_revisar)} detalles consultados…")

    total = sum(stats.values())
    if not total:
        logger.error("No se clasificó ninguna Compra Ágil")
        return 1

    nuevos = stats["NUEVO_POR_DESCRIPCION"]
    logger.info("=" * 62)
    logger.info(f"AUDITORÍA COMPRA ÁGIL {fecha}")
    logger.info("=" * 62)
    logger.info(f"Universo publicado en la ventana : {universo:,}")
    logger.info(f"Auditadas (con detalle)          : {total:,}")
    if sin_detalle:
        logger.warning(f"Sin descripción (detalle falló)  : {sin_detalle:,}")
    logger.info("")
    logger.info(f"  YA_MATCH_NOMBRE       : {stats['YA_MATCH_NOMBRE']:>5,}  (lo que el radar ya te manda)")
    logger.info(f"  NUEVO_POR_DESCRIPCION : {nuevos:>5,}  (lo que ganaríamos... y el ruido)")
    logger.info(f"  EXCLUIDA_NOMBRE       : {stats['EXCLUIDA_NOMBRE']:>5,}")
    logger.info(f"  SIN_MATCH             : {stats['SIN_MATCH']:>5,}")
    bloqueadas = sum(excl_con_kw_desc.values())
    if bloqueadas:
        logger.info(
            f"  De las EXCLUIDA_NOMBRE, {bloqueadas:,} tienen keyword en la descripción: "
            "nombre genérico que cae por exclusión, pero la descripción sí habla de lo tuyo."
        )
        logger.info("  Matchear la descripción NO las rescata — la exclusión pega antes:")
        for kw, n in excl_con_kw_desc.most_common(10):
            logger.info(f"    {n:>4}× excluidas por '{kw}'")

    logger.info("")
    if nuevos:
        proyeccion = nuevos / total * universo
        logger.info(
            f"Proyección a la ventana completa: ~{proyeccion:.0f} ítems nuevos por corrida. "
            "Si la mayoría es basura, NO conviene matchear descripción."
        )
        logger.info("")
        logger.info("Keywords que traen esos candidatos nuevos (sospechosas si dominan):")
        for kw, n in kw_nuevas_hits.most_common(15):
            logger.info(f"  {n:>4}× {kw}")
    else:
        logger.info("Ninguna Compra Ágil entraría por descripción en esta muestra.")

    logger.info("")
    logger.info(f"CSV generado: {out_path.resolve()}")
    logger.info(
        "Siguiente paso: abrir en Excel, filtrar categoria=NUEVO_POR_DESCRIPCION, "
        "leer la columna descripcion y marcar cuáles sirven de verdad."
    )
    return 0


if __name__ == "__main__":
    limite = int(sys.argv[1]) if len(sys.argv) > 1 else MAX_DETALLES
    sys.exit(run(limite))
