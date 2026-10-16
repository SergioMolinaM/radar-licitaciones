# Fuera del Radar — 16-oct-2026

Búsqueda manual por fuera de la herramienta (buscador público de Compra Ágil y buscador de licitaciones de
Mercado Público), hecha el viernes 16-oct entre las 10:40 y las 11:50 (hora del navegador). Motivo: la API de Compra Ágil no respondió
hoy a ocho términos diarios y el Radar filtra por palabra del título. Excluidos los códigos que el Radar ya trajo
hoy y los que están en curso (lista del coordinador).

## Cómo se buscó y qué limita el resultado

- **Compra Ágil**: buscador público `buscador.mercadopublico.cl/compra-agil`, estado Publicada, fechas
  16-sep a 16-oct (por defecto del buscador). Se llamó desde la página al mismo servicio que usa el buscador
  (`api.buscador.mercadopublico.cl/compra-agil`, parámetro `keywords`) para no depender de la interfaz. Se leyeron
  hasta 6 páginas de 15 por término.
- **El buscador de Compra Ágil no busca frases**: calza palabras sueltas en nombre y descripción. Por eso
  «plataforma web» da 77 y «capacitación en género» 4.315. Los conteos de abajo son los del servicio, no
  coincidencias reales; lo útil se sacó leyendo los títulos.
- **El servicio de Compra Ágil estuvo saturado**: muchas consultas cortan a los ~29 s (lo mismo que le pasa al
  Radar). Cada término se intentó al menos dos veces; los que no respondieron quedan marcados «sin respuesta».
- **Licitaciones**: `mercadopublico.cl/BuscarLicitacion` (POST `/BuscarLicitacion/Home/Buscar`), estado Publicada,
  orden «Últimas publicadas», paginando hasta pasar el 14-oct. Se contaron solo las publicadas el 14, 15 y 16-oct.
- Fichas de Compra Ágil: el detalle también depende del servicio saturado; varias no cargaron (se dice en cada
  caso). Montos de licitación: varias fichas no publican el monto (se dice «no publicado»).

## Conteos por búsqueda

### Compra Ágil (resultados del servicio, estado Publicada, 16-sep a 16-oct)

| Término | Resultados | Nota |
|---|---|---|
| sitio web | 15 | |
| página web | 12 | |
| plataforma web | 77 | palabra suelta |
| portal web | 128 | palabra suelta |
| diseño web | 69 | palabra suelta |
| redes sociales | 43 | |
| marketing digital | 80 | |
| producción audiovisual | 129 | |
| tablero | 6 | todos tableros eléctricos o marcadores |
| dashboard | 0 | la interfaz dijo «No se encontraron resultados»; control: «sitio web» dio 15 y «tablero» 6 en la misma sesión |
| encuesta | 3 | |
| sistematización | 3 | |
| página | 4 | |
| software | 39 | reintento con ventana 06 a 16-oct; 22 con «software» en el título, casi todo licencias |
| aplicación | 28 | ídem; 8 con la palabra en el título (cursos de aplicación de normas, plaguicidas) |
| comunicaciones | 28 | ídem; 10 en el título, ninguno servicio de comunicación salvo «Evento Teletón» |
| video | 16 | ídem; 9 en el título |
| diseño gráfico | 71 | ídem; 3 en el título |
| plataforma | 70 | ídem; 7 en el título (renovaciones de plataformas de terceros, carros) |
| capacitación inteligencia artificial | 172 | ídem; 1 en el título (721703-140, ya visto) |
| estudio de opinión, desarrollo de sistema | sin respuesta | 2 rondas de 3 intentos cada una |

Únicos vistos: 320 procesos; 9 ya los trajo el Radar; unos 150 son bienes (insumos clínicos, materiales,
equipos, toner, alimentos) y se cuentan sin abrir.

### Licitaciones (Publicadas; total vigente / publicadas 14-16 oct)

| Término | Vigentes | Publicadas 14-16 oct |
|---|---|---|
| plataforma | 117 | 33 |
| sitio web | 37 | 7 |
| software | 135 | 45 |
| sistema informático | 742 | 150 |
| datos | 145 | 42 |
| estudio | 68 | 8 |
| diagnóstico | 111 | 34 |
| encuesta | 4 | 0 (control: «plataforma» dio 117 en la misma sesión) |
| comunicación | 171 | 38 |
| difusión | 59 | 24 |
| audiovisual | 37 | 20 |
| capacitación | 162 | 55 |
| inteligencia artificial | 24 | 5 |

Únicas publicadas 14-16 oct: 258. Bienes (suministros, fármacos, implantes, equipos): 69. Servicios sin relación
con TL (mantención de equipos, aseo, obras, alarmas, laboratorio, transporte): unos 150. Afines a TL por título: 40,
de las cuales 6 ya estaban en el Radar o en curso (1469-284-L126, 711841-22-LP26, 2405-149-CO26, 1138297-12-LE26,
610-20-LE26, 1233607-3-LE26).

## Candidatas nuevas (ordenadas por cierre)

Veredicto preliminar. Nada es `NO` por falta de requisito textual: lo que no se abrió dice «no abierta».

| Código | Organismo | Monto | Cierre | Qué piden | Veredicto |
|---|---|---|---|---|---|
| 859378-388-COT26 | no verificado (ficha no cargó) | $4.000.000 | **hoy 16-oct 15:00** | Desarrollo de página web y elaboración de material | PRESENTAR solo si Sergio alcanza hoy |
| 1422414-36-COT26 | no verificado | $2.000.000 | 17-oct 17:00 | «Servicio de producción técnica – PY. FUTURA/UMAS» | PREGUNTAR (leer ficha: puede ser producción de evento) |
| 889473-2224-COT26 | no verificado | $1.500.000 | 18-oct 18:00 | Diseño y desarrollo de piezas gráficas (SC 8936) | PRESENTAR |
| 4494-616-COT26 | no verificado | $1.600.000 | 18-oct 13:26 | «Taller de capacitación (P.810)» | PREGUNTAR (tema no visible en el título) |
| 2961-937-COT26 | Programa Somos Barrio (organismo no verificado) | $1.000.000 | 19-oct 10:00 | Material audiovisual de recuperación de memoria barrial; plazo 3 días; tiene adjunto no leído | PREGUNTAR (leer adjunto) |
| 2328-1280-COT26 | no verificado | $7.200.000 | 19-oct 10:00 | Capacitaciones en convivencia educativa para profesores y directivos | CON SOCIO (relator de convivencia escolar) |
| 553368-111-COT26 | Universidad de Tarapacá | $3.000.000 | 19-oct 12:00 (2.º llamado 22-oct 13:44) | Spot publicitario de Admisión 2026 producido con IA; plazo 6 días | PRESENTAR |
| 2268-167-COT26 | no verificado | $400.000 | 19-oct 12:00 | Curso de Python para análisis de datos | PRESENTAR |
| 1412-27-COT26 | no verificado | $600.000 | 19-oct 15:00 | Diseño gráfico y maquetación editorial | PRESENTAR |
| 1216094-56-COT26 | no verificado | $5.500.000 | 19-oct 17:00 | Diseño y confección de un sistema modular metodológico-participativo | PREGUNTAR (puede ser material físico) |
| 2728-48-COT26 | I. Municipalidad de San Carlos | $7.153.545 | 20-oct 10:00 | Software de gestión interna del Cementerio Municipal (ficha no cargó en 2 intentos) | PRESENTAR (leer ficha antes) |
| 696713-81-COT26 | Fiscalías Regionales Metropolitanas (según el título) | $5.000.000 | 20-oct 09:00 | Video para la Cuenta Pública | PRESENTAR |
| 4879-123-COT26 | no verificado | $600.000 | 20-oct 09:00 | Registro audiovisual Feria de Puntos de Cultura | PRESENTAR |
| 1485-65-COT26 | no verificado | $2.500.000 | 20-oct 10:00 | Capacitación docente – jornada taller (tema truncado) | PREGUNTAR |
| 1375754-80-COT26 | no verificado | $7.000.000 | 20-oct 12:00 | Servicio profesional de mantenimiento y desarrollo de intranet | PRESENTAR |
| 1725-218-COT26 | Subsecretaría de las Culturas y las Artes (por el código hermano 1725-219; no verificado) | $3.000.000 | 20-oct 16:50 | Diseño y diagramación (título truncado: «…del Estadi…») | PRESENTAR |
| 1765-11-COT26 | Sercotec, Dirección Regional de Ñuble | $1.400.000 | 21-oct 12:00 | Jornada de capacitación (tema no visible) | PREGUNTAR |
| 1469-286-L126 | Universidad de Talca, Fac. de Odontología | no publicado (L1: < 100 UTM) | 22-oct 15:30 (preguntas hasta 19-oct) | Servicio de plataforma e-learning para cursos de Educación Continua | PREGUNTAR (si piden LMS alojado, TL puede ofrecer Moodle administrado) |
| 1301883-60-COT26 | Servicio Nacional de Reinserción Social Juvenil (según la descripción) | $7.140.000 | 22-oct 20:30 | Microserie documental en formato vodcast, 3 capítulos, historias de jóvenes en reinserción | PRESENTAR |
| 745463-15-COT26 | no verificado | $3.000.000 | 24-oct 08:34 | «Servicio de mantención, actualización de seguridad y soporte de…» (truncado; puede ser sitio web) | PREGUNTAR |
| 4732-27-LE26 | I. Municipalidad de Codegua | no publicado (LE: 100-1.000 UTM) | 26-oct (preguntas hasta 18-oct) | Actualización del Plan Municipal de Cultura con proceso participativo: diagnóstico, co-diseño, levantamiento y análisis, sistematización, validación comunitaria | PRESENTAR |
| 1003780-1-LE26 | Gobierno Regional Metropolitano | no publicado (LE) | 28-oct 15:00 (preguntas hasta 19-oct) | Estudio de percepción sobre el eje Nueva Alameda: diagnóstico de percepciones y experiencias ciudadanas | PRESENTAR (CON SOCIO si exige trabajo de campo grande) |
| 752-32-LP26 | Gobierno Regional de Los Lagos | $100.000.000 | 03-nov 15:30 (preguntas hasta 20-oct) | Consultoría para actualizar el diseño de indicadores y metas de seguimiento | CON SOCIO (monto y equipo) |
| 1782-17-LE26 | Gobierno Regional de Antofagasta | $25.000.000 | 04-nov 15:00 (preguntas hasta 22-oct) | Diagnóstico del ecosistema regional de inversión productiva y propuesta técnica de una Plataforma de Inteligencia Territorial (bases técnicas, costo referencial, insumos EVALTIC). Criterios: técnica 45 %, experiencia del equipo 35 %, económica 15 %, formales 3 %, integridad 2 %. Se permite subcontratar | PRESENTAR (CON SOCIO economista regional para la parte de inversión) |
| 5403-11-LP26 | Comisión Nacional de Acreditación | no publicado (LP: 1.000-5.000 UTM) | 04-nov 16:00 (preguntas hasta 20-oct) | Diseño e instalación progresiva de un modelo institucional de gobernanza de datos | PREGUNTAR / CON SOCIO (leer bases) |
| 1113265-17-LE26 | CFT Estatal de la Región de Antofagasta | no publicado (LE) | 06-nov 15:09 (preguntas hasta 26-oct) | Adquisición e implementación de una plataforma de gestión estratégica de la permanencia estudiantil | PRESENTAR (calza con Camino a la U) |
| 1261-37-LR26 | Gobierno Regional Metropolitano | no verificado (LR: > 5.000 UTM) | 16-nov (preguntas hasta 26-oct) | Estrategia de reconocimiento de humedales: componentes 2 (diagnóstico regional), 3 (gobernanza y planificación) y 5 (conciencia pública) | CON SOCIO (consultora ambiental; TL en el componente 5) |

Abiertas y descartadas como no-servicio para TL (sin requisito que leer): 1057384-157-L126 (es compra de
licencias Adobe), 2775-126-LP26 (obra FRIL de iluminación), 3447-457-COT26 y 895072-128-COT26 (suscripciones
a software de terceros).

No abiertas, afines por título, de menor encaje: 1782-15-LE26 (producción logística y montaje de feria, GORE
Antofagasta, 26-oct), 2446-309-LE26 (difusión radial, 29-oct), 1271178-49-LE26 (gestor documental SaaS, 29-oct),
y la serie de capacitaciones de salud (4375-137, 4375-138, 652-60, 1978-130, 2688-29, 2483-260, 734-61,
1084156-47; cierres 23 a 28-oct) donde TL solo calza si hay un lote de IA o herramientas digitales.

Ya cerrada al revisar (11:02): 1447928-52-COT26 (APP para la web de una fundación, cerró 10:55).
Cierran hoy a las 12:00, sin margen real a las 11:50: 553368-106 (difusión multiplataforma, $7.100.000),
1098710-195 (adaptación del módulo de autoevaluación de una plataforma, $6.000.000), 1609-104 (apoyo
tecnológico para implementación digital, $7.160.000), 4886-42 (registro y edición de video documental de gira
de orquesta, $7.100.000). Cierran hoy 13:00-13:15: 1367960-170 a 173 (planes de medios radial, TV y diario para
una fiesta regional, $150.000-$300.000 c/u; es compra de espacio en medios).

## Por qué el Radar no las trajo (contra `src/config.py`)

- 1003780-1-LE26 «ESTUDIO PERCEPCIÓN SOBRE…»: la keyword es «estudio de percepción»; el título no tiene «de».
- 5403-11-LP26 «gobernanza de datos»: no hay keyword; «análisis de datos» e «inteligencia de datos» no calzan.
- 1782-17-LE26 «Consultoría Plataforma Inteligencia Inversión»: solo existe «plataforma web»; falta «plataforma» o «inteligencia territorial».
- 1113265-17-LE26 «PLATAFORMA DE GESTIÓN ESTRATÉGICA»: misma causa.
- 752-32-LP26 «Estudio… Indicadores y Metas»: no hay keyword de indicadores ni «consultoría» a secas (excluida a propósito).
- 4732-27-LE26 «Plan Municipal de Cultura»: «participación ciudadana» está solo en la descripción, que las fuentes no pasan.
- 1261-37-LR26 «Estrategia Reconocimiento Humedales»: no hay keyword.
- 1469-286-L126 «plataforma e-learning»: está «aula virtual», no «e-learning».
- 1301883-60-COT26 «microserie», 2961-937 y 4879-123 «material/registro audiovisual»: solo existe «producción audiovisual» y «video institucional»; falta «audiovisual» suelto.
- 1412-27-COT26 «Diseño Gráfico y Maquetación Editorial»: falta «diseño gráfico» y «maquetación».
- 2728-48-COT26 «Software…»: no hay keyword «software».
- 1375754-80-COT26 «Intranet»: no hay keyword.
- 2328-1280-COT26 «convivencia educativa»: la keyword es «convivencia escolar».
- 553368-111-COT26 «PRODUCCIÓN AUDIOVISUAL…» y 2268-167 «análisis de datos»: las keywords existen; la consulta a la API no respondió hoy (término caído, no falta de keyword).
- 696713-81-COT26 «VIDEO PARA CUENTA PÚBLICA…»: «cuenta pública» está en las keywords; término caído (rotativo, la API no respondió).
- 1367960-170 a 173 «PLAN DE MEDIOS DE COMUNICACIÓN…»: «plan de medios» está en las keywords; término caído.
- 889473-2224-COT26 «Diseño y Desarrollo Piezas Gráficas»: falta «piezas gráficas» o «diseño gráfico».
- 1725-218-COT26 «DISEÑO Y DIAGRAMACION…»: «diagramación» está en las keywords y debería calzar; no se pudo ver el título completo ni el registro del Radar. No verificado: puede ser término caído o una exclusión en el resto del título.

## Términos caídos del Radar (pedido del coordinador, Compra Ágil, estado Publicada)

Primera ronda con fechas 16-sep a 16-oct; la mayoría cortó a los ~29 s, así que la segunda ronda usó 06 a 16-oct
(una Compra Ágil casi nunca sigue abierta más de diez días; no verificado como regla). Cada ronda: hasta 3
intentos por término. «Resultados» es el conteo del servicio (palabras sueltas); «En título» son los procesos
cuyo nombre contiene todas las palabras del término, dentro de las primeras 60 filas leídas.

| Término | Resultados | En título | Nota |
|---|---|---|---|
| encuesta | 3 | 2 | 895072-128 (suscripción a software de encuestas, bien) y 1725-219 (ya en Radar) |
| economía circular | 11 | 0 | |
| participación ciudadana | 57 | 1 | 5418-73: coffee break de una jornada de participación (no servicio TL) |
| consulta ciudadana | 33 | 0 | |
| guía metodológica | 105 | 0 | |
| diseño editorial | 62 | 0 | |
| manual pedagógico | 23 | 0 | |
| material educativo | 260 | 0 | |
| cuenta pública | 290 | 0 | 696713-81 «Video para cuenta pública» salió por «video» (la búsqueda por esta frase no lo trajo entre las 60 primeras) |
| asesoría comunicacional | 11 | 0 | |
| comunicación institucional | 186 | 0 | |
| comunicación pública | 214 | 0 | |
| consultoría en comunicaciones | 4.171 | 0 | |
| diagnóstico institucional | 177 | 0 | |
| diseño metodológico | 63 | 0 | |
| metodología cualitativa | 7 | 0 | |
| plan comunicacional | 84 | 4 | 1367960-170 a 173, planes de medios; cierran hoy 13:00 |
| capacitación en género | sin respuesta | | |
| monitoreo y evaluación, diseño de instrumento, diálogo social, perspectiva de género, enfoque de género, edición de libro, publicación de libro, corrección de estilo, análisis de datos, memoria institucional, comunicación estratégica, comunicación de riesgo, estudio cualitativo, estudio cuantitativo, estudio de opinión, estudio de percepción, evaluación de impacto, evaluación de programa, evaluación de políticas, gestión de medios, inteligencia de datos, investigación social, plan de comunicaciones, plan de medios | sin respuesta | | 2 rondas × 3 intentos; corte a ~29 s |

Los 0 «en título» son ceros de una lectura parcial (60 filas por término, ordenadas por publicación reciente), no
ausencias verificadas: el servicio no filtra por frase y no se pudo leer el universo completo. Control positivo
de que la lectura funciona: «encuesta» devolvió 1725-219 y «plan comunicacional» los cuatro 1367960.
Para «análisis de datos» hay evidencia indirecta: 2268-167 (Curso Python para análisis de datos) apareció en otra
búsqueda y el Radar no lo trajo.
