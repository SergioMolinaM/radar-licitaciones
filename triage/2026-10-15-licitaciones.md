# Triage de licitaciones — 15-oct-2026

Lectura de solo lectura en Mercado Público (sin login, sin foro, sin ofertar). Fuente: ficha pública de cada licitación y el PDF de bases leído completo con pdf.js dentro del navegador (texto extraído página por página; los números de página citados son los del PDF). Nada se resumió con WebFetch.

**Descarga de PDF: falló.** Chrome bajó un solo archivo (la Res. Ex. 568 de la CNE, ya copiada a `bases-2026-10-15\610-20-LE26\`) y bloqueó las descargas siguientes desde mercadopublico.cl (dos intentos, como registra la memoria `mercado-publico-bajar-bases`). Las bases se leyeron en memoria. Sergio tiene que bajarlas a mano para tenerlas en disco:

| Código | Archivo de bases | Ficha |
|---|---|---|
| 610-20-LE26 | `BasesdelicitacionestudioAutomatizacionProydda_FINAL.pdf` (682 KB, 38 pp.); además `ANEXOSBasesdelicitacion…docx`, `Planilla ExperienciaProponente.xlsx`, `Calendario Lic ProyeccióndeDamanda.pdf` | https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?idlicitacion=610-20-LE26 |
| 1233607-3-LE26 | `REX N°3297 - APRUEBA-BASES--ID-1233607-3-LE26--ver3.pdf` (1.222 KB, 46 pp.); además Anexos 1-6 .docx | https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?idlicitacion=1233607-3-LE26 |
| 1606-35-LE26 | `REX 303 ESTILOS EDITORIALES.pdf` (1.963 KB, 51 pp.); además Anexos 1-9 .docx | https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?idlicitacion=1606-35-LE26 |

No se leyeron: los .docx de anexos (sus formatos vienen transcritos dentro de cada PDF de bases), la planilla .xlsx de la CNE ni el PDF de calendario de la CNE (las fechas se tomaron de la ficha). No se abrió la vista pública de ningún foro.

---

## 1. 610-20-LE26 — Automatización e IA en los modelos de proyección de demanda (CNE)

**Comprador.** Comisión Nacional de Energía, RUT 61.707.000-6 (p. 1). Contraparte técnica: Jefe del Departamento de Regulación Económica (p. 20).

**Monto.** $20.467.000, «Presupuesto Disponible», «Monto con impuestos incluidos» (p. 1; repetido en p. 18). El Anexo 7 pide desglosar «Estudio» y «Desarrollo de Software», y la suma no puede exceder el presupuesto (p. 37). Pago: 90 % contra el Informe de Avance N°1 y 10 % contra el Informe Final (p. 18).

**Plazo.** Contrato de 180 días corridos desde la total tramitación del acto que lo aprueba, sin renovación (p. 20). Informe de Avance N°1 a los 50 días corridos e Informe Final a los 70 (p. 5). Firma estimada 16-11-2026 (ficha).

**Qué se entrega.** OE1: desagregar la demanda horaria del año inicial desde las barras del balance del Coordinador Eléctrico hasta la subestación y el nivel de tensión más bajo posible, con seis actividades mínimas de topología (SE 220 kV, SE zonales con varios niveles, consistencia con transformadores, barras «A I/A II», propietarios) (pp. 2-3). OE2: revisión crítica de metodologías, propuesta y aplicación de un modelo de proyección horaria con IA (al menos machine learning y deep learning) a 20 años (pp. 2-3). Memoria de cálculo reproducible y sin enlaces externos (p. 3). Dos informes con planillas y una presentación PowerPoint por entrega (p. 5). Si usa IA: Plan de Uso de Herramientas de IA en la propuesta técnica, entrega de código fuente y entorno reproducible sin servicios externos, y capacitación al personal de la CNE en el algoritmo (pp. 23-24). Propiedad de todo el material para la CNE; los informes serán públicos (p. 23). La omisión de algún servicio «podría dejar fuera de bases la propuesta» (p. 3).

**Criterios (p. 13).** Oferta técnica 84 %; económica 10 % (Vmin/Vi × 100, valor bruto); requisitos formales 2 %; programas de integridad 2 %; sustentabilidad (gestión de residuos, Anexo 4) 2 %. Dentro de la técnica (pp. 13-14): Jefe de Proyecto 20 %, Integrante 1 20 %, Integrante 2 20 %, propuesta metodológica 40 %.
- Jefe de Proyecto: ≥7 años = 100; ≥6 = 70; ≥5 = 50; ≥3 = 25; <3 = 0, en «aspectos técnico-económicos del sector energético asociados a la demanda energética y/o en trabajos de bases de datos con IA y trabajos realizados en la nube» (p. 13).
- Integrante 1: ≥5 años = 100; ≥4 = 70; ≥3 = 50; ≥2 = 25, mismo ámbito (p. 14).
- Integrante 2: ≥5 años = 100 … ≥2 = 25, en «topología de instalaciones de transmisión y su respectiva calificación» (p. 14).
- Metodología: parte de 100 y descuenta 5/10/20 por observación leve/mediana/grave; copiar la metodología de las bases sin complementarla es falta grave (pp. 14-16).
- **Umbral: técnica bajo 65 puntos = inadmisible** (p. 13); puntaje final ≥65 para adjudicar (p. 17). Desempate: experiencia del Jefe de Proyecto, luego Integrante 1, luego precio (p. 17).

**Equipo y cómo se acredita.** Anexo 5 (individualización, con profesión «pregrado y postgrado»), Anexo 6 (CV con mes/año de inicio y término y referencias) y la planilla Excel «Experiencia Proponente»; si hay inconsistencias manda la planilla (pp. 4, 15). Los años son la suma de meses de funciones o proyectos; sin mes y año no se cuentan; no cuentan estudios ni trabajos hechos durante o para la formación académica (p. 15). No se exige título específico ni experiencia de la empresa: lo que puntúa es la experiencia individual de tres personas. No se pide certificado de experiencia; la experiencia debe ser «comprobable» (p. 4).

**Admisibilidad.** Anexos 1-4, copia de personería con antigüedad ≤90 días, Anexos 5-6, planilla, propuesta técnica con Gantt y Anexo 7; sin ellos la oferta es inadmisible, salvo Anexo 8 y personería (p. 9). Validez de la oferta: 60 días corridos (p. 18).

**UTP.** Sí; cada integrante firma Anexos 1-4 y responde solidariamente (pp. 8, 11). **Subcontratación: contradicción.** La ficha dice «No permite subcontratación»; las bases la admiten parcialmente, hasta 30 % del monto, excluyendo los dos informes (p. 22).

**Foro.** Preguntas del 14-10 12:00 al **16-10-2026 17:00**; respuestas el 20-10 17:00 (ficha). Cierre 26-10 17:00; adjudicación 03-11 (ficha).

**Garantías.** Sin seriedad. Fiel cumplimiento: 5 % del precio neto, vigencia = contrato + 60 días hábiles, dentro de 10 días hábiles desde la adjudicación (pp. 11-12); la ficha fija vencimiento 12-08-2027.

**Lo que pesa.** El 60 % de la técnica depende de tres CV con años acreditables en demanda eléctrica o IA/nube y en topología de transmisión; el Integrante 2 es un perfil de ingeniería eléctrica de transmisión. Con menos de 65 puntos técnicos la oferta no se abre.

---

## 2. 1233607-3-LE26 — PVS Servicios de capacitación Programa 01, SLEP Iquique

**Comprador.** Servicio Local de Educación Pública de Iquique, RUT 61.980.910-6 (ficha). Unidad técnica: Encargado del Departamento de Gestión y Desarrollo de Personas (p. 4).

**Monto.** $10.530.102 IVA incluido, «presupuesto disponible» (p. 18) y «presupuesto referencial» (p. 25). Por línea: L1 $6.000.000 IVA incluido; L2 $4.530.102 IVA incluido (p. 30). Se adjudica por línea (p. 17) y se puede ofertar a una o a las dos (p. 30). Sin anticipos; pago a 30 días desde la factura (p. 25).

**Plazo.** Hasta el 31-12-2026, desde la emisión y aceptación de la orden de compra; no hay contrato, se formaliza con la OC (pp. 20-21).

**Qué se entrega.**
- Línea 1, «Convivencia y resolución de conflictos en terreno»: taller presencial de 8 horas para 80 funcionarios en Iquique, 4° trimestre 2026, de metodología física, lúdica y experiencial; una propuesta basada en charlas no se considera suficiente. El proveedor pone recinto para 80 personas con alternativa techada, coffee AM y PM, almuerzo, hidratación, materiales y equipo audiovisual; entrega programa, asistencia, registro fotográfico y audiovisual e informe (pp. 30-33). Facilitador principal con título en Psicología, Trabajo Social, Educación, Educación Física, Gestión de Personas, Ciencias Sociales o afín, más personal de apoyo (p. 32).
- Línea 2, «Liderazgo y manejo de equipos»: curso presencial de 8 horas para 10 jefaturas intermedias, 3° y 4° trimestre 2026, teórico-práctico; sala, coffee AM y PM, evaluación diagnóstica y final (pp. 33-35). Relator con título en Psicología, Administración, Gestión de Personas, Ciencias Sociales, Educación o afín (p. 35).

**Criterios (p. 13).** Administrativo 5 %; técnico 50 %; económico 45 % (precio mínimo × 100 / precio ofertado) (p. 16). Dentro del técnico: B.1 experiencia en servicios similares 25 %; B.2 experiencia de relatores 25 %; B.3 formación de relatores 20 %; B.4 descentralización 20 %; B.5 comportamiento contractual 5 %; B.6 pacto de integridad 5 %.
- B.1: OC o licitaciones adjudicadas de «capacitaciones a funcionarios públicos» de los últimos 2 años; ≥10 = 100; 7-9 = 75; 4-6 = 50; 1-3 = 25; ninguna = 1. Con privados, contratos firmados por ambas partes o facturas (pp. 13-14).
- B.2: certificados de experiencia emitidos por las entidades; >3 años = 100; 2-3 = 75; 1-2 = 50; <1 = 25; sin certificados = 1 (p. 14).
- B.3: título + cursos + doctorado o 2 magísteres atingentes = 100; con magíster = 75; con diplomado = 50; solo título y cursos = 25 (pp. 14-15).
- B.4: domicilio o sucursal en Tarapacá = 100; Arica o Antofagasta = 75; otra región = 50; acreditado con carpeta tributaria o inicio de actividades (p. 15).
- B.5: sin sanciones en Mercado Público = 100 (p. 15). B.6: Anexo 4 = 100 (p. 15).

**Admisibilidad.** Inscrito en el Registro de Proveedores al ofertar (p. 10). Inadmisible si falta el Anexo 4, la oferta técnica (Anexo 6 con sus respaldos) o la económica (Anexo 3) (p. 12). **Giro: el oferente debe tener actividad económica en el SII atingente a «servicios de capacitaciones»; si no, inadmisible** (p. 12). No verifiqué qué actividades tiene registradas Tercera Letra en el SII.

**UTP.** Sí, con acuerdo por instrumento público o privado adjuntado al ofertar (pp. 10-11). El formulario del Anexo 5 enumera criterios que no son los de esta licitación (precio, plazo de respuesta, equidad de género) (p. 43). **Subcontratación: no se contempla** (p. 23).

**Foro.** Preguntas del 14-10 18:01 al **17-10-2026 18:00**; respuestas el 19-10 18:00 (ficha). Cierre martes 20-10 18:01; adjudicación 17-11 (ficha).

**Garantías.** Ninguna: sin seriedad (p. 28) y sin fiel cumplimiento (p. 29). Multas de 10 % (atraso o cambio de relator o contenido sin aviso) y 15 % (incumplimiento del programa), con tope de 30 % (pp. 27-28). Se exige domicilio en Iquique para notificaciones (p. 29).

**Lo que pesa.** La L1 es un taller físico-recreativo con logística completa para 80 personas en Iquique. B.1 y B.4 premian historial con órdenes de compra de capacitación a funcionarios públicos y presencia en el norte. Cierra en 5 días, con el foro cerrando el sábado 17-10.

---

## 3. 1606-35-LE26 — Servicio de corrección de estilo para documentos (AGCID / ANCI, fondos UE)

**Comprador.** Agencia Chilena de Cooperación Internacional para el Desarrollo, RUT 60.108.000-1 (ficha; p. 21). Ejecuta la Agencia Nacional de Ciberseguridad (ANCI), cuya coordinación es la contraparte técnica (pp. 22, 31).

**Monto.** EUR 11.500 «con todos los impuestos incluidos», presupuesto máximo; una oferta por encima es inadmisible (p. 3). La ficha lo rotula «Precio Referencial», en euros. La oferta va en euros (neto + IVA 19 % en el Anexo 5) y otra moneda es inadmisible (pp. 5, 43). Se paga en pesos al tipo de cambio de BancoEstado cuando la AGCID convierte, y la variación del cambio no es imputable a la AGCID (p. 19). Pago por hitos: 22 % por el manual y 13 % por cada uno de los otros seis hitos (p. 20).

**Plazo.** Contrato hasta el 30-04-2027 desde la total tramitación de su aprobación (p. 21); la ficha dice 198 días.

**Qué se entrega.** Manual de estilo editorial y de citación APA 7 (Producto 1, 15 días hábiles desde la reunión de inicio); corrección de estilo de 11 documentos técnicos de ciberseguridad (siete documentos de trabajo, tres informes de investigación aplicada y una ley modelo) de **150 a 200 páginas cada uno**, con control de cambios y versión limpia, más glosario por documento y glosario consolidado (pp. 33-36). Cada documento se entrega 10 días hábiles después de recibido (15 para el primer par); llegan entre octubre de 2026 y marzo de 2027 (pp. 35-36). Hasta dos rondas de observaciones; una tercera no se acepta y se considera incumplimiento grave (pp. 36-37). Si usa IA, debe declarar la herramienta y el alcance de su intervención (pp. 29-30).

**Criterios (pp. 11-14).** Experiencia del oferente 25 %; formación del responsable principal 20 %; propuesta metodológica 25 %; precio 20 % (Vmin/Vi × 100); equidad de género 4 %; requisitos formales 2 %; programa de integridad 4 %.
- Experiencia: «servicios similares» son edición y redacción de documentos científicos, divulgación científica, tesis, libros, publicaciones científicas, papers u otros similares; ≥5 proyectos = 100; 3-4 = 70; 1-2 = 40; ninguno = 0. Se acredita con portafolios, contratos, OC, resoluciones aprobatorias, facturas y/o boletas de honorarios, declarados en el Anexo 4 con mes y año de término (pp. 11, 41). Las bases dicen «experiencia en proyectos del oferente»; no dicen si cuentan proyectos ejecutados por personas del equipo antes de la empresa (no encontrado en las bases, leídas pp. 1-51).
- Formación del responsable: grado o título en Literatura, Letras, Lingüística, Periodismo, Edición o afín + posgrado en corrección + diplomados o cursos = 100; título + posgrado = 80; título + diplomado o cursos = 60; solo título = 40 (pp. 11-12).
- Metodología: 100 si incluye metodología, Gantt, coordinación con ANCI, revisión y validación, y estrategia de fidelidad y consistencia terminológica; 70, 30 o 0 según lo que falte. Sin propuesta metodológica la oferta es inadmisible (p. 12).
- Género: 100 si el oferente es mujer o empresa liderada por mujer, verificado con el Sello Empresa Mujer (p. 13).
- Integridad: el Anexo 8 declarando «no tengo personal contratado» vale 100 (p. 13).
- Se descuentan 20 puntos por término anticipado y 10 por multa con la AGCID en los últimos 24 meses (p. 14). Desempate: género, precio, metodología (p. 14).

**Admisibilidad.** Hábil en el Registro al abrir (p. 4). Anexos 1, 2 y 8 (y 6 y 6.1 si es UTP), Anexo 4 con propuesta metodológica y Anexo 5; si falta alguno, la oferta es inadmisible (pp. 4-5, 10-11). Validez de la oferta: 90 días (p. 15). Para contratar: Anexos 3, 7 y 9 (encargo de tratamiento de datos personales) y vigencias de la sociedad y del poder con antigüedad ≤60 días (pp. 5-6).

**UTP.** Sí, solo entre empresas de menor tamaño, con documento de acuerdo al ofertar (p. 7). **Subcontratación.** La ficha dice «No permite subcontratación». En las bases, la cláusula 11.8 «Cesión de contrato y Subcontratación» solo prohíbe ceder (p. 17); la prohibición expresa de subcontratar no la encontré en las bases (leídas pp. 1-51).

**Foro.** Preguntas del 14-10 10:51 al **19-10-2026 12:00**; respuestas el 22-10 18:30 (ficha). Las bases dan 3 días hábiles para consultar (p. 3). Cierre lunes 26-10 18:30; adjudicación 18-11 (ficha).

**Garantías.** Ninguna, ni de seriedad ni de fiel cumplimiento (p. 8). Multas de 1 % del neto total por día hábil de atraso, con tope de 10 %; dos multas tramitadas o superar el 10 % son causal de término anticipado (p. 17).

**Lo que pesa.** El volumen: unas 1.650 a 2.200 páginas técnicas por EUR 11.500 brutos, con entregas de 10 días hábiles por documento. El 45 % técnico depende de proyectos de edición acreditados del oferente y del título de la persona responsable en letras, periodismo o afín, con posgrado o cursos de corrección. Riesgo cambiario a cargo del proveedor.

---

## Lecturas incompletas

- 610-20-LE26: bases pp. 1-38 completas. No leídos: el calendario PDF, el .docx de anexos y la planilla .xlsx.
- 1233607-3-LE26: PDF pp. 1-46 completas (bases administrativas, técnicas y anexos 1-6 transcritos).
- 1606-35-LE26: PDF pp. 1-51; quedaron sin leer dos tramos cortos: el final de la p. 29 (cierre del pacto de integridad, antes de la cláusula 11.31) y parte de la p. 49 (cláusula séptima del Anexo 9 de datos personales). No leídos los .docx de anexos.
