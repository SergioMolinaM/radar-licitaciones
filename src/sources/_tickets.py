"""Tickets de Mercado Público: principal y respaldo.

MERCADO_PUBLICO_TOKEN es el principal. MERCADO_PUBLICO_TOKEN_2 (emitido el
22-oct-2026) es solo de respaldo: se usa cuando ChileCompra rechaza el
principal por inválido, inactivo o bloqueado. NUNCA ante un 429: la cuota es
por ticket y por día (guía Compra Ágil §4), y repartir consultas entre dos
tickets para sumar cuota es saltarse el límite. La guía dice que una cuota
mayor se pide a ChileCompra (§4.3).

El valor del ticket nunca se loguea: solo su nombre («principal»/«respaldo»).
"""

import os

_VARIABLES = (("principal", "MERCADO_PUBLICO_TOKEN"), ("respaldo", "MERCADO_PUBLICO_TOKEN_2"))


def tickets() -> list[tuple[str, str]]:
    """[(nombre, valor)] de los tickets configurados, en orden de uso."""
    return [(nombre, os.environ[var]) for nombre, var in _VARIABLES if os.getenv(var)]
