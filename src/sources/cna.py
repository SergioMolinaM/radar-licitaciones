"""CNA: aviso cuando se abre un llamado al Registro de Pares Evaluadores.

Pedido de David (16-oct-2026): saber cuándo se abre para postular. La CNA no tiene
RSS; el sitio es SharePoint y sus listas responden por API. Se miran dos:
- noticias (/noticias/Paginas): los llamados de 2015, 2016, 2017 y ene-2026 salieron
  como noticia («CNA busca pares evaluadores de pregrado», «CNA-Chile abre Concurso
  Público para integrar el Registro de Pares Evaluadores…»);
- archivos (/noticias/SiteAssets): las bases institucionales de dic-2015 y de 2020
  (el concurso que renovó el registro) están ahí y no tienen noticia.
Cursos, jornadas y talleres son para pares ya inscritos: no son llamados.
"""

import logging
import re
import tempfile
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote

import certifi
import requests

logger = logging.getLogger(__name__)

API = "https://www.cnachile.cl/noticias/_api/web/GetList('{lista}')/items?$select={campos}&$orderby=Created%20desc&$top=40"
LISTAS = (
    ("/noticias/Paginas", "Title,Created,ArticleStartDate,FileRef"),
    ("/noticias/SiteAssets", "Created,FileRef"),
)
TIMEOUT = 30
VENTANA_DIAS = 14  # solo lo reciente: el histórico no debe avisar como nuevo

_PARES = re.compile(r"\bpares\b|\bpar evaluador")  # «\bpar\b» calzaba «agencia par»
_LLAMADO = re.compile(r"concurso|convocatoria|convoca\b|postula|llamado|presentacion de antecedentes|busca par"
                      r"|integrar el registro|inscripcion|proceso de seleccion|invita a ser|\bbases\b|formulario")
# \bcurso: «concurso» no debe caer. «Formación virtual» (2017) fue un concurso real.
_NO_ES_LLAMADO = re.compile(r"\bcursos?\b|jornada|taller|planes? de formacion|programa de formacion|diplomado"
                            r"|capacitacion|webinar|encuentro|se suman|nombra|elegibles|admisibles|desiert"
                            r"|finaliz|resultado|seleccionad|nominad|termino (el )?periodo|cerrad|se cerro")

# cnachile.cl entrega solo su certificado, sin el intermedio (medido 17-oct-2026:
# openssl «unable to verify the first certificate»). Se agrega el intermedio público
# de DigiCert (vence 02-07-2030) a los raíces de certifi; no se apaga la verificación.
_INTERMEDIO = Path(__file__).parent / "certs" / "geotrust-ev-rsa-ca-g2.pem"


def _bundle() -> str:
    destino = Path(tempfile.gettempdir()) / "radar-cna-ca.pem"
    destino.write_text(Path(certifi.where()).read_text(encoding="utf-8") + "\n"
                       + _INTERMEDIO.read_text(encoding="utf-8"), encoding="utf-8")
    return str(destino)


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[-_]+", " ", s)


def es_convocatoria_pares(texto: str) -> bool:
    t = _norm(texto)
    return bool(_PARES.search(t) and _LLAMADO.search(t) and not _NO_ES_LLAMADO.search(t))


def _fecha(n: dict):
    """La más reciente entre creación y publicación; None si no hay fecha legible."""
    fechas = []
    for f in (n.get("Created"), n.get("ArticleStartDate")):
        try:
            d = datetime.fromisoformat(str(f).replace("Z", "+00:00"))
            fechas.append(d if d.tzinfo else d.replace(tzinfo=timezone.utc))
        except ValueError:
            continue
    return max(fechas) if fechas else None


def _aviso(n: dict, desde):
    ref = n.get("FileRef")
    if not isinstance(ref, str) or not ref:
        return None
    titulo = (n.get("Title") or "").strip() or ref.rsplit("/", 1)[-1]
    fecha = _fecha(n)
    if not fecha or fecha < desde or not es_convocatoria_pares(f"{titulo} {ref.rsplit('/', 1)[-1]}"):
        return None
    return {
        "id": "CNA:" + ref,
        "titulo": titulo,
        "fecha": fecha.strftime("%d/%m/%Y"),
        "link": "https://www.cnachile.cl" + quote(ref),
    }


def fetch_convocatorias_pares():
    """Devuelve (avisos, ok). ok=False si alguna lista no respondió. Nunca lanza:
    un fallo de la CNA no puede tumbar el correo de licitaciones."""
    desde = datetime.now(timezone.utc) - timedelta(days=VENTANA_DIAS)
    avisos, ok = [], True
    for lista, campos in LISTAS:
        try:
            resp = requests.get(
                API.format(lista=lista, campos=campos),
                headers={"Accept": "application/json;odata=nometadata", "User-Agent": "Mozilla/5.0"},
                timeout=TIMEOUT,
                verify=_bundle(),
            )
            resp.raise_for_status()
            items = resp.json()["value"]
            if not isinstance(items, list):
                raise ValueError("value no es lista")
        except Exception as e:  # red, SSL, JSON, disco: se informa como revisión parcial
            logger.error(f"CNA {lista}: sin respuesta ({e})")
            ok = False
            continue
        n_avisos = 0
        for n in items:
            try:
                a = _aviso(n, desde) if isinstance(n, dict) else None
            except Exception as e:
                logger.warning(f"CNA {lista}: entrada ilegible ({e})")
                continue
            if a:
                avisos.append(a)
                n_avisos += 1
        logger.info(f"CNA {lista}: {len(items)} leídas, {n_avisos} llamados a pares recientes")
    return avisos, ok
