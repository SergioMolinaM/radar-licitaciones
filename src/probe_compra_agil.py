"""Sonda de la API de Compra Ágil: qué consulta responde y cuál da 504.

Manual (workflow probe-compra-agil.yml), no envía correo ni toca data/.
Desde agosto 2026 el barrido diario cae con 504 (~29 s) en la página 1 con
estado+publicado_desde+ordenar_por+tamano_pagina=50. Esta sonda prueba
variantes de esos parámetros, dos rondas, y registra código, tiempo y
paginación de cada una. El ticket va solo en el header y nunca se imprime.

Uso: python -m src.probe_compra_agil            (alternativas a los diarios que dan 504)
     python -m src.probe_compra_agil --variantes (sondas del 14 y 16-oct)
     python -m src.probe_compra_agil --paginacion (listado sin q, todas las páginas de 1 día)
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


# 28-oct (run 40741312235): de las palabras sueltas de los cuatro diarios que dan
# 504 respondieron «web» (2 de 2 rondas), «digital» y «audiovisual» (1 de 2);
# «diseño», «redes», «sociales», «marketing» y «producción», 504 en las dos.
# 29-oct: ¿qué término trae redes sociales, marketing y difusión? «web» va de
# control positivo, «redes sociales» de control negativo, y al final el listado
# sin q de 1 día, por si cabe en 29 s.
ALTERNATIVAS = [
    "web", "redes sociales",
    "publicidad", "difusión", "comunicaciones", "comunicación", "contenidos",
    "community", "campaña", "fotografía", "video", "gráfico",
]


def alternativas(ticket: str) -> None:
    desde = _desde(3)
    for ronda in (1, 2):
        print(f"--- alternativas, ronda {ronda} ({datetime.now(timezone.utc):%H:%M:%S} UTC), desde {desde}")
        for t in ALTERNATIVAS:
            _probar(ticket, f"q={t}", {"q": t, "estado": "publicada", "publicado_desde": desde, "tamano_pagina": 50})
            time.sleep(5)
        _probar(ticket, "sin q, 1 d", {"estado": "publicada", "publicado_desde": _desde(1), "tamano_pagina": 50})
        time.sleep(5)


# 30-oct (run 41078223545): el listado sin q de 1 día respondió en 3-4 s en las dos
# rondas (3.040 resultados, 61 páginas); el 14-oct el de 3 días caía en 504. Si todas
# las páginas responden, se puede bajar todo y filtrar local en vez de 140 términos q.
# Esta sonda recorre todas las páginas: código, tiempo, ítems y códigos únicos.
def paginacion(ticket: str, dias: int = 1, pausa: float = 5) -> None:
    desde = _desde(dias)
    print(f"--- paginación sin q, {dias} d ({datetime.now(timezone.utc):%H:%M:%S} UTC), desde {desde}")
    codigos, total, pagina, fallas, t_inicio = set(), None, 1, 0, time.monotonic()
    while total is None or pagina <= total:
        params = {"estado": "publicada", "publicado_desde": desde, "tamano_pagina": 50, "numero_pagina": pagina}
        t0 = time.monotonic()
        try:
            resp = requests.get(COMPRA_AGIL_API_URL, headers={"ticket": ticket}, params=params, timeout=TIMEOUT)
        except requests.RequestException as e:
            print(f"pág {pagina:3} | error de red tras {time.monotonic() - t0:5.1f} s — {type(e).__name__}")
            fallas += 1
            pagina += 1
            continue
        dt = time.monotonic() - t0
        if resp.status_code == 200:
            payload = resp.json().get("payload") or {}
            pag = payload.get("paginacion") or {}
            total = total or pag.get("total_paginas") or 0
            items = payload.get("items") or []
            codigos |= {i.get("codigo") for i in items}
            print(f"pág {pagina:3}/{total} | HTTP 200 | {dt:5.1f} s | items={len(items)} total_resultados={pag.get('total_resultados')}")
        else:
            fallas += 1
            print(f"pág {pagina:3} | HTTP {resp.status_code} | {dt:5.1f} s | {resp.text[:120]!r} | Retry-After={resp.headers.get('Retry-After')}")
            if resp.status_code == 429:
                print("429: se detiene")
                break
            if total is None:
                total = 1  # sin la primera página no se sabe cuántas hay
        pagina += 1
        time.sleep(pausa)
    print(f"--- fin: {pagina - 1} páginas pedidas, {fallas} fallas, {len(codigos)} códigos únicos, "
          f"{time.monotonic() - t_inicio:.0f} s")


def main() -> int:
    ticket = os.getenv("MERCADO_PUBLICO_TOKEN")
    if not ticket:
        print("MERCADO_PUBLICO_TOKEN no configurado")
        return 1
    if "--paginacion" in sys.argv:
        paginacion(ticket, dias=1)
        return 0
    if "--variantes" in sys.argv:
        semantica(ticket)
        for ronda in (1, 2):
            print(f"--- ronda {ronda} ({datetime.now(timezone.utc):%H:%M:%S} UTC)")
            for nombre, params in VARIANTES:
                _probar(ticket, nombre, params)
                time.sleep(3)
        return 0
    alternativas(ticket)
    return 0


if __name__ == "__main__":
    sys.exit(main())
