"""CNA: aviso cuando se abre un llamado al Registro de Pares Evaluadores.

Pedido de David (16-oct-2026): saber cuándo se abre para postular. La CNA no tiene
RSS. Desde el 26-nov-2026 el sitio es WordPress (antes SharePoint: las listas
/noticias/Paginas y /noticias/SiteAssets dan 404 y /noticias/Paginas/default.aspx
redirige a /noticias/). Se miran dos colecciones de la API pública wp-json:
- entradas (/wp/v2/posts): en SharePoint los llamados de 2015, 2016, 2017 y ene-2026
  salieron como noticia; en WordPress la entrada más antigua es de jul-2020 y está la
  del 16-01-2026 («CNA-Chile abre Concurso Público para integrar el Registro de Pares
  Evaluadores…», id 739; verificador, 27-11-2026);
- archivos (/wp/v2/media): en SharePoint las bases de dic-2015 y de 2020 se subieron
  sin noticia. En WordPress no están (verificador, 27-11), pero un llamado nuevo puede
  volver a salir así, también colgado de una página o de un tipo propio del sitio
  (`documento`, `investigacion`…: 432 de los 709 archivos con `post`). Solo se salta el
  archivo cuya entrada ya avisó en la misma corrida, para no avisar dos veces.
Cursos, jornadas y talleres son para pares ya inscritos: no son llamados. Las páginas
de WordPress sobre el registro (ids 1926, 1438, 1010) no se miran, igual que antes.
"""

import html
import logging
import re
import socket
import ssl
import tempfile
import unicodedata
import warnings
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import unquote

import certifi
import requests

logger = logging.getLogger(__name__)

# Solo lo publicado dentro de la ventana (after=), paginado de a 100 (máximo de WordPress). La migración
# subió hasta 2.976 archivos en un día y el lunes junta tres días: 40 sin paginar dejaba bases sin ver
# (verificador, 27-11-2026: 132 archivos en la ventana, el último en la posición 139).
API = ("https://www.cnachile.cl/wp-json/wp/v2/{coleccion}?per_page=100&page={pagina}&after={desde}"
       "&orderby=date&order=desc&_fields={campos}")
MAX_PAGINAS = 30  # 3.000 ítems; si no alcanza, la revisión queda parcial (ok=False)
LISTAS = (
    ("posts", "id,date,date_gmt,link,title"),
    ("media", "id,date,date_gmt,source_url,title,post"),
)
# La carpeta /uploads/AAAA/MM/ es casi siempre el mes de subida (4.370 de 4.509 archivos, verificador
# 27-11), pero la migración dejó algunos con subida 26-11 en una carpeta anterior
# (RESOLUCION-EXENTA-RACL-N°0113-26 en /uploads/2026/10/). Se toma la fecha más antigua de las dos. No
# protege de un archivo histórico subido de nuevo hoy: ese avisaría (ruido del lado seguro).
_CARPETA = re.compile(r"/wp-content/uploads/(\d{4})/(\d{2})/")
_DOMINIO = re.compile(r"^https://(www\.)?cnachile\.cl/")
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
# openssl «unable to verify the first certificate»). Se agregan intermedios a los raíces
# de certifi; no se apaga la verificación. El 20-oct-2026 la CNA renovó con otro emisor
# (GeoTrust EV RSA CA G2 → Thawte TLS RSA CA G1) y el aviso se cayó: por eso cada corrida
# baja además el intermedio que el propio certificado anuncia (AIA, caIssuers). Los
# guardados en certs/ quedan de respaldo si esa descarga falla.
_CERTS = Path(__file__).parent / "certs"
_HOST = "www.cnachile.cl"


def _intermedio_aia(raices_pem: str) -> str:
    """PEM del emisor anunciado por el certificado de la CNA, o "" si no se pudo.
    La hoja y la URL vienen de la red sin verificar: todo lo que esté en el CAfile cuenta
    como raíz para OpenSSL, así que un autofirmado bajado por http abriría la puerta a un
    MITM (medido por el verificador, 30-oct-2026). Por eso el certificado bajado solo entra
    si es CA, no es autofirmado y lo firma directamente una raíz de certifi."""
    try:
        from cryptography import x509
        from cryptography.hazmat.primitives import serialization
        from cryptography.x509.oid import AuthorityInformationAccessOID

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with socket.create_connection((_HOST, 443), timeout=TIMEOUT) as s:
            with ctx.wrap_socket(s, server_hostname=_HOST) as ss:
                hoja = x509.load_der_x509_certificate(ss.getpeercert(binary_form=True))
        aia = hoja.extensions.get_extension_for_class(x509.AuthorityInformationAccess).value
        url = next(d.access_location.value for d in aia
                   if d.access_method == AuthorityInformationAccessOID.CA_ISSUERS)
        resp = requests.get(url, timeout=TIMEOUT)
        resp.raise_for_status()
        datos = resp.content
        cert = (x509.load_pem_x509_certificate(datos) if datos.lstrip().startswith(b"-----BEGIN")
                else x509.load_der_x509_certificate(datos))
        if cert.issuer == cert.subject:
            raise ValueError("autofirmado")
        if not cert.extensions.get_extension_for_class(x509.BasicConstraints).value.ca:
            raise ValueError("no es CA")
        # Una a una: certifi trae una raíz con serie no positiva que cryptography anuncia
        # que dejará de cargar, y cargarlas juntas haría caer todas por esa.
        for bloque in re.findall(r"-----BEGIN CERTIFICATE-----.+?-----END CERTIFICATE-----", raices_pem, re.S):
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    raiz = x509.load_pem_x509_certificate(bloque.encode("ascii"))
                if raiz.subject != cert.issuer:
                    continue
                cert.verify_directly_issued_by(raiz)
            except Exception:
                continue
            return cert.public_bytes(serialization.Encoding.PEM).decode("ascii")
        raise ValueError("no lo firma ninguna raíz de certifi")
    except Exception as e:
        logger.warning(f"CNA: intermedio por AIA descartado ({e}); se usan los de certs/")
        return ""


def _bundle() -> str:
    raices = Path(certifi.where()).read_text(encoding="utf-8")
    partes = [raices]
    for p in sorted(_CERTS.glob("*.pem")):
        try:
            texto = p.read_text(encoding="utf-8")
            from cryptography import x509
            x509.load_pem_x509_certificates(texto.encode("utf-8"))  # un bloque roto tumba el bundle entero
            partes.append(texto)
        except Exception as e:
            logger.warning(f"CNA: {p.name} ilegible ({e})")
    partes.append(_intermedio_aia(raices))
    destino = Path(tempfile.gettempdir()) / "radar-cna-ca.pem"
    destino.write_text("\n".join(partes), encoding="utf-8")
    return str(destino)


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[-_]+", " ", s)


def es_convocatoria_pares(texto: str) -> bool:
    t = _norm(texto)
    return bool(_PARES.search(t) and _LLAMADO.search(t) and not _NO_ES_LLAMADO.search(t))


def _fecha(n: dict, link: str):
    """Fecha de publicación (date_gmt, UTC); en archivos, acotada al fin del mes de su carpeta.
    None si no hay fecha legible."""
    try:
        d = datetime.fromisoformat(str(n.get("date_gmt")).replace("Z", "+00:00"))
    except ValueError:
        return None
    d = d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    m = _CARPETA.search(link)
    if m:
        anio, mes = int(m.group(1)), int(m.group(2))
        if 1 <= mes <= 12 and 1 <= anio < 9999:
            sig = datetime(anio + (mes == 12), mes % 12 + 1, 1, tzinfo=timezone.utc)
            d = min(d, sig - timedelta(seconds=1))
    return d


def _fecha_chile(d: datetime) -> str:
    """dd/mm/aaaa en hora de Chile. El campo `date` de WordPress no sirve: el sitio está en
    Europe/Madrid (gmt_offset 1, verificador 27-11). Sin base de zonas horarias, la UTC."""
    try:
        from zoneinfo import ZoneInfo
        d = d.astimezone(ZoneInfo("America/Santiago"))
    except Exception:
        pass
    return d.strftime("%d/%m/%Y")


def _titulo(n: dict) -> str:
    t = n.get("title")
    t = t.get("rendered") if isinstance(t, dict) else t
    return html.unescape(re.sub(r"<[^>]+>", "", t or "")).strip()


def _aviso(n: dict, desde, avisadas=frozenset()):
    if n.get("post") and n.get("post") in avisadas:  # su entrada ya avisó en esta corrida
        return None
    link = n.get("link") or n.get("source_url")
    if not isinstance(link, str) or not _DOMINIO.match(link):
        return None
    archivo = unquote(link.rstrip("/").rsplit("/", 1)[-1])
    titulo = _titulo(n) or archivo
    fecha = _fecha(n, link)
    if not fecha or fecha < desde or not es_convocatoria_pares(f"{titulo} {archivo}"):
        return None
    return {
        "id": "CNA:wp:" + str(n.get("id") or link),
        "titulo": titulo,
        "fecha": _fecha_chile(fecha),
        "link": link,
    }


def _leer(lista: str, campos: str, desde: datetime, bundle: str) -> list:
    """Todas las páginas de la colección publicadas desde `desde`. Lanza si falla o no alcanza."""
    items = []
    for pagina in range(1, MAX_PAGINAS + 1):
        resp = requests.get(
            API.format(coleccion=lista, pagina=pagina, desde=desde.strftime("%Y-%m-%dT%H:%M:%SZ"),
                       campos=campos),
            headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"},
            timeout=TIMEOUT,
            verify=bundle,
        )
        resp.raise_for_status()
        lote = resp.json()
        if not isinstance(lote, list):
            raise ValueError("la respuesta no es lista")
        items += lote
        # Una página puede traer menos de 100, o ninguno, sin ser la última: WordPress cuenta archivos
        # que no lista (4.675 contados, 4.509 listados, 27-11). Se sigue solo X-WP-TotalPages; sin esa
        # cabecera no se sabe si se leyó todo y la revisión queda parcial.
        try:
            total = int(resp.headers["X-WP-TotalPages"])
        except (KeyError, ValueError):
            raise ValueError("sin X-WP-TotalPages legible")
        if pagina >= total:
            return items
    raise ValueError(f"más de {MAX_PAGINAS} páginas en la ventana")


def fetch_convocatorias_pares():
    """Devuelve (avisos, ok). ok=False si alguna lista no respondió. Nunca lanza:
    un fallo de la CNA no puede tumbar el correo de licitaciones."""
    desde = datetime.now(timezone.utc) - timedelta(days=VENTANA_DIAS)
    avisos, ok = [], True
    avisadas = set()  # ids de entradas que avisaron (LISTAS lee posts antes que media)
    try:
        bundle = _bundle()
    except Exception as e:  # disco: se informa como revisión parcial
        logger.error(f"CNA: no se pudo armar el bundle de certificados ({e})")
        return [], False
    for lista, campos in LISTAS:
        try:
            items = _leer(lista, campos, desde, bundle)
        except Exception as e:  # red, SSL, JSON, disco: se informa como revisión parcial
            logger.error(f"CNA {lista}: sin respuesta ({e})")
            ok = False
            continue
        n_avisos = 0
        for n in items:
            try:
                a = _aviso(n, desde, avisadas if lista == "media" else frozenset()) if isinstance(n, dict) else None
            except Exception as e:
                logger.warning(f"CNA {lista}: entrada ilegible ({e})")
                continue
            if a:
                avisos.append(a)
                n_avisos += 1
                if lista == "posts":
                    avisadas.add(n.get("id"))
        logger.info(f"CNA {lista}: {len(items)} leídas, {n_avisos} llamados a pares recientes")
    return avisos, ok
