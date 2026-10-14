"""Sonda de la API de Compra Ágil: qué consulta responde y cuál da 504.

Manual (workflow probe-compra-agil.yml), no envía correo ni toca data/.
Desde agosto 2026 el barrido diario cae con 504 (~29 s) en la página 1 con
estado+publicado_desde+ordenar_por+tamano_pagina=50. Esta sonda prueba
variantes de esos parámetros, dos rondas, y registra código, tiempo y
paginación de cada una. El ticket va solo en el header y nunca se imprime.

Uso: python -m src.probe_compra_agil
"""

import os
import sys
import time
from datetime import datetime, timedelta, timezone

import requests

from .config import COMPRA_AGIL_API_URL

TIMEOUT = 60


def _desde(dias: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=dias)).strftime("%Y-%m-%dT%H:%M:%SZ")


VARIANTES = [
    ("A actual (3 d, ordenar, 50)", {"estado": "publicada", "publicado_desde": _desde(3), "ordenar_por": "FechaPublicacion", "tamano_pagina": 50}),
    ("B 3 d, ordenar, 15", {"estado": "publicada", "publicado_desde": _desde(3), "ordenar_por": "FechaPublicacion", "tamano_pagina": 15}),
    ("C 3 d, sin ordenar, 50", {"estado": "publicada", "publicado_desde": _desde(3), "tamano_pagina": 50}),
    ("D 3 d, sin ordenar, 15", {"estado": "publicada", "publicado_desde": _desde(3), "tamano_pagina": 15}),
    ("E 1 d, sin ordenar, 50", {"estado": "publicada", "publicado_desde": _desde(1), "tamano_pagina": 50}),
    ("F solo estado, 15", {"estado": "publicada", "tamano_pagina": 15}),
    ("G sin filtros, 5", {"tamano_pagina": 5}),
]


def _probar(ticket: str, nombre: str, params: dict) -> None:
    params = {**params, "numero_pagina": 1}
    t0 = time.monotonic()
    try:
        resp = requests.get(COMPRA_AGIL_API_URL, headers={"ticket": ticket}, params=params, timeout=TIMEOUT)
    except requests.RequestException as e:
        print(f"{nombre:30} | error de red tras {time.monotonic() - t0:5.1f} s — {type(e).__name__}")
        return
    dt = time.monotonic() - t0
    detalle = ""
    if resp.status_code == 200:
        try:
            payload = resp.json().get("payload") or {}
            pag = payload.get("paginacion") or {}
            detalle = f"items={len(payload.get('items') or [])} paginacion={pag}"
        except ValueError:
            detalle = "JSON inválido"
    else:
        detalle = resp.text[:200].replace("\n", " ")
    print(f"{nombre:30} | HTTP {resp.status_code} | {dt:5.1f} s | {detalle}")


def main() -> int:
    ticket = os.getenv("MERCADO_PUBLICO_TOKEN")
    if not ticket:
        print("MERCADO_PUBLICO_TOKEN no configurado")
        return 1
    for ronda in (1, 2):
        print(f"--- ronda {ronda} ({datetime.now(timezone.utc):%H:%M:%S} UTC)")
        for nombre, params in VARIANTES:
            _probar(ticket, nombre, params)
            time.sleep(3)
    return 0


if __name__ == "__main__":
    sys.exit(main())
