"""Persistencia del estado: IDs de licitaciones ya notificadas."""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta

STATE_PATH = Path("data/state.json")
RETENTION_DAYS = 90  # Purga IDs vistos hace más de 90 días


def load_state() -> dict:
    """Carga el state.json. Si no existe, retorna estado vacío."""
    if not STATE_PATH.exists():
        return {"seen": {}}
    try:
        with STATE_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"seen": {}}


def save_state(state: dict) -> None:
    """Guarda el state.json en disco, atómico: escribe a un temporal y lo
    reemplaza. El workflow commitea con if: always(); un JSON a medio escribir
    se cargaría como vacío y reenviaría 90 días de avisos."""
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_PATH.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2, sort_keys=True)
    os.replace(tmp, STATE_PATH)


def is_new(state: dict, item_id: str) -> bool:
    """Determina si un ID es nuevo (no notificado)."""
    return item_id not in state.get("seen", {})


def mark_seen(state: dict, item_id: str) -> None:
    """Marca un ID como notificado con timestamp."""
    state.setdefault("seen", {})[item_id] = datetime.utcnow().isoformat()


def prune_state(state: dict) -> None:
    """Elimina IDs vistos hace más de RETENTION_DAYS días."""
    cutoff = datetime.utcnow() - timedelta(days=RETENTION_DAYS)
    seen = state.get("seen", {})
    pruned = {
        k: v
        for k, v in seen.items()
        if _parse_iso(v) and _parse_iso(v) > cutoff
    }
    state["seen"] = pruned


def _parse_iso(s: str):
    try:
        return datetime.fromisoformat(s)
    except (ValueError, TypeError):
        return None
