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
import socket
import ssl
import tempfile
import unicodedata
import warnings
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
    try:
        bundle = _bundle()
    except Exception as e:  # disco: se informa como revisión parcial
        logger.error(f"CNA: no se pudo armar el bundle de certificados ({e})")
        return [], False
    for lista, campos in LISTAS:
        try:
            resp = requests.get(
                API.format(lista=lista, campos=campos),
                headers={"Accept": "application/json;odata=nometadata", "User-Agent": "Mozilla/5.0"},
                timeout=TIMEOUT,
                verify=bundle,
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
