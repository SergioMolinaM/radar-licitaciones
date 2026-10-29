"""Configuración central del radar de licitaciones."""

# Keywords de inclusión: si una licitación contiene alguno, entra al match.
# Match case-insensitive y sin acentos sobre el NOMBRE (las fuentes no pasan la
# descripción). Cada keyword debe empezar al inicio de una palabra del título.
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
    # Web y comunicación digital. "portal" a secas no: trae "portal de acceso"
    # (obra vial) y "portal de pagos". Medido contra audit-2026-07-08.csv.
    "portal institucional",
    "portal web",
    "sitio web",
    "sitios web",
    "página web",
    "páginas web",
    "diseño web",
    "desarrollo web",
    "rediseño web",
    "rediseño del portal",
    "rediseño del sitio",
    "rediseño de la página",
    "aula virtual",
    "plataforma web",
    "redes sociales",
    "contenidos digitales",
    "comunicación digital",
    "producción audiovisual",
    "video institucional",
    "identidad visual",
    "imagen corporativa",
    "transformación digital",
    "inteligencia artificial",
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
    # Radar Construcción Industrializada (7-oct-2026): estudios, no compra de
    # módulos. "modular" y "paneles" a secas no: traen arriendo de oficinas
    # modulares y paneles solares. "vivienda(s) industrializada(s)" no sirve:
    # la exclusión "vivienda" gana siempre. La consultoría de fiscalización de
    # plantas (712307-38-LE26) igual queda fuera por "fiscalización de" y
    # "consultoría apoyo técnico"; caza el estudio SIP (587-45-L125).
    "construcción industrializada",
    "industrialización de la construcción",
    "plantas industrializadoras",
    "paneles sip",
    # Huecos del triage «fuera del radar» del 16-oct-2026 (triage/2026-10-16-
    # fuera-del-radar.md): servicios afines que se publicaron y el Radar no vio.
    # Ruido medido contra audit-2026-07-08.csv; el que apareció tiene exclusión
    # propia («licencias de software», «pavimentos», «equipos audiovisuales», «plataforma
    # elevadora»). "datos" a secas no: trae enlaces y redes de datos (7 de 7).
    # "humedales" no: estrategia ambiental, TL solo entraría con socio.
    "audiovisual",
    # "documental" a secas no: 3 de 4 en julio eran gestión documental.
    "serie documental",
    "realización de documental",
    "producción de documental",
    "microserie",
    "podcast",
    "vodcast",
    "spot publicitario",
    "diseño gráfico",
    "piezas gráficas",
    "maquetación",
    "software",
    "intranet",
    "plataforma",
    "e-learning",
    "elearning",
    "moodle",
    "dashboard",
    "inteligencia territorial",
    "gobernanza de datos",
    "gestión de datos",
    "ciencia de datos",
    "visualización de datos",
    "datos abiertos",
    "indicadores",
    "convivencia",
    "plan municipal de cultura",
    "participativo",
    "participativa",
]

# Keywords de inclusión que deben calzar como PALABRA COMPLETA (no prefijo).
# "ia" como prefijo trae "IaaS"; "digital" trae "digitalización" (archivos,
# fotocopiado); "web" trae "webpay". Medido contra audit-2026-07-08.csv: web 6,
# digital ~15 (incluye ruido: plataformas escolares, "biopsia... digital"), ia 2.
KEYWORDS_INCLUDE_PALABRA = [
    "web",
    "digital",
    "ia",
    # 16-oct: «VIDEO PARA CUENTA PÚBLICA» (696713-81-COT26). Como prefijo traería
    # videoconferencia y videovigilancia.
    "video",
    "videos",
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
    "televigilancia",   # compuestos: desde el borde de palabra (2-oct) "vigilancia"
    "videovigilancia",  # ya no los cubre dentro de la palabra
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
    "electroquirúrgic",
    "cardioquirúrgic",
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
    "hidrogeológic",
    "geofísic",
    "fitoplancton",
    "zoobentos",
    "físico químic",
    "fisicoquímic",
    "modelación",
    "remodelación",
    "radiocomunicaciones",
    # Otros bienes/servicios anchos que no aplican
    "insumos",
    "kit ",
    "servicio de transporte",
    "vehículos fiscales",
    # Ruido de las keywords del 16-oct, medido en audit-2026-07-08.csv
    # 7 de las 12 de «software» eran licencias de terceros. «licencia» a secas no:
    # botaba «Licencias Claude Pro» y «licencias ChatGPT» (reventa, triage 15-oct).
    "licencias de software",
    "licencia de software",
    "licencias software",
    "licencia software",
    "pavimentos",             # «pavimentos participativos» (obra)
    "pav.",                   # «CONST. PROG. PAV. PARTICIPATIVOS»
    "equipos audiovisuales",
    "plataforma elevadora",
    "laringoscop",            # «video» como palabra: equipos médicos y de seguridad
    "endoscop",
    "video portero",
    "videoportero",
    "cámara de video",
    "cámaras de video",
]

# Estados de Mercado Público a incluir (publicada = abierta para postular)
MP_ESTADOS_INTERES = ["publicada", "activa"]

# Monto mínimo estimado (en CLP) para filtrar ruido. None = sin filtro.
MONTO_MINIMO_CLP = None

# Keywords en inglés, solo para fuentes internacionales (PNUD y ONU), que publican
# casi todo en inglés: con las de arriba un «Communication strategy» no calzaba.
# Lista aparte porque KEYWORDS_INCLUDE alimenta las búsquedas rotativas de Compra
# Ágil y sumarle términos gasta su cuota (429). Mismo matcheo: inicio de palabra.
KEYWORDS_INCLUDE_EN = [
    "communication", "outreach", "public awareness", "awareness campaign", "media",
    "campaign", "advocacy", "storytelling", "editorial", "editing", "copy edit",
    "publication", "audiovisual", "video production",
    "survey", "public opinion", "perception study", "focus group", "qualitative",
    "quantitative", "research", "baseline", "evaluation", "assessment", "diagnostic",
    "data", "dashboard", "information system", "digital platform", "web platform",
    "website", "web portal", "software development", "artificial intelligence",
    "machine learning",
    "citizen participation", "public participation", "consultation", "stakeholder",
    "engagement", "dialogue", "governance", "capacity building", "training",
    "workshop", "facilitation",
    "circular economy", "waste management", "recycling", "extended producer",
    "climate change", "education",
]

# Exclusiones en inglés para las mismas fuentes (bienes y obras).
KEYWORDS_EXCLUDE_EN = [
    "supply of", "supply and", "delivery of goods", "equipment", "vehicle",
    "construction", "civil works", "rehabilitation works", "medical", "laboratory",
    "furniture", "fuel", "spare parts", "refrigeration", "air conditioning",
]

# Feeds RSS de PNUD a consultar. Chile es CHI, no CHL: CHL da 404 y por eso hasta el
# 26-oct-2026 Chile solo entraba por el feed global (CHI.xml: «listings are for CHILE»).
UNDP_FEEDS = {
    "Chile": "https://procurement-notices.undp.org/rss_feeds/CHI.xml",
    "Bolivia": "https://procurement-notices.undp.org/rss_feeds/BOL.xml",
    "Perú": "https://procurement-notices.undp.org/rss_feeds/PER.xml",
    "Colombia": "https://procurement-notices.undp.org/rss_feeds/COL.xml",
    "Argentina": "https://procurement-notices.undp.org/rss_feeds/ARG.xml",
    "Ecuador": "https://procurement-notices.undp.org/rss_feeds/ECU.xml",
    "México": "https://procurement-notices.undp.org/rss_feeds/MEX.xml",
}

# Países cuyo feed PNUD entra completo, sin exigir keyword: pocos avisos al mes
# (5 de jul a oct 2026) y Sergio prefiere ver todo y decidir. Siguen las exclusiones.
UNDP_FEEDS_SIN_KEYWORDS = {"Chile"}

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

# Búsqueda por palabra clave en el servidor (`q`, guía §5.1 Grupo 5) en vez de
# barrer el listado. Medido el 14-oct-2026: cada consulta tarda 5-29 s y la API
# corta a los 29 s (504), sea cual sea el tamaño de página; 3 días de
# publicadas eran 5.400 registros (108 páginas lentas). Barrer todo ya no cabe.
# Estos términos se buscan en TODAS las corridas; deben estar en KEYWORDS_INCLUDE.
# `q` calza CUALQUIER palabra del término (sonda run 38938450758, 16-oct: «sitio
# web» = «sitio» ∪ «web»). «diseño web» ya trae todo lo de «web», así que «sitio
# web», «página web», «portal web» y «plataforma web» sobraban como diarios: cuatro
# consultas menos, con la API dando 504 a la mitad. «diseño web» y «producción
# audiovisual» se quedan porque además traen «diseño» y «producción» (el folleto
# de Antuco 4027-283-COT26, PRESENTAR el 16-oct, solo llegaba por «diseño»). Las
# cuatro frases siguen en la rotación.
# 29-oct (Sergio): «diseño web», «marketing digital» y «producción audiovisual»
# dieron 504 en todas las corridas del 20 al 28-oct, y «diseño» y «producción»
# solas también. Sonda run 40741312235 (28-oct): «web» 200 en 2 de 2 rondas;
# «digital» y «audiovisual» 200 en 1 de 2. Las frases vuelven a la rotación.
# «redes sociales» queda hasta que la sonda encuentre sustituto.
COMPRA_AGIL_TERMINOS_DIARIOS = [
    "inteligencia artificial",
    "web",
    "redes sociales",
    "digital",
    "audiovisual",
    "encuesta",
    "redacción",
    "diagramación",
    "infografía",
    "relator",
    "economía circular",
]
# Exclusiones que NO se aplican a los resultados de la búsqueda q: en Compra
# Ágil casi todo título empieza con «Adquisición de…» o «Compra de…» (14-oct:
# los 9 resultados de «inteligencia artificial» caían por «adquisición»), y el
# servidor ya filtró por tema. El resto de KEYWORDS_EXCLUDE sí se aplica.
COMPRA_AGIL_EXCLUSIONES_OMITIDAS = ["adquisición", "compra de", "suministro"]
# El resto de KEYWORDS_INCLUDE rota: cada corrida sigue desde donde quedó la
# anterior (state["ca_cursor"]) con el tiempo que sobre del presupuesto. Cada
# término (diario o rotativo) busca desde su última búsqueda exitosa y no
# truncada (state["ca_ultima"]), así una vuelta de varios días o una racha de
# fallas no deja huecos; tope COMPRA_AGIL_DIAS_MAX_ROTATIVO.
# KEYWORDS_INCLUDE_PALABRA no se buscan con q. «web» sola dio 8 en 7 días (no los
# cientos que se temían), pero «diseño web» ya la cubre; «digital» e «ia» no se
# midieron.
COMPRA_AGIL_DIAS_MAX_ROTATIVO = 14

# Ficha pública de la Compra Ágil. La guía de la API no la documenta (solo expone
# links.detalle, que apunta de vuelta a la API y exige ticket). Este patrón se
# verificó a mano el 14-07-2026 abriendo 5627-188-COT26 desde el buscador
# público: carga sin sesión. El {codigo} tiene formato 1057539-228-COT26.
COMPRA_AGIL_WEB_URL_TEMPLATE = "https://buscador.mercadopublico.cl/ficha?code={codigo}"
# Sección del correo para lo que la búsqueda q trajo sin keyword en el nombre
# (q calza palabras sueltas, no la frase; 15-oct).
FUENTE_PALABRA_SUELTA = "Compra Ágil · por palabra suelta"
