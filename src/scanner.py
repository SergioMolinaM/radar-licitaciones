"""Orquestador del radar de licitaciones.

Flujo:
  1. Carga state.json (IDs ya notificados)
  2. Ejecuta cada fuente y reúne hits
  3. Filtra los ya vistos
  4. Notifica solo los nuevos
  5. Marca como vistos y guarda state.json
  6. Purga IDs antiguos (>90 días)
"""

import logging
import sys

from .sources.mercado_publico import fetch_licitaciones_dia
from .sources.undp import fetch_undp_notices
from .state import load_state, save_state, is_new, mark_seen, prune_state
from .notifier import send_email

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def run() -> int:
    state = load_state()

    todos = []
    todos.extend(fetch_licitaciones_dia())
    todos.extend(fetch_undp_notices())

    logger.info(f"Total bruto tras filtros de keywords: {len(todos)}")

    nuevos = [item for item in todos if is_new(state, item["id"])]
    logger.info(f"Nuevos (no notificados previamente): {len(nuevos)}")

    enviado = send_email(nuevos)
    if not enviado:
        logger.error("Notificación falló — no se actualiza state")
        return 1

    for item in nuevos:
        mark_seen(state, item["id"])

    prune_state(state)
    save_state(state)
    logger.info("State guardado correctamente")
    return 0


if __name__ == "__main__":
    sys.exit(run())
