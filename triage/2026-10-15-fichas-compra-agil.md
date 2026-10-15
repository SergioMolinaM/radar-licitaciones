# Fichas de Compra Ágil — revisión del 15-oct-2026

Lectura hecha el 15-oct-2026 entre las 10:00 y las 10:31 (hora de Chile, reloj del equipo). Solo lectura: sin login, sin ofertas, sin formularios.

**Fuente y método.** La API del radar (`api2.mercadopublico.cl/v2/compra-agil/{codigo}`, `fetch_detalle` en `src/sources/compra_agil.py`) sí trae el detalle por código, pero pide el ticket `MERCADO_PUBLICO_TOKEN`, que no está en el entorno local (el código no carga `.env`; corre con el secreto de GitHub). Se leyó entonces con Chrome, desde la ficha pública `buscador.mercadopublico.cl/ficha?code=…`, pidiendo al mismo backend que usa esa página (`api.buscador.mercadopublico.cl/compra-agil?action=ficha`) y a su listado de adjuntos (`adjunto.mercadopublico.cl/.../listar/{codigo}`). Los campos de abajo son los que entrega esa respuesta; las citas van entre comillas tal como vienen.

**Tres fichas no cargaron.** 634-393-COT26, 605-188-COT26 y 1614-61-COT26 dieron timeout del servidor (corte a los 29 s) en cuatro intentos cada una, también desde la página normal. De ellas solo se ve el organismo (por el historial) y el nombre de los adjuntos. El resto de sus campos queda «no visible en la ficha»; conviene abrirlas a mano.

**Adjuntos no leídos.** Ninguno se bajó: la descarga es un archivo y no estaba autorizada en esta tarea. Cada ficha lista el nombre de sus adjuntos para que Sergio los baje a mano desde la URL indicada.

**Lectura de montos.** La ficha da un número y un tipo («Estimado» o «Disponible»). No dice si incluye IVA salvo cuando la descripción lo escribe; en esos casos va la cita.

**Cotizaciones recibidas** = conteo público al momento de la lectura.

---

## 1. 1063538-2351-COT26 — Servicio de relator

- **Ficha:** https://buscador.mercadopublico.cl/ficha?code=1063538-2351-COT26
- **Comprador:** Hospital Base Osorno (unidad Bienes y Servicios), RUT 61.602.260-1.
- **Presupuesto:** $200.000 CLP, tipo «Estimado». La descripción dice: «El monto indicado es DISPONIBLE INCLUIDO EL IVA».
- **Cierre:** 1er llamado 15-10-2026 12:30; 2º llamado 16-10-2026 12:41.
- **Qué pide:** relator para el 4 y 5 de noviembre, de 8:30 a 17:00, en Mutual de Seguridad, Guillermo Buhler 1765, Osorno. Producto «Capacitación a empleados»: «Un profesional del territorio, conocedor de este, con experiencia en capacitación en temas de interculturalidad en salud, de la provincia de Osorno», con los temas territorio, determinantes sociales y recomendaciones para la convivencia intercultural. Plazo de entrega: 2 días.
- **Requisitos que podrían dejar fuera a una SpA:** «Se pagara con boleta honorario» (apunta a persona natural); exige ser de la provincia de Osorno y tener experiencia en interculturalidad en salud.
- **Adjuntos:** no tiene.
- **Cotizaciones recibidas:** 1.
- **Calce posible:** capacitación presencial en salud intercultural, fuera de las líneas de TL; el pago por boleta y el arraigo en Osorno pesan más que el tema.

## 2. 634-393-COT26 — Curso de oratoria y comunicación efectiva

- **Ficha:** https://buscador.mercadopublico.cl/ficha?code=634-393-COT26
- **Comprador:** Dirección General de Gendarmería de Chile, Dirección Nacional (según el historial: «Formulario Publicado» el 14-10-2026 12:07).
- **Presupuesto, cierre, descripción, plazo, productos:** no visible en la ficha (el servidor no respondió). El cierre de hoy a las 12:15 viene del listado del coordinador, no de la ficha.
- **Adjuntos:** «Requerimientos Administrativos Oratoria 2.0.docx» y «requerimientos capacitación oratoria.docx».
- **Cotizaciones recibidas:** 0 (visto en la página antes del timeout).
- **Calce posible:** curso de comunicación efectiva para funcionarios; cae en capacitación y comunicación estratégica, y el director tiene docencia. Hay que leer los dos .docx para saber formato, horas y perfil.

## 3. 605-188-COT26 — Intervención en relaciones laborales

- **Ficha:** https://buscador.mercadopublico.cl/ficha?code=605-188-COT26
- **Comprador:** Consejo de Defensa del Estado (historial: publicado el 13-10-2026 13:56).
- **Presupuesto, cierre, descripción, plazo, productos:** no visible en la ficha (timeout en cuatro intentos).
- **Adjuntos:** «compra agil Requerimiento tecnico adquisicion servicio de interve.docx».
- **Calce posible:** por el nombre, intervención organizacional en clima o relaciones laborales; podría tocar encuesta y análisis, pero sin la ficha no se sabe si pide psicólogo organizacional u otro perfil.

## 4. 2495-548-COT26 — Relator curso «Reciclador Base»

- **Ficha:** https://buscador.mercadopublico.cl/ficha?code=2495-548-COT26
- **Comprador:** I. Municipalidad de Coyhaique, Dirección de Desarrollo Comunitario (OTEC Municipal).
- **Presupuesto:** $1.500.000 CLP, tipo «Estimado». La ficha no dice si incluye IVA.
- **Cierre:** 15-10-2026 16:00. Sin segundo llamado.
- **Qué pide:** relatoría y ejecución teórico-práctica del curso «Reciclador Base», sobre «gestión, recolección, clasificación, pretratamiento y comercialización de materiales reciclables». Producto: «Servicio de relatoria 20 horas teoricas y 20 practicas». Plazo de entrega registrado: 1 día. Lugar: Magallanes 283 (Coyhaique).
- **Requisitos que podrían dejar fuera a una SpA:** no visible en la ficha; estarán en los términos de referencia.
- **Adjuntos:** «Contenido Reciclador  Base 40 Horas.docx» y «Terminos_de_Referencia_Relatoria_Reciclador_Base.docx».
- **Cotizaciones recibidas:** 2.
- **Calce posible:** formación de recicladores de base, en el terreno de Ley REP; el título «relator base» oculta que es un curso de reciclaje. Lo práctico (20 h) es presencial en Coyhaique.

## 5. 1549-4316-COT26 — Campañas de simulación de phishing

- **Ficha:** https://buscador.mercadopublico.cl/ficha?code=1549-4316-COT26
- **Comprador:** Servicio de Salud Metropolitano Norte, Hospital San José.
- **Presupuesto:** $2.000.000 CLP, tipo «Estimado». La ficha no dice si incluye IVA.
- **Cierre:** 1er llamado 15-10-2026 16:10; 2º llamado 16-10-2026 16:19.
- **Qué pide:** «a lo menos»: dos campañas de simulación de phishing para 2.500 usuarios; medición de correos enviados, aperturas, clics e intentos de ingreso de datos; informe con indicadores, conclusiones y mejoras; curso de capacitación con evaluación y certificado de aprobación. Producto: «Asesorías Informáticas». Plazo registrado: 1 día.
- **Requisitos que podrían dejar fuera a una SpA:** no visible en la ficha. No tiene adjuntos.
- **Cotizaciones recibidas:** 2.
- **Calce posible:** mezcla plataforma de envío y medición, informe y capacitación; lo técnico de ciberseguridad (simulación de phishing a 2.500 cuentas) es una especialidad que TL no ha ofrecido.

## 6. 1078247-1-COT26 — Diseño y diagramación del informe de Acceso a la Justicia

- **Ficha:** https://buscador.mercadopublico.cl/ficha?code=1078247-1-COT26
- **Comprador:** Subsecretaría del Ministerio de Justicia (unidad «Administración de fondos»).
- **Presupuesto:** $1.800.000 CLP, tipo «Estimado». La ficha no dice si incluye IVA.
- **Cierre:** 1er llamado 16-10-2026 08:00; 2º llamado 17-10-2026 20:45.
- **Qué pide:** «Servicio de diseño y diagramación del Informe Final del Estudio de Acceso a la Justicia en Chile. Detalles en documento adjunto». Plazo registrado: 12 días. Producto: «Diseño gráfico».
- **Requisitos que podrían dejar fuera a una SpA:** no visible en la ficha.
- **Adjuntos:** «TDR Diseñador gráfico_estudio Chile-México V4.docx» (el nombre sugiere perfil de diseñador; no leído).
- **Cotizaciones recibidas:** 4.
- **Calce posible:** diagramación de informe de estudio con datos; TL hace informes y visualización. Ya tiene 4 cotizaciones.

## 7. 1614-61-COT26 — Curso de IA en gestión directiva

- **Ficha:** https://buscador.mercadopublico.cl/ficha?code=1614-61-COT26
- **Comprador:** Superintendencia de Electricidad y Combustibles (historial: publicado el 13-10-2026 09:45).
- **Presupuesto, cierre, descripción, plazo, productos:** no visible en la ficha (timeout en cuatro intentos). Nombre y cierre (16-oct 10:00) vienen del listado del coordinador.
- **Adjuntos:** «SC-245.pdf».
- **Calce posible:** capacitación en IA para directivos de un servicio público; está en el centro de la línea de capacitación en IA. Sin ficha no se ve monto, horas ni perfil exigido: es la que más conviene abrir a mano.

## 8. 1485943-35-COT26 — Diseñador para proyectos SEDE RM

- **Ficha:** https://buscador.mercadopublico.cl/ficha?code=1485943-35-COT26
- **Comprador:** BAJ Metropolitana, Corporación Cultural Balmaceda Arte Joven, Dirección Regional Metropolitana.
- **Presupuesto:** $380.000 CLP, tipo «Disponible». La ficha no dice si incluye IVA.
- **Cierre:** 1er llamado 16-10-2026 10:00; 2º llamado 18-10-2026 03:32.
- **Qué pide:** diseño gráfico de piezas de difusión para tres actividades: «Aquí se Toka - 16 horas», «Inauguración de Residencias de Artes Visuales - 8 horas», «Escena Emergente - 16 horas» (total 40 h); propuestas, adaptaciones a formatos digitales e impresos, archivos finales y editables. Plazo registrado: 5 días.
- **Requisitos:** «REQUISITO: ADJUNTAR DOSSIER». Lo demás no visible en la ficha.
- **Adjuntos:** «TR SERVICIO DISEÑO 2026.docx.pdf».
- **Cotizaciones recibidas:** 0.
- **Calce posible:** diseño gráfico por horas para programación cultural; encargo chico de diseño puro, sin datos ni plataforma.

## 9. 831-222-COT26 — Créditos API Anthropic Claude

- **Ficha:** https://buscador.mercadopublico.cl/ficha?code=831-222-COT26
- **Comprador:** Gobierno Regional de la Región del Biobío.
- **Presupuesto:** $2.500.000 CLP, tipo «Estimado». La ficha no dice si incluye IVA.
- **Cierre:** 1er llamado 16-10-2026 10:00; 2º llamado 19-10-2026 07:32.
- **Qué pide:** créditos de uso de la API de Anthropic «para incorporar y evaluar funcionalidades de inteligencia artificial en sistemas institucionales»: análisis de información, clasificación de antecedentes, resúmenes y revisión preliminar de solicitudes. Producto: «Software de gestión de licencias». Plazo registrado: 5 días.
- **Requisitos:** no visible en la ficha.
- **Adjuntos:** «especificaciones-REQ-2026-0503.pdf».
- **Cotizaciones recibidas:** 2.
- **Calce posible:** reventa de créditos; el margen es bajo y pasa por facturar un servicio extranjero. Lo interesante es el uso descrito (clasificar y resumir solicitudes), que es trabajo de IA aplicada que el Gore no está comprando acá.

## 10. 3512-182-COT26 — Asesoría para el Plan Comunal de Seguridad Pública de Illapel 2027-2031

- **Ficha:** https://buscador.mercadopublico.cl/ficha?code=3512-182-COT26
- **Comprador:** I. Municipalidad de Illapel (Departamento de Finanzas Municipal).
- **Presupuesto:** $7.000.000 CLP, tipo «Estimado». La ficha no dice si incluye IVA.
- **Cierre:** 1er llamado 16-10-2026 16:00; 2º llamado 18-10-2026 15:29.
- **Qué pide:** «asesoría técnica y jurídica especializada» para formular el Plan Comunal de Seguridad Pública 2027–2031, «conforme a la Ley N.º 18.695, la Ley N.º 20.965, las modificaciones introducidas por la Ley N.º 21.802» (número citado de la ficha, no verificado) y orientaciones de la Subsecretaría de Prevención del Delito, incluido el diagnóstico comunal. Plazo registrado: 2 días (dato del sistema; las bases técnicas dirán el real).
- **Requisitos que podrían dejar fuera a una SpA:** pide componente «jurídico», que TL no tiene en casa. El resto no visible en la ficha.
- **Adjuntos:** «BASES TECNICAS ASESORIA.pdf».
- **Cotizaciones recibidas:** 1.
- **Calce posible:** diagnóstico comunal con datos, participación y redacción de plan; el componente jurídico pediría un abogado asociado.

## 11. 5418-72-COT26 — Mapa de actores, Planes de Zonas en Desarrollo, Los Ríos

- **Ficha:** https://buscador.mercadopublico.cl/ficha?code=5418-72-COT26
- **Comprador:** Gobierno Regional de Los Ríos.
- **Presupuesto:** $7.172.000 CLP, tipo «Disponible». La ficha no dice si incluye IVA.
- **Cierre:** 1er llamado 16-10-2026 22:00; 2º llamado 19-10-2026 04:27.
- **Qué pide:** «Consultoría de Mapa de Actores para el proceso de formulación e implementación de los Planes de Zonas en Desarrollo de la Región de Los Ríos». Plazo: «El plazo máximo de ejecución será de 70 días corridos»; los 50 días hábiles de la plataforma son «únicamente referenciales». Producto: «Asesorías en gestión estratégica».
- **Requisitos:** no visible en la ficha; están en las especificaciones técnicas.
- **Adjuntos:** «Especificaciones Técnicas_Mapa de Actore_FINAL.14.10.26.pdf» y «Anexos.docx».
- **Cotizaciones recibidas:** 0.
- **Calce posible:** mapa de actores para planificación territorial: levantamiento, participación y visualización de redes; se acerca a la línea de consulta ciudadana (DDLS) y análisis. Es la de monto más alto junto con Illapel y el CFT.

## 12. 1491370-78-COT26 — Licencia Claude Pro

- **Ficha:** https://buscador.mercadopublico.cl/ficha?code=1491370-78-COT26
- **Comprador:** la ficha dice «Proyecto ING2530001 DECANAT FACULTAD DE INGENIERÍA», unidad «DECANATO FACULTAD DE INGENIERÍA»; dirección Benavente 980. La universidad no se nombra en la ficha.
- **Presupuesto:** $286.000 CLP, tipo «Disponible». La ficha no dice si incluye IVA.
- **Cierre:** 1er llamado 17-10-2026 12:00; 2º llamado 20-10-2026 13:39.
- **Qué pide:** una licencia «Claude AI Pro 12 meses o equivalente técnico» para el proyecto RocketLab 2026 (convenio N.° CI-2026-010). «El oferente deberá proveer suscripción al plan Claude AI Pro oficial de Anthropic. Debe permitir selección de modelo (ej: Sonnet o superior)». Plazo registrado: 5 días.
- **Adjuntos:** «02. Formato de EETT Compra agil.docx».
- **Cotizaciones recibidas:** 2.
- **Calce posible:** reventa de una suscripción individual; monto chico.

## 13. 609-112-COT26 — Bolsa de créditos de IA por API (INDAP)

- **Ficha:** https://buscador.mercadopublico.cl/ficha?code=609-112-COT26
- **Comprador:** Instituto de Desarrollo Agropecuario (INDAP).
- **Presupuesto:** $4.000.000 CLP, tipo «Disponible». El producto dice «por hasta $4.000.000 impuestos incluidos, con un saldo neto mínimo acreditable a favor de INDAP de USD $3.000».
- **Cierre:** 1er llamado 19-10-2026 08:30; 2º llamado 25-10-2026 00:32.
- **Qué pide:** bolsa de créditos para servicios de IA por API, «(OpenAI o equivalente técnico)», con lenguaje natural, visión e IA generativa, para pruebas, desarrollos e integraciones. Plazo registrado: 5 días.
- **Adjuntos:** «TDR TOKEN OPEN AI.pdf».
- **Cotizaciones recibidas:** 3.
- **Calce posible:** reventa de créditos con saldo mínimo de USD 3.000 dentro de $4.000.000 con impuestos; el margen sale de la diferencia cambiaria y queda estrecho.

## 14. 1075952-31-COT26 — Licencias Claude Pro (Superintendencia de Educación Superior)

- **Ficha:** https://buscador.mercadopublico.cl/ficha?code=1075952-31-COT26
- **Comprador:** Superintendencia de Educación Superior.
- **Presupuesto:** $2.800.000 CLP, tipo «Estimado»; la descripción dice «Presupuesto referencial 2.800.000 CLP, incluidos impuestos y todos los costos asociados».
- **Cierre:** 1er llamado 19-10-2026 12:00; 2º llamado 24-10-2026 14:02.
- **Qué pide:** «10 licencias de Claude Pro individuales por 12 meses», vigencia hasta 12 meses desde la activación. Plazo registrado: 3 días.
- **Adjuntos:** «1. TDR_LICENCIAS IA.pdf».
- **Cotizaciones recibidas:** 3.
- **Calce posible:** reventa de licencias; comprador del sector educación superior, cercano a la línea de educación de TL.

## 15. 1075952-32-COT26 — Bolsa de tokens (Superintendencia de Educación Superior)

- **Ficha:** https://buscador.mercadopublico.cl/ficha?code=1075952-32-COT26
- **Comprador:** Superintendencia de Educación Superior.
- **Presupuesto:** $2.800.000 CLP, tipo «Estimado»; «incluidos impuestos y todos los costos asociados».
- **Cierre:** 19-10-2026 12:00. Sin segundo llamado.
- **Qué pide:** «Una Bolsa General única, prepagada y trazable, equivalente a USD 2.000 en créditos de consumo», vigencia hasta 12 meses o hasta agotarse. La ficha no nombra proveedor de IA. Plazo registrado: 3 días.
- **Adjuntos:** «1. TDR_TOKEN.pdf».
- **Cotizaciones recibidas:** 2.
- **Calce posible:** reventa de créditos, igual que la anterior.

## 16. 3447-457-COT26 — Suscripción a IA generativa (Alto Hospicio)

- **Ficha:** https://buscador.mercadopublico.cl/ficha?code=3447-457-COT26
- **Comprador:** Municipalidad de Alto Hospicio, Dirección de Administración y Finanzas.
- **Presupuesto:** $6.000.000 CLP, tipo «Disponible». La ficha no dice si incluye IVA.
- **Cierre:** 1er llamado 19-10-2026 15:00; 2º llamado 24-10-2026 12:10.
- **Qué pide:** suscripción de 12 meses a «Plataforma de Inteligencia Artificial Generativa, tipo ChatGPT o equivalente» para la Oficina de Transformación Digital. Producto (x4 en la ficha): «Contratación de 10 suscripciones ChatGPT Business para la Municipalidad de Alto Hospicio, por un período de 12 meses». Plazo registrado: 3 días.
- **Adjuntos:** «MEMO 1248.2026 - AUTORIZA COMPRA CHAT GPT.pdf» y «TÉRMINO DE REFERENCIA (MEMO 1248).pdf».
- **Cotizaciones recibidas:** 3.
- **Calce posible:** reventa de licencias de OpenAI; una oficina de transformación digital que compra IA puede ser cliente de capacitación después.

## 17. 855-34-COT26 — Publicidad para difusión de postulaciones y matrículas 2027

- **Ficha:** https://buscador.mercadopublico.cl/ficha?code=855-34-COT26
- **Comprador:** Junta Nacional de Jardines Infantiles (JUNJI), Dirección Regional de Magallanes y de la Antártica Chilena.
- **Presupuesto:** $500.000 CLP, tipo «Disponible». La ficha no dice si incluye IVA.
- **Cierre:** 1er llamado 20-10-2026 11:00; 2º llamado 26-10-2026 05:53.
- **Qué pide:** «servicio de publicidad en un medio de comunicación social multimedia (radio, televisión y diario de papel digital), de alcance regional» para la campaña de postulaciones y matrículas 2027. Dirección de entrega: «MEDIO DE COMUNICACION PROVEEDOR ADJUDICADO». Plazo registrado: 10 días. Producto: «Publicidad en televisión».
- **Requisitos que podrían dejar fuera a una SpA:** el oferente tiene que ser el medio de comunicación con cobertura en Magallanes.
- **Adjuntos:** «TDR PUBLICIDAD.pdf», «Anexo N1 Declaración Jurada.docx», «Anexo N2 Clausula proveedores.docx», «Anexo N3 Programa de Integridad.docx», «Anexo N4  economica de la oferta.docx», «CDP PUBLICIDAD.pdf».
- **Cotizaciones recibidas:** 0.
- **Calce posible:** compra de espacio en un medio regional; TL no es medio.

## 18. 1317954-9-COT26 — Estudio de clima laboral 2026, Empresa Portuaria Coquimbo

- **Ficha:** https://buscador.mercadopublico.cl/ficha?code=1317954-9-COT26
- **Comprador:** Empresa Portuaria Coquimbo.
- **Presupuesto:** $1.000.000 CLP, tipo «Estimado». La ficha no dice si incluye IVA.
- **Cierre:** 1er llamado 20-10-2026 23:55; 2º llamado 28-10-2026 08:52.
- **Qué pide:** encuesta estructurada de clima (liderazgo, comunicación, motivación, condiciones de trabajo, bienestar), comparación con el estudio de 2025, presentación ejecutiva al Directorio y al equipo de gestión, y plan de trabajo con medidas de mejora. Plazo registrado: 24 días. Producto: «Relaciones laborales y sindicales».
- **Requisitos:** no visible en la ficha.
- **Adjuntos:** «Cotización Clima Laboral 2026 .pdf».
- **Cotizaciones recibidas:** 2.
- **Calce posible:** encuesta, análisis comparativo y presentación ejecutiva, que es la línea de encuestas y análisis de TL; depende de tener el instrumento y la base de 2025.

## 19. 1109692-245-COT26 — Factibilidad de la oferta formativa del CFT Estatal de Magallanes

- **Ficha:** https://buscador.mercadopublico.cl/ficha?code=1109692-245-COT26
- **Comprador:** Centro de Formación Técnica Estatal de Magallanes.
- **Presupuesto:** $7.200.000 CLP, tipo «Estimado». La ficha no dice si incluye IVA.
- **Cierre:** 21-10-2026 16:00. Sin segundo llamado.
- **Qué pide:** estudio de factibilidad, pertinencia territorial y plan de negocios para expandir la oferta formativa hacia Puerto Natales y Punta Arenas. El producto detalla: diagnóstico institucional, estudio de demanda educativa, encuestas, benchmarking, propuesta de oferta académica, integración ChileValora, análisis de financiamiento, modelo financiero a 5 años, política financiera, matrices de factibilidad y riesgos, estrategia de captación y hoja de ruta 2027-2031. Plazo registrado: 60 días.
- **Requisitos:** «Entregables y requisitos de admisibilidad según documento de especificaciones técnicas adjunto»; no visibles en la ficha.
- **Adjuntos:** «Anexo N°1 Identificación del oferente.docx», «Criterios de admisibilidad, desempate, Forma de entrega, Facturac.pdf», «ESPECIFICACIONES TÉCNICAS SERVICIO PLAN DE NEGOCIOS CFT DE MAGALL.pdf».
- **Cotizaciones recibidas:** 0.
- **Calce posible:** estudio de demanda educativa con encuestas y análisis territorial, cerca de la línea de educación; el modelo financiero a 5 años y el plan de negocios piden un perfil económico que habría que sumar.

---

## Pendiente para Sergio

- Abrir a mano 634-393 (cierra hoy 12:15), 605-188 y 1614-61: su ficha no cargó desde el servidor.
- Adjuntos que deciden el calce y que no se leyeron: los dos .docx de oratoria (634-393), el TDR de Reciclador Base (2495-548), el TDR del diseño del informe de Justicia (1078247-1), SC-245.pdf (1614-61), las bases de Illapel (3512-182), las especificaciones de Los Ríos (5418-72) y las del CFT de Magallanes (1109692-245).
- **Nota técnica para el radar:** la ficha pública responde con dos claves que están en el JS del buscador (`x-api-key` para `action=ficha`/`historial`, `user_key` para el listado de adjuntos). El listado de adjuntos responde en menos de 100 ms; la ficha tarda 8-29 s y corta a los 29 s, igual que la API v2.

---

## Adjuntos leídos (15-oct tarde)

Lectura completa de los adjuntos bajados a `triage/bases-2026-10-15/<código>/`. PDF con pypdf; .docx con python-docx (párrafos, tablas, encabezados y pies; las imágenes incrustadas se revisaron y son logos). El PDF de Los Ríos es escaneado (0 caracteres de texto en las 18 páginas): se renderizó cada página a imagen con PyMuPDF y se leyó visualmente, sin OCR. Las páginas citadas son las del PDF; en los .docx, que no tienen paginación fija, se cita la sección. Lo que el adjunto no dice va como «no está en el adjunto». No hay veredicto de descarte: decide Sergio.

### 1614-61-COT26 — SEC, curso «Uso e Impacto de la Inteligencia Artificial en la Gestión Directiva y Toma de Decisiones» (SC-245.pdf, 2 páginas)

- **Monto:** «Presupuesto máximo: $3.000.000» (p. 1, §2). No dice si incluye IVA. Dos líneas antes hay una viñeta suelta: «(impuestos o exención según corresponda)» (p. 1), sin cifra al lado; no aclara si el tope es bruto o neto.
- **Plazo:** «Período de Ejecución: Noviembre a mediados de diciembre de 2026» (p. 1). 16 horas pedagógicas sincrónicas; sugerido «8 sesiones de 2 horas (2 sesiones semanales durante 4 semanas)». Modalidad «Telemática Sincrónica (100% Clases en vivo…)». Público: «20 Jefaturas de alto nivel (Nivel Directivo)».
- **Contenidos mínimos (p. 1):** fundamentos de IA; IA generativa en el sector público; uso responsable, ética, probidad y protección de datos; herramientas de productividad directiva; ingeniería de prompts; informes, minutas y presentaciones con IA; IA para gestión y decisiones; automatización de procesos; gestión del cambio; ejercicios con casos institucionales. Al menos 60% del tiempo en talleres prácticos (p. 1, §3). Herramientas libres o licencias temporales («ChatGPT, Claude, Copilot, Gemini, Perplexity, Canva/PowerPoint AI»).
- **Entregables (p. 2, §7):** plan de trabajo y cronograma a los 5 días de adjudicado; manual y material didáctico en PDF (guías, repositorio de prompts, presentaciones) antes del inicio; grabaciones en la plataforma dentro de 48 h de cada clase; informe final de gestión académica (asistencia, notas, encuestas de satisfacción, sugerencias). Cada participante entrega un «Caso de Uso Directivo» o catálogo de prompts, evaluado de 1,0 a 7,0 (p. 1-2). Evaluación diagnóstica inicial, asistencia mínima 80%, certificado digital (p. 2, §6).
- **Infraestructura exigida (p. 2, §5):** videoconferencia con licencia empresarial (Zoom, Teams o Meet) con salas pequeñas, votaciones y grabación HD; LMS (Moodle, Canvas u otro) 24/7 durante el curso y 30 días después; un coordinador técnico en línea durante el 100% de las clases.
- **Perfil (p. 1, §4):** proveedor u OTEC con «Certificación de Calidad vigente (NCh 2728 si aplica por franquicia SENCE o registro público equivalente)» y «Experiencia demostrable en capacitación a cuadros directivos o de alta dirección en el sector público o privado (mínimo 3 años)». Relator: profesional universitario «(Ingeniería, Administración Pública, Ciencia de Datos, Derecho con mención en Tecnología, o afines) con grado de Magíster o especialización relevante»; al menos 3 años en capacitación o docencia ejecutiva en tecnologías disruptivas, transformación digital o IA; mínimo 4 años en proyectos de gestión, tecnología, innovación o transformación digital. El adjunto no distingue persona natural o empresa: habla de «OTEC o Proveedor».
- **Criterios de evaluación de ofertas:** no está en el adjunto. La §6 «Criterios de evaluación y aprobación» es de los participantes, no de las ofertas.
- **Lo que podría dejar fuera a TL:** la NCh 2728 está redactada como condicional («si aplica por franquicia SENCE»); no queda claro si la exigen a un proveedor que no usa franquicia. Los 3 años de capacitación a directivos se acreditan como empresa o equipo, y el adjunto no dice con qué documento. El título de periodista no está en la lista del relator; entraría solo como «afines», y el doctorado cubre el grado. Pide licencia empresarial de videoconferencia y un LMS: si TL no los tiene, son costo del servicio.
- **Inconsistencia del adjunto:** la «Justificación de la solicitud» (p. 2) habla de «convivencia laboral, inclusión, igualdad de oportunidades y perspectiva de género», no de IA. Parece copiada de otra solicitud; conviene preguntarlo en el foro si hay plazo.
- **Calce posible:** curso de IA generativa para directivos públicos, 16 h en línea, con material de prompts y casos aplicados: es la línea de capacitación en IA de TL tal cual. Lo que hay que resolver es la acreditación (NCh 2728 y años con directivos).

### 5418-72-COT26 — Gobierno Regional de Los Ríos, «Consultoría de Mapa de Actores para el proceso de formulación e implementación de los Planes de Zonas en Desarrollo» (Especificaciones Técnicas, 18 páginas, escaneado)

- **Monto:** «$7.172.000.- impuestos incluidos» (p. 7, §II.6) y «$7.172.000.- con IVA incluido» (p. 8, §III.1). Suma alzada.
- **Plazo:** «plazo máximo de 70 días corridos», que «incluye los días de revisión y corrección» (p. 7, §8). Día 1 lo fija la Inspectoría Técnica por correo después de la aceptación de la OC; la OC se acepta dentro de 24 h hábiles o puede rechazarse (p. 7). Por etapa (p. 9): Informe 1 en 20 días, Informe 2 en 30, Informe 3 en 20.
- **Territorio:** provincias de Valdivia (Mariquina, Lanco, Máfil, Panguipulli, Los Lagos, Corral, Paillaco) y del Ranco (La Unión, Río Bueno, Lago Ranco, Futrono), con Valdivia comuna incluida en el análisis (p. 2-3). El adjunto no dice si el trabajo de campo debe ser presencial: no está en el adjunto.
- **Entregables (p. 6-7):**
  - Informe 1, «Identificación, Caracterización de Instancias y Respectivos Actores»: metodología, análisis normativo y de contexto del modelo de gobernanza, estado de las organizaciones por comuna, y listado de actores con rol, sector, ámbito, nivel de representación y capacidades.
  - Informe 2, «Categorización por Interés e Influencia y Análisis de Relaciones»: matriz poder/interés, carácter estratégico, dinámicas (alianzas, conflictos, dependencias), tipo de vínculos, capacidad de alianzas y restricciones.
  - Informe 3, «Bases de Datos y Estrategias de Participación y Seguimiento»: listado de actores con nombre, cargo, correo, celular, comuna, nivel de influencia e instancias actuales y recomendadas; acciones diferenciadas por grupo; propuesta de evaluación participativa y «mapeo ágil» periódico.
  - Levantamiento mínimo: encuesta a 150 actores o el 50% de la base regional, y entrevistas en profundidad a 20 actores o el 5% (p. 6).
  - Formato: PDF firmado y Word; presupuesto y cronograma en Excel y PDF firmado (p. 8, §9). Informes con portada, índice, resumen ejecutivo, conclusiones y bibliografía, en tercera persona (p. 7).
- **Pago:** 25% / 50% / 25% contra cada informe aprobado, dentro de 30 días corridos desde la factura (p. 8-9).
- **Perfil:**
  - **Oferente (admisibilidad, p. 4, §II.1):** «experiencia comprobable de, al menos 5 años» en consultorías sobre participación ciudadana, investigación social, análisis de redes sociales, desarrollo social, gestión pública, métodos de investigación social, gestión de proyectos y/o políticas públicas; solo cuentan consultorías de los últimos 5 años; «mínimo de tres (3) experiencias», o la oferta es inadmisible. Se acredita con OC con recepción conforme, contratos, certificados, facturas con antecedentes u otro documento (p. 4), en el Anexo N.º 1 (p. 16).
  - **Equipo (p. 5, §II.3):** «título profesional del área de las Ciencias Económicas, Sociales o Políticas»; posgrado deseable; «al menos, 5 años de experiencia» en análisis de actores, procesos participativos, investigación social, mapas de poder o asesorías en descentralización o gobernanza territorial. Se valora experiencia previa en Gobiernos Regionales o municipios. Documentos: título, posgrado, CV actualizado «hasta el 31 de agosto de 2026», certificados de experiencias y de capacitaciones. Anexo N.º 2 (p. 17).
  - **Persona natural o empresa:** admite «Equipo Profesional o Profesional» (p. 5); los estados de pago los firma el «Representante Legal de la empresa» (p. 8).
- **Propuesta técnica:** máximo 5 páginas (Anexo N.º 3, p. 18), con metodología, componentes, organización del trabajo y resultados.
- **Criterios de evaluación (p. 11, §9; detalle p. 11-14):** Propuesta Técnica 50% (base 100/75/50/25/0 más hasta 15 puntos por reducir plazo, ampliar cobertura de actores o agregar variables; se divide por 115); Experiencia del Oferente 10% (100 pts con 8 o más consultorías, 75 con 6-7, 50 con 5, 25 con 4, 0 con 3); Formación académica del equipo 10% (100 con posgrado en Ciencias Económicas, Sociales o Políticas, 50 sin posgrado, 0 si no es del área); Experiencia del equipo 25% (100 con 8 o más años, 50 con 5, 0 con menos de 5); Precio 5% (precio más bajo / ofertado × 100). Comportamiento contractual anterior descuenta 3 a 5 puntos por sanción (p. 13-14). Desempate: propuesta técnica, experiencia del oferente, equipo técnico, menor precio (p. 14).
- **Lo que podría dejar fuera a TL:**
  - El umbral de admisibilidad: 5 años de experiencia del oferente y 3 consultorías de las materias listadas dentro de los últimos 5 años, acreditadas con documentos. Si la experiencia que cuenta es la de la SpA y no la del director, la antigüedad de TL y sus contratos documentables deciden; no lo verifiqué contra registro.
  - El título del equipo: «Ciencias Económicas, Sociales o Políticas». Si periodismo cae dentro de Ciencias Sociales lo decide la comisión; con 0 en formación el equipo no queda inadmisible por puntaje, pero el requisito del §II.3 se lee como condición. Es pregunta para el foro.
  - «La oferta deberá dar cumplimiento al 100% de los requerimientos» como requisito de admisibilidad (p. 8).
  - Giro verificado en el SII y «relacionado con el objeto» (p. 14).
  - Si no hay trabajadores dependientes, declaración jurada ante notario con el primer estado de pago (p. 10).
- **Datos personales:** el Informe 3 es una base nominativa con correo y celular de 150 o más personas (p. 7). Requiere tratamiento conforme a la Ley 19.628 (y la 21.719 desde el 1-dic-2026); la ejecución cae en esa transición.
- **Calce posible:** levantamiento con encuesta, entrevistas, análisis de redes de actores y una base de datos de seguimiento, con 50% del puntaje en la propuesta técnica y solo 5% en precio: es trabajo de datos y participación cercano a la consulta ciudadana. La admisibilidad por experiencia de 5 años es el filtro.

### 634-393-COT26 — Gendarmería de Chile, curso de Oratoria y Comunicación Efectiva (Requerimientos Administrativos Oratoria 2.0.docx)

- **Monto:** «MONTO TOTAL ESTIMADO ADQUISICIÓN: $2.990.000.- IVA Incluido» (encabezado del Anexo N.º 1). Expediente «EXP. N° 485/2025».
- **Plazo, horas, participantes, modalidad, lugar y contenidos:** no está en el adjunto. Este archivo es solo administrativo; la ficha listaba un segundo adjunto, «requerimientos capacitación oratoria.docx», que no está en la carpeta bajada.
- **Entregables:** no está en el adjunto. La cotización debe traer vigencia de la oferta, monto unitario, total neto y con impuesto, plazo de entrega, metodología, «todo lo requerido en anexos técnicos» y contacto (sección «De la oferta»).
- **Perfil:** no está en el adjunto. Pide facturar a Gendarmería (sección «Pago»), lo que supone factura; no dice nada de persona natural.
- **Criterios de evaluación (sección «Criterios de evaluación»):** Precio 80% (precio más ventajoso × 10 / precio ofrecido); Experiencia en Oratoria y Comunicación Efectiva 18% (10 puntos con 3 o más contratos, 5 con 1 o 2, 0 sin contratos), acreditada «con órdenes de compra en estado aceptadas o con recepción conforme (últimos 24 meses)»; Políticas de Sustentabilidad 2% (Formulario N.º 01 más medios de verificación). Desempate: menor precio, mayor experiencia, primera cotización ingresada.
- **Multas (sección «Multas y sanciones»):** 2% diario sobre lo incumplido, máximo 20 días, mínimo 1 UTM, tope 30% del contrato.
- **Lo que podría dejar fuera a TL:** la experiencia solo cuenta con OC de Mercado Público en oratoria o comunicación efectiva de los últimos 24 meses; sin ellas el 18% queda en 0 y la competencia se decide por precio (80%). El 2% de sustentabilidad pide una declaración jurada y medios de verificación.
- **Cierre:** el informe de la mañana lo registra hoy a las 12:15 según el listado del coordinador; el adjunto no trae fecha de cierre.
- **Calce posible:** capacitación en comunicación para funcionarios; el contenido técnico está en el otro .docx, que falta.

### 605-188-COT26 — Consejo de Defensa del Estado, intervención en relaciones laborales y gestión de conflictos (Requerimiento técnico .docx)

- **Monto:** «$3.500.000.- (Tres millones quinientos mil pesos) impuestos incluidos» (§III). Pago único contra recepción conforme del informe final.
- **Plazo (§I.5):** inicio «desde la segunda quincena del mes de octubre»; la multa A fija el inicio para «la tercera semana del mes de octubre del año 2026» (§IV). Calendario de 7 semanas: encuadre y DISC (sem. 1), cuatro sesiones grupales (sem. 2-5), dos sesiones con la jefatura (sem. 3 y 5), seguimiento (sem. 6), informe (sem. 7).
- **Entregables:** reunión presencial de encuadre de 1 h; diagnóstico con instrumento conductual tipo DISC y ajuste de la propuesta; cuatro talleres de 3 h (comunicación, escucha, conversaciones difíciles, retroalimentación, conflictos, acuerdos); dos sesiones de 3 h con la jefatura subrogante; acuerdos de funcionamiento en conductas observables; seguimiento de 1,5 h a los 15 días; informe final (§I.2 y §I.6). Todo presencial en Agustinas 1225, Santiago. 12 participantes, área de litigio. Firma de acuerdo de confidencialidad.
- **Perfil (§I.4 y §II):** «profesión de sicólogo/a o carrera afín con estudios de postgrado», experiencia en intervención de equipos del sector público. Para ofertar exige «certificado de título de psicólogo/a y de sus estudios de postgrado», al menos 2 certificados de clientes del sector público «del nivel central» por intervenciones de equipos en los últimos cuatro años, y CV de los últimos 6 años.
- **Criterios de evaluación:** no está en el adjunto.
- **Multas (§IV):** 2% por día de retraso en el inicio y 2% por día en el informe final; tope 20%.
- **Contexto que eleva el riesgo (§I):** el equipo tiene «antecedentes asociados a enfermedades profesionales» y «acciones judiciales de tutela laboral».
- **Lo que podría dejar fuera a TL:** el requisito para ofertar es el certificado de título de psicólogo/a; «carrera afín» aparece en el §I.4, pero el §II pide el título de psicólogo/a sin alternativa. Los dos certificados de clientes del nivel central en intervención de equipos. El inicio en la tercera semana de octubre, que es la próxima.
- **Calce posible:** intervención psicosocial presencial; TL no tiene psicólogo en casa. Solo entraría con un profesional asociado que reúna título y certificados.

### 1317954-9-COT26 — Empresa Portuaria Coquimbo, estudio de clima laboral 2026 (Cotización Clima Laboral 2026.pdf, 10 páginas)

- **Monto:** «monto disponible máximo de $1.000.000.- CLP (impuestos incluidos, sea IVA o retención de boleta de honorarios)» (p. 9, §2). Suma alzada, con «detalle por horas de trabajo» y desglose por etapa (p. 9).
- **Plazo (p. 7, Tabla 2):** Etapa 1 del 27-oct al 6-nov; Etapa 2 del 9 al 20-nov; Etapa 3 del 23 al 27-nov de 2026. La entrega final del 27-nov no se mueve (p. 7). Recepción de propuestas el martes 20-10-2026, ampliable al 23-10 si no hay ofertas; adjudicación el 26-10 (p. 4).
- **Entregables (p. 6):** informe final 2026, comparación con 2025, presentación ejecutiva y plan de trabajo con medidas de mejora, con responsables y plazos (p. 5). Encuesta a toda la dotación, «dotación referencial: 19 trabajadores», con tasa de respuesta mínima esperada de 80%; modalidad «[online / presencial / mixta]», campo sin completar en el documento (p. 5). Comparabilidad con 2025 usando «el mismo instrumento o dimensiones equivalentes» (p. 5). Presentación al Directorio (p. 5).
- **Pago:** 100% al final, después de la presentación al Directorio y la recepción conforme (p. 7 y p. 10, §5.2).
- **Perfil:** no está en el adjunto ningún título ni años mínimos. Pide detallar el consultor o equipo y «su experiencia en la realización de estudios de clima laboral o diagnósticos organizacionales, idealmente en empresas públicas o del sector portuario» (p. 9, §3). Admite factura o boleta de honorarios (p. 9).
- **Criterios de evaluación (p. 9, §4.1):** «Precio (40%), Experiencia del consultor o equipo en estudios similares (40%) y Metodología y plan de trabajo propuesto (20%)». Empate: mayor puntaje en Experiencia.
- **Multas (p. 7-8):** 1% diario por atraso (tope 20 días), 5% por incumplimiento técnico, tope total 20%.
- **Datos:** anonimato de los trabajadores y tratamiento de datos personales «conforme a la normativa vigente»; bases, instrumentos y resultados son propiedad de EPCO (p. 4).
- **Lo que podría dejar fuera a TL:** el 40% de experiencia en clima laboral o diagnósticos organizacionales; sin estudios previos de ese tipo, ese criterio queda bajo. Con 19 trabajadores, el anonimato por subgrupo es frágil y la comparación con 2025 depende del instrumento que EPCO entregue (p. 4).
- **Calce posible:** encuesta corta, análisis comparativo y presentación ejecutiva, que es la línea de encuestas de TL; $1.000.000 con impuestos y pago único al final.

### 1109692-245-COT26 — CFT Estatal de Magallanes, factibilidad y plan de negocios (Criterios de admisibilidad… .pdf, 2 páginas; Anexo N.º 1 .docx)

- **Monto, plazo, entregables, perfil y criterios de evaluación:** no está en los adjuntos leídos. Están en «ESPECIFICACIONES TÉCNICAS SERVICIO PLAN DE NEGOCIOS CFT DE MAGALL.pdf», que todavía no está en la carpeta.
- **Admisibilidad (p. 1):** se revisa la Ficha del Proveedor en el Registro de Proveedores; las actividades económicas declaradas deben ser «concordantes con los bienes y/o servicios requeridos», o la oferta es inadmisible. El comprador no responde por fichas desactualizadas, aunque sea por fallas de interoperabilidad con el SII.
- **Desempate (p. 1):** 1) Sello Empresa Mujer; 2) menos sanciones en 24 meses; 3) presentar el Anexo N.º 1. Si persiste, se cancela y se vuelve a publicar.
- **Facturación y pago (p. 1-2):** factura o boleta de honorarios contra recepción total conforme, con el N.º de OC en la glosa; los documentos emitidos antes se rechazan; pago dentro de 30 días corridos.
- **Anexo N.º 1:** formulario de identificación (razón social, RUT, domicilio, ciudad, teléfono, correo y encargado de la propuesta). Repite las condiciones de factura y pago.
- **Lo que podría dejar fuera a TL:** que las actividades económicas registradas no calcen con un estudio de factibilidad y plan de negocios. Las de TL no las revisé en esta tarea.
- **Calce posible:** sin las especificaciones técnicas no se puede juzgar; queda pendiente de ese PDF.

### Pendientes que dejan estos adjuntos

- 634-393: falta «requerimientos capacitación oratoria.docx», que trae lo técnico.
- 5418-72: falta «Anexos.docx» de la ficha (los tres anexos sí vienen al final del PDF, p. 16-18).
- 1109692-245: faltan las especificaciones técnicas.
- 1614-61: el criterio de evaluación de ofertas no viene en SC-245; puede estar en la ficha, que no cargó en la mañana.
