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
    # 14-oct, ronda sin q: A-F tardaron 23-29 s y cayeron en 504 al pasar 29 s, sea cual
    # fuera el tamaño de página, el orden o la ventana; tamano_pagina < 10 da 400.
    # q: palabras clave en nombre/descripción, filtradas en el servidor (guía §5.1 Grupo 5).
    ("Q1 q=IA, 3 d, 50", {"q": "inteligencia artificial", "estado": "publicada", "publicado_desde": _desde(3), "tamano_pagina": 50}),
    ("Q2 q=capacitación, 3 d, 50", {"q": "capacitación", "estado": "publicada", "publicado_desde": _desde(3), "tamano_pagina": 50}),
    ("Q3 q=sitio web, solo estado, 50", {"q": "sitio web", "estado": "publicada", "tamano_pagina": 50}),
    ("Q4 q=encuesta, 3 d, ordenar, 50", {"q": "encuesta", "estado": "publicada", "publicado_desde": _desde(3), "ordenar_por": "FechaPublicacion", "tamano_pagina": 50}),
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
            items = payload.get("items") or []
            nombres = "; ".join((i.get("nombre") or "")[:40] for i in items[:3])
            detalle = f"items={len(items)} paginacion={pag} | {nombres}"
        except ValueError:
            detalle = "JSON inválido"
    else:
        detalle = resp.text[:200].replace("\n", " ")
    print(f"{nombre:30} | HTTP {resp.status_code} | {dt:5.1f} s | {detalle}")


# 16-oct: ¿q calza la frase, todas las palabras o cualquiera? El buscador público
# dio «sitio web» 15, «página web» 12, «portal web» 128: sugiere «cualquiera».
# Si «web» sola contiene a las cinco frases web, una consulta reemplaza cinco.
SEMANTICA = ["web", "sitio web", "página web", "portal web", "plataforma web", "diseño web", "sitio", "portal"]


def _codigos(ticket: str, termino: str, desde: str) -> set[str] | None:
    codigos: set[str] = set()
    for pagina in range(1, 6):
        params = {"q": termino, "estado": "publicada", "publicado_desde": desde, "tamano_pagina": 50, "numero_pagina": pagina}
        resp = None
        for _ in range(3):
            try:
                resp = requests.get(COMPRA_AGIL_API_URL, headers={"ticket": ticket}, params=params, timeout=TIMEOUT)
            except requests.RequestException:
                resp = None
            if resp is not None and resp.status_code == 200:
                break
            time.sleep(5)
        if resp is None or resp.status_code != 200:
            return None
        payload = resp.json().get("payload") or {}
        items = payload.get("items") or []
        codigos |= {i.get("codigo") for i in items if i.get("codigo")}
        if len(items) < 50:
            return codigos
    print(f"  {termino!r}: más de 5 páginas, conjunto truncado")
    return codigos


def semantica(ticket: str) -> None:
    desde = _desde(7)
    print(f"--- semántica de q, publicadas desde {desde}")
    res = {}
    for t in SEMANTICA:
        res[t] = _codigos(ticket, t, desde)
        print(f"{t:16} | {'sin respuesta' if res[t] is None else len(res[t])}")
    w = res.get("web")
    if w is None:
        print("«web» sin respuesta: no se puede concluir")
        return
    for t in SEMANTICA[1:6]:
        if res[t] is not None:
            print(f"{t:16} ⊆ web: {res[t] <= w} (fuera de web: {len(res[t] - w)})")
    for frase, palabra in (("sitio web", "sitio"), ("portal web", "portal")):
        f, p = res.get(frase), res.get(palabra)
        if f is not None and p is not None:
            print(f"{frase!r} = {palabra!r} ∪ web: {f == (p | w)}; = ∩: {f == (p & w)}")


def main() -> int:
    ticket = os.getenv("MERCADO_PUBLICO_TOKEN")
    if not ticket:
        print("MERCADO_PUBLICO_TOKEN no configurado")
        return 1
    semantica(ticket)
    for ronda in (1, 2):
        print(f"--- ronda {ronda} ({datetime.now(timezone.utc):%H:%M:%S} UTC)")
        for nombre, params in VARIANTES:
            _probar(ticket, nombre, params)
            time.sleep(3)
    return 0


if __name__ == "__main__":
    sys.exit(main())
