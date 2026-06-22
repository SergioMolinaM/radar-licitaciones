"""Configuración central del radar de licitaciones."""

# Keywords de inclusión: si una licitación contiene alguno, entra al match.
# Match case-insensitive sobre Nombre + Descripcion.
KEYWORDS_INCLUDE = [
    # Núcleo Tercera Letra
    "comunicación estratégica",
    "comunicación institucional",
    "comunicación de riesgo",
    "comunicación pública",
    "estudio cualitativo",
    "estudio cuantitativo",
    "estudio de percepción",
    "estudio de opinión",
    "investigación social",
    "consultoría",
    "asesoría estratégica",
    "asesoría comunicacional",
    "evaluación de programa",
    "evaluación de política",
    "diagnóstico institucional",
    "diseño metodológico",
    "metodología cualitativa",
    "análisis de datos",
    "inteligencia de datos",
    "monitoreo y evaluación",
    "diseño de instrumento",
    "facilitación",
    "participación ciudadana",
    "consulta ciudadana",
    "diálogo social",
    "vocería",
    # RADAR / Radar Circular
    "economía circular",
    "responsabilidad extendida",
    "ley rep",
    "gestión de residuos",
    "valorización",
    # Educación (Radar Educativo / Camino a la U)
    "convivencia escolar",
    "educación superior",
    "trayectoria educativa",
    "abandono escolar",
    "deserción",
    "slep",
    "servicios locales de educación",
]

# Keywords de exclusión: si aparecen, descarta (ruido típico observado).
# Ajustadas tras auditar 34 matches reales del 22-06-2026.
KEYWORDS_EXCLUDE = [
    # Compra de bienes físicos (Tercera Letra no vende productos)
    "adquisición",
    "suministro",
    "arriendo",
    "compra de",
    "aseo",
    "vigilancia",
    "guardia",
    "alimentación",
    "casino",
    "uniforme",
    "mobiliario",
    "insumos médicos",
    "materiales de",
    "material pedagógico",
    "implementos",
    "equipamiento deportivo",
    "equipamiento recreativo",
    "proyectores",
    "hosting",
    "telefonía",
    # Obras públicas e infraestructura física
    "obra civil",
    "construcción de",
    "construcción centro",
    "reparación de",
    "mantención de",
    "mantención preventiva",
    "habilitación de instalaciones",
    "diseño de arquitectura",
    "diseño arquitectura",
    "arquitectura y especialidades",
    "topografía",
    "fotogrametría",
    "pavimentación",
    "repavimentación",
    "iluminación",
    "vivienda",
    "viviendas",
    "camino",
    "plaza",
    "costanera",
    "centro de salud",
    "centro cerrado",
    "transporte escolar",
    # Servicios técnicos específicos (no perfil Tercera Letra)
    "erp",
    "sap",
    "consultoría legal",
    "consultoría de diseño",
    "consultoría diseño",
    "consultoría de especialidades",
    "consultoría apoyo técnico",
    "fiscalización de",
    "escrituras",
]

# Estados de Mercado Público a incluir (publicada = abierta para postular)
MP_ESTADOS_INTERES = ["publicada", "activa"]

# Monto mínimo estimado (en CLP) para filtrar ruido. None = sin filtro.
# MP no siempre entrega monto; cuando no, se incluye igual.
MONTO_MINIMO_CLP = None

# Feeds RSS de PNUD a consultar.
# PNUD usa códigos propietarios (no ISO3). Chile, Uruguay y Paraguay no tienen
# feed propio (sin oficina con compras suficientes). Para Chile, la fuente
# institucional es Mercado Público. El feed global atrapa el resto.
UNDP_FEEDS = {
    "Bolivia": "https://procurement-notices.undp.org/rss_feeds/BOL.xml",
    "Perú": "https://procurement-notices.undp.org/rss_feeds/PER.xml",
    "Colombia": "https://procurement-notices.undp.org/rss_feeds/COL.xml",
    "Argentina": "https://procurement-notices.undp.org/rss_feeds/ARG.xml",
    "Ecuador": "https://procurement-notices.undp.org/rss_feeds/ECU.xml",
    "México": "https://procurement-notices.undp.org/rss_feeds/MEX.xml",
}

# Feed global PNUD: red de seguridad para licitaciones regionales/multipaís
# que no aparecen en feeds país. Mayor volumen, mismo filtro de keywords.
UNDP_GLOBAL_FEED = "https://procurement-notices.undp.org/rss_feeds/rss.xml"

# Si el feed global trae muchas entradas internacionales irrelevantes,
# limitar por país en el título/descripción (case-insensitive).
# Vacío = sin filtro geográfico adicional.
UNDP_GLOBAL_PAIS_FILTRO = [
    "chile", "bolivia", "perú", "peru", "colombia", "argentina",
    "ecuador", "méxico", "mexico", "latin america", "regional",
]

# Endpoint API Mercado Público (correcto, verificado)
MP_API_URL = "https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json"
