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
from .sources.undp import fetch_undp_notices
from .state import load_state, save_state, is_new, mark_seen, prune_state, _parse_iso
from .notifier import send_email, send_heartbeat

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

HEARTBEAT_WEEKDAY = 4  # 0=lunes ... 4=viernes (UTC). Cron corre 12:00 UTC L-V.


def _weekly_stats(state, universo_mp, universo_undp, matches_totales_hoy, nuevos_hoy):
    hace_7d = datetime.utcnow() - timedelta(days=7)
    seen = state.get("seen", {})
    nuevos_semana = 0
    for _id, ts in seen.items():
        dt = _parse_iso(ts)
        if dt and dt >= hace_7d:
            nuevos_semana += 1
    return {
        "universo_mp": universo_mp,
        "universo_undp": universo_undp,
        "matches_totales_hoy": matches_totales_hoy,
        "nuevos_hoy": nuevos_hoy,
        "nuevos_semana": nuevos_semana,
        "total_seen": len(seen),
    }


def run() -> int:
    state = load_state()

    matches_mp, universo_mp = fetch_licitaciones_dia()
    matches_undp, universo_undp = fetch_undp_notices()
    todos = matches_mp + matches_undp

    logger.info(f"Universo escaneado: MP={universo_mp}, PNUD={universo_undp}")
    logger.info(f"Total tras filtro keywords: {len(todos)}")

    nuevos = [item for item in todos if is_new(state, item["id"])]
    logger.info(f"Nuevos (no notificados previamente): {len(nuevos)}")

    enviado = send_email(nuevos)
    if not enviado:
        logger.error("Notificacion fallo - no se actualiza state")
        return 1

    for item in nuevos:
        mark_seen(state, item["id"])

    prune_state(state)
    save_state(state)
    logger.info("State guardado correctamente")

    # Heartbeat semanal (viernes UTC): confirma que el sistema respira aunque
    # no haya oportunidades nuevas. Distingue "silencio real" de "sistema roto".
    if datetime.now(timezone.utc).weekday() == HEARTBEAT_WEEKDAY:
        stats = _weekly_stats(state, universo_mp, universo_undp, len(todos), len(nuevos))
        send_heartbeat(stats)

    return 0


if __name__ == "__main__":
    sys.exit(run())
