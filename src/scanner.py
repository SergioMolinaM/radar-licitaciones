"""Orquestador del radar de licitaciones.

Flujo:
  1. Carga state.json (IDs ya notificados)
  2. Ejecuta cada fuente y reune hits
  3. Filtra los ya vistos
  4. Notifica solo los nuevos
  5. Marca como vistos y guarda state.json
  6. Purga IDs antiguos (>90 dias)
  7. Si es viernes: envia heartbeat semanal de estado
"""

import logging
import sys
from datetime import datetime, timedelta, timezone

from .sources.mercado_publico import fetch_licitaciones_dia
from .sources.compra_agil import fetch_compra_agil
from .sources.undp import fetch_undp_notices
from .sources.cna import fetch_convocatorias_pares
from .state import load_state, save_state, is_new, mark_seen, prune_state, _parse_iso
from .notifier import send_email, send_heartbeat, send_aviso_cna, send_aviso_cna_extra, destinatarios_cna_extra

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

HEARTBEAT_WEEKDAY = 4  # 0=lunes ... 4=viernes (UTC). Cron corre 12:00 UTC L-V.


def _weekly_stats(state, universo_mp, universo_ca, universo_undp, matches_totales_hoy, nuevos_hoy):
    hace_7d = datetime.utcnow() - timedelta(days=7)
    seen = state.get("seen", {})
    nuevos_semana = 0
    for _id, ts in seen.items():
        if _id.startswith(("CNA:", "extra:")):  # avisos CNA: no son oportunidades
            continue
        dt = _parse_iso(ts)
        if dt and dt >= hace_7d:
            nuevos_semana += 1
    return {
        "universo_mp": universo_mp,
        "universo_ca": universo_ca,
        "universo_undp": universo_undp,
        "matches_totales_hoy": matches_totales_hoy,
        "nuevos_hoy": nuevos_hoy,
        "nuevos_semana": nuevos_semana,
        "total_seen": len(seen),
    }


def run() -> int:
    state = load_state()

    matches_mp, universo_mp = fetch_licitaciones_dia()
    matches_ca, resumen_ca = fetch_compra_agil(cursor=state.get("ca_cursor", 0), ultima=state.get("ca_ultima"))
    state["ca_cursor"] = resumen_ca["cursor"]
    state["ca_ultima"] = resumen_ca["ultima"]
    universo_ca = resumen_ca["devueltas"]
    matches_undp, universo_undp = fetch_undp_notices()
    try:
        avisos_cna, cna_ok = fetch_convocatorias_pares()
    except Exception:
        logger.exception("Noticias CNA: error inesperado")
        avisos_cna, cna_ok = [], False
    todos = matches_mp + matches_ca + matches_undp

    logger.info(f"Universo escaneado: MP={universo_mp}, CA devueltas={universo_ca}, PNUD={universo_undp}")
    logger.info(f"Total tras filtro keywords: {len(todos)}")

    # Universo 0 nunca es real en MP (~4.000 activas) ni en PNUD: es una fuente
    # caída. Compra Ágil se busca por término (`q`) y una búsqueda puede volver
    # vacía de verdad: se da por caída solo si ningún término diario respondió.
    caidas = [nombre for nombre, universo in
              (("Mercado Público", universo_mp), ("PNUD", universo_undp))
              if universo == 0]
    if not resumen_ca["diarios_ok"]:
        caidas.append("Compra Ágil" + (f" ({resumen_ca['cortado']})" if resumen_ca["cortado"] else ""))
    # Cobertura parcial: va en el aviso del correo, pero no pone la corrida en
    # rojo (con la API lenta pasaría casi todos los días y el rojo dejaría de avisar).
    parciales = []
    if resumen_ca["diarios_ok"]:
        if resumen_ca["diarios_fallidos"]:
            parciales.append("Compra Ágil sin respuesta para: " + ", ".join(resumen_ca["diarios_fallidos"])
                             + " (lo que calce solo con esos términos no aparece hoy; se busca de nuevo"
                               " en la próxima corrida desde la última búsqueda exitosa)")
        if resumen_ca["cortado"]:
            parciales.append(f"Compra Ágil cortada ({resumen_ca['cortado']}): los términos rotativos"
                             " que faltaban se buscan en la próxima corrida")
    if resumen_ca["truncados"]:
        parciales.append("Compra Ágil con más de 250 resultados para: " + ", ".join(resumen_ca["truncados"])
                         + " (aparecen los primeros 250; pueden faltar los siguientes)")
    if not cna_ok:
        parciales.append("Noticias de la CNA sin respuesta: hoy no se revisó si abrió un llamado a pares evaluadores")
    if caidas:
        logger.error(f"Fuentes caídas en esta corrida: {', '.join(caidas)}")

    nuevos = [item for item in todos if is_new(state, item["id"])]
    logger.info(f"Nuevos (no notificados previamente): {len(nuevos)}")

    enviado = send_email(nuevos, caidas, parciales)
    if not enviado:
        logger.error("Notificacion fallo - no se actualiza state")
        return 1

    for item in nuevos:
        mark_seen(state, item["id"])

    # Llamado a pares de la CNA: correo aparte a RADAR_TO_EMAIL y a RADAR_CNA_TO
    # (David), cada uno marcado por separado para no repetirle a nadie. Lo que falla
    # se reintenta mientras siga en la ventana de 14 días. Nada de esto puede
    # impedir que se guarde el state de las licitaciones ya notificadas.
    try:
        fallo_extra = False
        if destinatarios_cna_extra():
            extra = [a for a in avisos_cna if is_new(state, "extra:" + a["id"])]
            if extra:
                if send_aviso_cna_extra(extra):
                    for a in extra:
                        mark_seen(state, "extra:" + a["id"])
                else:
                    fallo_extra = True
        principal = [a for a in avisos_cna if is_new(state, a["id"])]
        if principal and send_aviso_cna(principal, fallo_extra):
            for a in principal:
                mark_seen(state, a["id"])
    except Exception:
        logger.exception("Aviso CNA: error inesperado; se sigue sin él")

    prune_state(state)
    save_state(state)
    logger.info("State guardado correctamente")

    # Heartbeat semanal (viernes UTC): confirma que el sistema respira aunque
    # no haya oportunidades nuevas. Distingue "silencio real" de "sistema roto".
    if datetime.now(timezone.utc).weekday() == HEARTBEAT_WEEKDAY:
        stats = _weekly_stats(state, universo_mp, universo_ca, universo_undp, len(todos), len(nuevos))
        stats["caidas"] = caidas
        stats["parciales"] = parciales
        stats["ca_terminos"] = (
            f"{len(resumen_ca['diarios_ok'])}/{len(resumen_ca['diarios_ok']) + len(resumen_ca['diarios_fallidos'])} diarios, "
            f"{len(resumen_ca['rotativos_ok'])} de {resumen_ca['rotativos_total']} rotativos"
        )
        send_heartbeat(stats)

    # State ya guardado: salir con error deja la corrida en rojo en GitHub
    # Actions (que avisa por correo) sin perder lo notificado.
    if caidas:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(run())
