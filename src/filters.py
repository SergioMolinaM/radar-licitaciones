"""Filtrado de licitaciones por keywords de inclusión/exclusión."""

import re
import unicodedata
from .config import (
    KEYWORDS_INCLUDE, KEYWORDS_INCLUDE_PALABRA, KEYWORDS_EXCLUDE,
    KEYWORDS_INCLUDE_EN, KEYWORDS_EXCLUDE_EN,
)


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


# Conectores que los títulos se comen: «ESTUDIO PERCEPCIÓN SOBRE…» (1003780-1-LE26,
# 16-oct) no calzaba «estudio de percepción». Solo para inclusión: en exclusión
# «compra de» o «construcción de» pasarían a excluir «compra» y «construcción».
_CONECTORES = {"de", "del", "la", "las", "el", "los", "en", "y", "e", "para", "a", "al", "un", "una"}
_SEP_CONECTORES = r"(?:\s+(?:" + "|".join(sorted(_CONECTORES)) + r"))*\s+"


def _patron_inclusion(kw_norm: str) -> re.Pattern:
    """Como _patron, pero los conectores entre palabras son opcionales y se
    aceptan otros: «estudio de percepción» calza «estudio percepción» y
    «estudio de la percepción». Solo si la keyword trae conectores: «ley rep»
    con conectores opcionales calzaba «Ley de la República»."""
    palabras = [p for p in kw_norm.split(" ") if p not in _CONECTORES]
    if len(palabras) < 2 or len(palabras) == len(kw_norm.split(" ")):
        return _patron(kw_norm)
    return re.compile(r"(?<![a-z0-9])" + _SEP_CONECTORES.join(re.escape(p) for p in palabras))


# Pre-normalizar keywords una sola vez al importar
_INCLUDE_NORM = [(kw, _normalize(kw)) for kw in KEYWORDS_INCLUDE]
_EXCLUDE_NORM = [_normalize(kw) for kw in KEYWORDS_EXCLUDE]
_INCLUDE_RE = [(kw, _patron_inclusion(n)) for kw, n in _INCLUDE_NORM] + \
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


_INCLUDE_EN_RE = [(kw, _patron(_normalize(kw))) for kw in KEYWORDS_INCLUDE_EN]
_EXCLUDE_EN_RE = [_patron(_normalize(kw)) for kw in KEYWORDS_EXCLUDE_EN]


def matches_keywords_intl(text: str, exigir_keyword: bool = True) -> tuple[bool, list[str]]:
    """Como matches_keywords, para fuentes internacionales: keywords en español y en
    inglés, exclusiones de los dos idiomas. Con exigir_keyword=False pasa todo lo no
    excluido (feeds de país chicos que se quieren ver completos)."""
    if not text:
        return False, []
    t = _normalize(text)
    if any(p.search(t) for p in _EXCLUDE_RE + _EXCLUDE_EN_RE):
        return False, []
    encontradas = [kw for kw, p in _INCLUDE_RE + _INCLUDE_EN_RE if p.search(t)]
    if not exigir_keyword:
        return True, encontradas or ["(todo el feed del país)"]
    return (len(encontradas) > 0, encontradas)
