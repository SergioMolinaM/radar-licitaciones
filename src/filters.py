"""Filtrado de licitaciones por keywords de inclusión/exclusión."""

import re
import unicodedata
from .config import KEYWORDS_INCLUDE, KEYWORDS_EXCLUDE


def _normalize(text: str) -> str:
    """Lowercase + remueve acentos + colapso de espacios múltiples."""
    text = text.lower()
    # Descomponer acentos y eliminarlos
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    # Colapsar espacios
    return re.sub(r"\s+", " ", text).strip()


# Pre-normalizar keywords una sola vez al importar
_INCLUDE_NORM = [(kw, _normalize(kw)) for kw in KEYWORDS_INCLUDE]
_EXCLUDE_NORM = [_normalize(kw) for kw in KEYWORDS_EXCLUDE]


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
    for kw_norm in _EXCLUDE_NORM:
        if kw_norm in t:
            return False, []

    # Filtro de inclusión (devuelve las originales con acentos, para display)
    encontradas = [kw_original for kw_original, kw_norm in _INCLUDE_NORM if kw_norm in t]
    return (len(encontradas) > 0, encontradas)
