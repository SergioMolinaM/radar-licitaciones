"""Filtrado de licitaciones por keywords de inclusión/exclusión."""

import re
import unicodedata
from .config import KEYWORDS_INCLUDE, KEYWORDS_INCLUDE_PALABRA, KEYWORDS_EXCLUDE


def _normalize(text: str) -> str:
    """Lowercase + remueve acentos + colapso de espacios múltiples."""
    text = text.lower()
    # Descomponer acentos y eliminarlos
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    # Colapsar espacios
    return re.sub(r"\s+", " ", text).strip()


def _patron(kw_norm: str, palabra_completa: bool = False) -> re.Pattern:
    """La keyword debe empezar al inicio de una palabra; puede terminar dentro
    de una ("quirúrgic" sigue cubriendo "quirúrgico"). Sin esto, "erp" excluía
    "interpretación" y "cuerpos", y "sap" excluía "ssap".
    Con palabra_completa también debe terminar en borde de palabra."""
    fin = r"(?![a-z0-9])" if palabra_completa else ""
    return re.compile(r"(?<![a-z0-9])" + re.escape(kw_norm) + fin)


# Pre-normalizar keywords una sola vez al importar
_INCLUDE_NORM = [(kw, _normalize(kw)) for kw in KEYWORDS_INCLUDE]
_EXCLUDE_NORM = [_normalize(kw) for kw in KEYWORDS_EXCLUDE]
_INCLUDE_RE = [(kw, _patron(n)) for kw, n in _INCLUDE_NORM] + \
              [(kw, _patron(_normalize(kw), palabra_completa=True)) for kw in KEYWORDS_INCLUDE_PALABRA]
_EXCLUDE_RE = [_patron(n) for n in _EXCLUDE_NORM]


def keywords_incluidas(text: str) -> list[str]:
    """Keywords de inclusión presentes en el texto, sin mirar exclusiones."""
    t = _normalize(text or "")
    return [kw for kw, patron in _INCLUDE_RE if patron.search(t)]


def excluido(text: str, omitir=()) -> bool:
    """True si el texto calza alguna keyword de exclusión, salvo las de `omitir`."""
    t = _normalize(text or "")
    omitir_norm = {_normalize(kw) for kw in omitir}
    return any(patron.search(t) for n, patron in zip(_EXCLUDE_NORM, _EXCLUDE_RE) if n not in omitir_norm)


def matches_keywords(text: str) -> tuple[bool, list[str]]:
    """
    Evalúa si un texto cumple criterios de inclusión y no incluye exclusiones.
    Retorna (match, keywords_originales_encontradas).
    Tanto texto como keywords se comparan sin acentos y con espacios normalizados.
    """
    if not text:
        return False, []

    t = _normalize(text)

    # Filtro de exclusión
    for patron in _EXCLUDE_RE:
        if patron.search(t):
            return False, []

    # Filtro de inclusión (devuelve las originales con acentos, para display)
    encontradas = [kw_original for kw_original, patron in _INCLUDE_RE if patron.search(t)]
    return (len(encontradas) > 0, encontradas)
