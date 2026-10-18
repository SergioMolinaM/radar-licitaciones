# Triage — Fuera del Radar — 17-oct-2026

## Resumen

| # | Código | Organismo | Qué piden | Monto | Cierre | Foro hasta | Veredicto | Horas de Sergio |
|---|---|---|---|---|---|---|---|---|
| 1 | 1047-1-RFIPRI26 | SERVIU RM | Consulta al mercado: plataforma de contratos de arriendo DS 52 (.NET, SQL Server) | no publicado | 05-jun-2026 10:00 | no aplica | NO (cerrada) | 0 |
| 2 | 3245-1-RFIPRI26 | DGAC | Consulta al mercado: plataforma de reclutamiento y evaluación psicolaboral | no publicado | 01-jul-2026 | no aplica | NO (cerrada) | 0 |
| 3 | no verificado | FIA | Soporte y actualización de la Biblioteca Digital (DSpace 7.6 → 9.2) | no publicado | no verificado | no verificado | NO (ejecución desde 01-ago-2026) | 0 |
| 4 | no verificado | Subsecretaría del Trabajo | RFI gestión documental SaaS | no publicado | no verificado (10 días hábiles desde la publicación; PDF creado el 04-ago) | no aplica | NO | 0 |
| 5 | 1122317-2-RFIPRI26 | DCCP | Consulta al mercado: estudios de mercado para Compras Coordinadas | no publicado | 11-sep-2026 17:30 | no aplica | NO (cerrada; vigilar la licitación) | 0 |
| 6 | 869591-3-LE126 | DCCP | Valorización NICSP 31 de los intangibles de las plataformas de ChileCompra | $70.000.000 presupuesto (bases p. 2) | 21-sep-2026 15:00 | no verificado | NO (cerrada) | 0 |
| 7 | 869591-2-LE126 | DCCP | Diagnóstico y plan de adopción digital de la nueva plataforma modular | 100 a 1.000 UTM | 02-oct-2026 15:00 (ampliada desde el 24-sep) | no verificado | NO (cerrada) | 0 |
| 8 | 869591-4-LE126 | DCCP | Relicitación de la valorización NICSP 31 de las plataformas (plataforma nueva, «Licitaciones Beta») | no verificado (la 554-B decía $70.000.000) | 04-nov-2026 15:00 | no verificado | CON SOCIO (valorización NICSP/IAS 38) | 25 |

**Corrección del mismo día:** la valorización se relicitó el 15-oct como 869591-4-LE126 y está **vigente** hasta el 04-nov 15:00 (nota chilecompra.cl del 15-oct, leída vía wp-json). Las bases bajadas (Res. 554-B del 27-ago) son las del proceso -3; hay que bajar las del -4 desde «Licitaciones Beta» con sesión de Sergio y cotejar cambios. Del resto ninguna está vigente; la 5 deja la licitación de estudios de mercado de la DCCP que vendrá.

## Cómo se leyó

Sergio bajó a `Descargas\` 12 archivos el 17-oct entre 11:13 y 11:18 (siete procesos; las dos `Guia_de_uso_licitaciones_simples*` son el manual genérico de ChileCompra y no se triaron). Texto extraído en el scratchpad de la sesión (`bases-17oct/`, no se copió al repo porque nada sigue). Dos subagentes leyeron todo: uno las bases 554-B (55 pp.), sus anexos y las generales 505-B; el otro los cinco restantes.

Vigencia: la API de Mercado Público no lee los códigos `-LE126` ni los RFI (devuelve «Los parámetros no son válidos»; con 1469-284-L126 como control sí responde), así que las fechas salen de las notas de chilecompra.cl y de los propios documentos. Comprobado por el hilo principal: 869591-2-LE126 cierre 2-oct 15:00 (chilecompra.cl/?p=56581) y 869591-3-LE126 cierre 21-sep 15:00, publicada el 27-ago (nota de chilecompra.cl del 27-ago), sin ampliación en lo leído. El resto, según el subagente: 1 (nota chilecompra.cl 29-may), 2 (chilecompra.cl/?p=54089), 5 (chilecompra.cl/?p=56450). El 3 y el 4 no traen código; sus fechas salen del documento.

Los `NO` de esta tabla son por plazo vencido, no por un requisito: el §1.5 no se aplica a un proceso cerrado.

## Candidatas

### 5. 1122317-2-RFIPRI26 — Estudios de mercado para Compras Coordinadas (DCCP) — NO (cerrada; vigilar)

- **Qué piden:** 12 meses de estudios de mercado por rubro, con «explotación de la información transaccional de mercadopublico.cl» (Componente 1), bases limpias con sintaxis y diccionario (Componente 8), 5 a 75 días por estudio (§2.3).
- **Cómo se decide:** no aplica (consulta al mercado).
- **Puntaje estimado de TL:** no aplica.
- **Requisitos y cómo se cubren:** el análisis sectorial y de precios (salud, energía) pide un economista; el resto calza con lo que TL hace en el Radar.
- **Riesgos y lo que falta:** fecha de la licitación posterior no publicada.
- **Siguiente paso:** keyword en el Radar para el comprador 869591 con «estudios de mercado» y «compras coordinadas» (otra sesión de radar-licitaciones).

### 6. 869591-3-LE126 — Valorización de activos intangibles (DCCP) — NO (cerrada)

- **Qué piden:** inventario y valorización NICSP 31 / Res. CGR 16/2015 de cinco plataformas, con Excel con fórmulas y asientos contables (pp. 28-32). Financia el BID (p. 39).
- **Cómo se decide:** técnico 75 %, económico 20 %, administrativo 5 % (p. 6); experiencia del oferente 35 % y del equipo 35 % del técnico, con 5 valorizaciones de intangibles desde 2020 para el máximo (pp. 7-9).
- **Puntaje estimado de TL:** sola, ≈ 39-45 (oferente 0, equipo 0).
- **Requisitos y cómo se cubren:** solo con una firma de valorización/auditoría con 5+ trabajos NICSP 31 / IAS 38; subcontratación prohibida (cl. 9, p. 19).
- **Riesgos y lo que falta:** el -3 cerró; sigue en la candidata 8 (relicitación -4, vigente).
- **Siguiente paso:** ver la 8.

### 8. 869591-4-LE126 — Valorización de activos intangibles, relicitación (DCCP) — CON SOCIO (valorización NICSP/IAS 38)

- **Qué piden:** lo mismo que la 6 según la nota del 15-oct (NICSP 31, Res. CGR 16/2015, asientos y migración a activo fijo); bases del -4 no leídas.
- **Cómo se decide:** si repite la 554-B, técnico 75 % (oferente 35 %, metodología 20 %, equipo 35 %, plazo 10 %), económico 20 %, administrativo 5 % (pp. 6-12).
- **Puntaje estimado de TL:** sola ≈ 39-45; con profesionales de valorización a honorarios (permitido: la cl. 9, p. 19, prohíbe subcontratar pero acepta contratos con cada profesional) sube el equipo; con una UTP con firma de valorización EMT sube también el oferente.
- **Requisitos y cómo se cubren:** tres perfiles nominados con título ≥ 8 semestres (13.4.2, p. 33) y 5 valorizaciones de intangibles cada uno para el máximo; experiencia del oferente con cartas de clientes desde 2020. Se cubre con socio: firma EMT con 5+ valorizaciones NICSP 31 / IAS 38 de software, o al menos un contador auditor y un especialista TI con esa experiencia contratados a honorarios.
- **Riesgos y lo que falta:** bases del -4 (pueden haber corregido el calendario que en el -3 no cerraba con la facturación al 21-dic); fecha del foro; socio.
- **Siguiente paso:** Sergio inicia sesión en Mercado Público; se bajan bases y foro del -4 desde «Licitaciones Beta»; Sergio decide a quién se le pide ser socio.

### 7. 869591-2-LE126 — Plan de adopción digital (DCCP) — NO (cerrada)

- **Qué piden:** diagnóstico y plan de adopción de la plataforma modular de compras; equipo mínimo nominado como admisibilidad (investigación cuali-cuanti, adopción digital y gestión del cambio, campañas, líder) y experiencia del oferente desde 2020 con cartas (Anexos 2 y 2.1).
- **Cómo se decide:** bases particulares no bajadas (no verificado).
- **Puntaje estimado de TL:** no verificado.
- **Requisitos y cómo se cubren:** era de las que calzaban (comunicación + investigación + digital).
- **Riesgos y lo que falta:** el Radar no la trajo o no se triageó; revisar por qué en la sesión del radar.
- **Siguiente paso:** ver si la DCCP la declara desierta o la relicita.

Los procesos 1 a 4 no se desarrollan: cerrados o ya en ejecución. Si reaparecen, el 1 (stack .NET/SQL Server, solo proveedores del Convenio Marco 2239-19-LR23), el 3 (DSpace) y el 4 (ISO 27001 e ISO 9001 exigidas, p. 2) son CON SOCIO; el 2 pide psicólogos y una batería de tests (§3.2, §3.5).

## Barrido de chilecompra.cl (17-oct)

Con la fuente nueva del Radar (commit c16a6a3, sin push) se leyeron las notas de chilecompra.cl de los últimos 30 días por su API pública: 5 procesos abiertos. Solo calza el 869591-4-LE126 (candidata 8). Las «Licitaciones Beta» de otros organismos y el buscador de consultas al mercado (reCAPTCHA) no se pudieron barrer: falta la sesión de Sergio en Mercado Público.

## Ruido

Cuatro procesos de bienes, sin abrir bases: 897096-1-LE126 (arriendo e instalación de equipos de videoconferencia, $49 MM, cierre 28-oct 15:00), 1122317-17-LR26 (Compra Coordinada de arriendo de impresoras, cierre 09-nov 15:15), 1122317-3-RFIPRI26 (consulta de vehículos, 20-oct) y 1122317-4/-5-RFIPRI26 (energía eléctrica y lubricantes, 18-oct). Las dos guías de uso de ChileCompra no son procesos.
