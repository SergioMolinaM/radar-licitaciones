"""Configuración central del radar de licitaciones."""

# Keywords de inclusión: si una licitación contiene alguno, entra al match.
# Match case-insensitive sobre Nombre + Descripcion.
KEYWORDS_INCLUDE = [
    # Núcleo comunicaciones
    "comunicación estratégica",
    "comunicación institucional",
    "comunicación de riesgo",
    "comunicación pública",
    "campaña comunicacional",
    "campañas comunicacionales",
    "plan de comunicaciones",
    "plan comunicacional",
    "plan de medios",
    "gestión de medios",
    "marketing digital",
    # Consultoría (específica, no "consultoría" a secas — trae mucho ruido)
    "consultoría comunicacional",
    "consultoría estratégica",
    "consultoría en comunicación",
    "consultoría en comunicaciones",
    "asesoría estratégica",
    "asesoría comunicacional",
    "asesoría en comunicación",
    "vocería",
    # Estudios e investigación
    "estudio cualitativo",
    "estudio cuantitativo",
    "estudio de percepción",
    "estudio de opinión",
    "investigación social",
    "encuesta",
    "encuestas",
    "clima organizacional",
    "análisis de datos",
    "inteligencia de datos",
    # Evaluación y diagnóstico
    "evaluación de programa",
    "evaluación de política",
    "evaluación de políticas",
    "evaluación de impacto",
    "diagnóstico institucional",
    "diseño metodológico",
    "metodología cualitativa",
    "monitoreo y evaluación",
    "diseño de instrumento",
    # Facilitación y formación
    "facilitación",
    "relatoría",
    "relator",
    "participación ciudadana",
    "consulta ciudadana",
    "diálogo social",
    "capacitación en género",
    "capacitación en materia de género",
    "perspectiva de género",
    "enfoque de género",
    # Editorial (Tercera Letra core)
    "edición de libro",
    "publicación de libro",
    "corrección de estilo",
    "corrección ortotipográfica",
    "redacción",
    "diagramación",
    "diseño editorial",
    "guía metodológica",
    "guía didáctica",
    "manual pedagógico",
    "material educativo",
    "cuenta pública",
    "memoria institucional",
    "memoria anual",
    "cápsulas radiales",
    "cápsulas educativas",
    "cápsulas informativas",
    "podcast institucional",
    "infografía",
    # RADAR / Radar Circular
    "economía circular",
    "responsabilidad extendida",
    "ley rep",
    "gestión de residuos",
    "valorización",
    "cambio climático",
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
    # Salud clínica y técnica (no perfil TL — atrapa "insumos médicos", "quirúrgico")
    "quirúrgic",
    "radiológic",
    "hemodinamia",
    "gastroenterolog",
    "psicolabor",
    "arterial",
    "sellador",
    # Técnico / ingeniería / geociencias
    "topográfic",
    "topografic",
    "geológic",
    "geofísic",
    "fitoplancton",
    "zoobentos",
    "físico químic",
    "fisicoquímic",
    "modelación",
    "radiocomunicaciones",
    # Otros bienes/servicios anchos que no aplican
    "insumos",
    "kit ",
    "servicio de transporte",
    "vehículos fiscales",
]

# Estados de Mercado Público a incluir (publicada = abierta para postular)
MP_ESTADOS_INTERES = ["publicada", "activa"]

# Monto mínimo estimado (en CLP) para filtrar ruido. None = sin filtro.
MONTO_MINIMO_CLP = None

# Feeds RSS de PNUD a consultar.
UNDP_FEEDS = {
    "Bolivia": "https://procurement-notices.undp.org/rss_feeds/BOL.xml",
    "Perú": "https://procurement-notices.undp.org/rss_feeds/PER.xml",
    "Colombia": "https://procurement-notices.undp.org/rss_feeds/COL.xml",
    "Argentina": "https://procurement-notices.undp.org/rss_feeds/ARG.xml",
    "Ecuador": "https://procurement-notices.undp.org/rss_feeds/ECU.xml",
    "México": "https://procurement-notices.undp.org/rss_feeds/MEX.xml",
}

UNDP_GLOBAL_FEED = "https://procurement-notices.undp.org/rss_feeds/rss.xml"

UNDP_GLOBAL_PAIS_FILTRO = [
    "chile", "bolivia", "perú", "peru", "colombia", "argentina",
    "ecuador", "méxico", "mexico", "latin america", "regional",
]

MP_API_URL = "https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json"

# --- Compra Ágil (API v2, api2.mercadopublico.cl) ---
# OJO: base distinta (api2) y auth por HEADER `ticket`, no query param.
COMPRA_AGIL_API_URL = "https://api2.mercadopublico.cl/v2/compra-agil"

# Estados a incluir. "publicada" = abierta recibiendo cotizaciones (oportunidad
# real para postular). Admite múltiples separados por coma.
COMPRA_AGIL_ESTADOS = "publicada"

# Ventana de días hacia atrás sobre fecha de publicación. 3 cubre el fin de
# semana en la corrida del lunes. El dedupe por state.json evita repetir.
COMPRA_AGIL_DIAS_VENTANA = 3

# Ficha pública de la Compra Ágil. La guía de la API no la documenta (solo expone
# links.detalle, que apunta de vuelta a la API y exige ticket). Este patrón se
# verificó a mano el 14-07-2026 abriendo 5627-188-COT26 desde el buscador
# público: carga sin sesión. El {codigo} tiene formato 1057539-228-COT26.
COMPRA_AGIL_WEB_URL_TEMPLATE = "https://buscador.mercadopublico.cl/ficha?code={codigo}"
