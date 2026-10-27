# Triage — Compra Ágil — 22-oct-2026

## Resumen

| # | Código | Organismo | Qué piden | Monto | Cierre | Foro hasta | Veredicto | Horas de Sergio |
|---|---|---|---|---|---|---|---|---|
| 1 | 1305560-66-COT26 | SLEP Valdivia, Depto. Jurídico | 4 licencias de plataforma de IA jurídica por 6 meses | 3.500.000 IVA incl. (máx., según TDR; ficha no verificada) | 23-oct 10:00 (según el Radar; ficha no verificada) | no verificado | CON SOCIO (plataforma chilena de IA jurídica ya existente) | 3 con socio; 0 sin socio |
| 2 | 4127-134-COT26 | Subsecretaría de Redes Asistenciales (Minsal) | Curso de IA aplicada a la función pública, 15 funcionarios, 12 h | 1.200.000 est. (TDR: máximo, impuestos incluidos) | 24-oct 13:00 (2.º llamado 27-oct 13:28) | sin foro | CON SOCIO (2 relatores con ≥2 años en IA generativa) | 6 + búsqueda de relatores |

Esta semana no cabe ninguna sin socio. La de Valdivia tiene más plata, pero cierra mañana a las 10:00 y pide un producto que TL no tiene. La del Minsal, si aparecen dos relatores antes del 24 o del 27, se arma reutilizando el curso de la SEC 1614-61.

## Cómo se leyó

Las tres fichas se leyeron con subagentes en pestañas propias de Chrome. La 1305560-66 no cargó en cinco intentos: la API corta a los 29,3 s y se ven solo «0 cotizaciones recibidas» y los dos adjuntos. Por eso descripción, monto de la ficha, cierre, foro e invitados quedan no verificados, y el cierre y el título salen del correo del Radar. Los adjuntos de la 1305560-66 y el TDR de la 4127-134 los releyó el hilo principal contra el original. Archivos en `triage/bases-2026-10-22/<código>/`:

- 1305560-66: `TDR IA (1).pdf` (325.800 bytes, 5 pp.) y `Anexo N°1.docx` (87.944 bytes).
- 4127-134: `IA aplicada a la funcion publica SRA.docx` (131.758 bytes) y `Curso IA SRA - transcripcion.txt` (el `Curso IA SRA.docx` original no bajó; se transcribió desde la ficha).

En `Downloads\` quedaron sueltos `TDR IA (1).pdf`, el `.tmp` del Anexo y el .docx del Minsal; sus copias están en el repo.

## Candidatas

### 1. 1305560-66-COT26 — Plataforma de IA jurídica, SLEP Valdivia — CON SOCIO (plataforma chilena de IA jurídica ya existente)

- **Qué piden:** «contratar el licenciamiento de uso de la plataforma de inteligencia artificial de asistencia judicial» (TDR p. 1), 4 licencias por 6 meses (Anexo N°1 §2).
- **Cómo se decide:** oferta económica 70 % por mínimo costo, con valores sin impuestos, y plazo de entrega 30 %: 1 día hábil = 100, 2 = 75, 3 = 50, más de 3 inadmisible (TDR p. 2). El máximo es $3.500.000 con impuestos incluidos y una oferta que lo supere no se considera (TDR §2).
- **Puntaje estimado de TL:** no aplica sin producto. Con un socio que entregue en 1 día, el plazo da el 30 % completo y el resto se decide por precio.
- **Requisitos y cómo se cubren:** Anexo N°1 firmado (sin él no se evalúa) y ficha técnica del software. Hay que declarar «Cumple» en las 14 especificaciones obligatorias, y si falla una la oferta es inadmisible (TDR §3-4). Las que TL no cubre: 1 («del rubro jurídico»), 1.5 (entrenado o configurado con normativa chilena vigente), 1.6 (búsqueda y síntesis de jurisprudencia de la CGR, la DT, la Corte Suprema y las Cortes de Apelaciones) y 1.7 (citación de fuentes). Ninguna de las plataformas de TL busca jurisprudencia (`experiencia-tercera-letra`). Solo se cubre revendiendo o distribuyendo un producto existente cuyo proveedor entregue la ficha técnica. El TDR no exige giro.
- **Riesgos y lo que falta:** declarar «Cumple» sin el producto sería una declaración falsa, y entregar tarde cuesta 1 UTM por día con término anticipado a los 10 días corridos (TDR §9). La vigencia (1.10) dice «mínima 6 meses» en el TDR (p. 1) y «mínima 12 meses» en el Anexo N°1 (p. 5), mientras la oferta económica y el TDR §7 dicen 6. Las especificaciones están escritas como ficha de un producto puntual: eso es lectura, no hecho verificado. No hay socio identificado y quién podría serlo no está verificado. Pago a mes vencido, a 30 días de la factura (TDR §8). Inspector: Cristián Ahumada Onell, Dpto. Jurídico y Transparencia (TDR §10).
- **Siguiente paso:** Sergio decide hoy si busca un proveedor de IA jurídica chilena para revender. Sin socio antes de mañana a las 10:00, se deja pasar.
- **Búsqueda de socio (22-oct):** el detalle con fuentes está en `bases-2026-10-22/1305560-66-COT26/proveedores-ia-juridica.md`, armado por un subagente. El candidato que más calza es iJurídica (BotiLex 2.5 Pro). Su portada, leída el 22-oct por el hilo principal, lista jurisprudencia administrativa de «Contraloría, SII, Dirección del Trabajo, SUSESO», más de 100.000 sentencias, legislación con vínculos a la BCN, «Fuentes revisables», y carga y revisión de documentos solo en Premium. El plan Portal Legal Premium cuesta $350.000/año o $55.000/mes, «Hasta 5 usuarios concurrentes». No verificado en su portada: que nombre la Corte Suprema y las Cortes de Apelaciones (el subagente lo cita de una nota de junio de 2026), la transferencia de licencias (1.12), la administración de usuarios (1.11) y si permite revender. La ficha no muestra segundo llamado automático.
- **Contra la reventa:** el plan cubre las 4 licencias de 6 meses con una sola cuenta de lista bajo $350.000. Con el 70 % por precio, si iJurídica u otro proveedor cotiza directo, la oferta de un revendedor pierde. El margen existe solo si nadie más cotiza (0 cotizaciones al 22-oct) o si el proveedor acepta ir por TL. Revender un plan cuyas condiciones no permiten reventa expone a TL. Sin acuerdo escrito y ficha técnica del proveedor, no se oferta.

### 2. 4127-134-COT26 — Curso de IA aplicada a la función pública, Minsal (SRA) — CON SOCIO (2 relatores con ≥2 años en IA generativa)

- **Qué piden:** curso «Inteligencia artificial aplicada a la función pública: herramientas para reducir tareas repetitivas y ordenar los procesos de trabajo» para 15 funcionarios: 12 h en 4 sesiones de 3 h por Teams o Zoom, grabadas. La herramienta principal es Copilot Chat institucional. Seis módulos con contenidos mínimos. Entregables: guía de prompts, semáforo de datos, Ficha de solución evaluada de 1 a 7, certificados, encuesta e informe final con el «indicador de tiempo liberado».
- **Cómo se decide:** criterios con peso no publicados. El TDR advierte que las propuestas genéricas, no adaptadas a sus antecedentes (CEAL-SM 2025, Plan MEL), tendrán menor puntaje.
- **Puntaje estimado de TL:** no verificable sin criterios. La adaptación al contexto es el punto fuerte si se trabaja la propuesta.
- **Requisitos y cómo se cubren:** el TDR §5 exige «al menos 2 relatores/as, los cuales deberán acreditar experiencia demostrable (al menos 2 años) en capacitación sobre inteligencia artificial generativa aplicada a la gestión administrativa en salud y en formación de personas adultas en el uso de IA», con CV (comprobado contra el .docx). Ni el kit ni la memoria acreditan esos dos años para Sergio. Se cubre con dos relatores externos, con Sergio en el diseño y la coordinación. La plataforma virtual con soporte se cubre con Google Classroom, como en la SEC. El TDR no exige OTEC ni SENCE, y aplica la actividad SII 855000.
- **Riesgos y lo que falta:** el plazo de 10 días (hábiles según el adjunto) no calza con 4 sesiones de hasta dos por semana, la prueba en el puesto de trabajo «la semana siguiente» y el informe a 15 días corridos de la última sesión: la oferta tiene que fijar qué hito cuenta como entrega. El monto es «máximo disponible: $1.200.000 (impuestos incluidos)» (TDR, comprobado), unos $1.008.403 netos para dos relatores e informe, con margen bajo. El pago es contra la recepción conforme del informe final. La Compra Ágil no tiene foro y el único canal es el correo de la solicitante (Valentina Fernández); escribirle lo decide Sergio.
- **Siguiente paso:** Sergio decide si busca dos relatores (sector público o salud) antes del 24-oct 13:00, o del 27-oct 13:28 si hay segundo llamado. Si los hay, la propuesta parte del material de la SEC 1614-61.

## Ruido

1: 799512-1462-COT26, Corporación Municipal de Valparaíso, impresión de 17 infografías en trovicel de 50×70 cm, $340.000 disponibles, infografía ya diseñada por el comprador. Es un bien. Cierre 23-oct 07:00.
