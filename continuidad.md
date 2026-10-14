# Continuidad — Radar de Licitaciones

## Sesión 2026-10-14 (miércoles) — triage de correos del 8 al 14-oct y sonda de Compra Ágil, desde la raíz

### Hecho

1. Triage de los correos del Radar del 8 (dos), 12, 13 y 14-oct: 20 avisos; 11 descartados por título, 2122-34
   ya en curso, 9 fichas leídas por subagente. Bases leídas a mano:
   - **765-25-L126 CONADI** ($6 MM con IVA, L1): SIMPLE + Clave Única + PISEE (~20 interoperaciones) + migración
     de los registros indígenas a SQL Server AWS con alta disponibilidad, CDC, auditoría y respaldos WORM, hasta
     el 28-dic, SLA 6 meses (1 h crítico), subcontratación prohibida, 30 % experiencia por OC en SIMPLE/CU/PISEE.
     **NO.**
   - **622-64-L126 TGR**, curso IA generativa 16 h para dirigentes AET ($5 MM con IVA, cierre 27-10 15:00,
     respuestas 22-10 18:00): experiencia del oferente 20 % (TL 0), Sello Mujer 5 % (TL 0), relator 25 %,
     metodología 20 % sobre «4 módulos» que no vienen en el PDF. **Sergio subió hoy dos preguntas al foro**
     (dónde están los módulos y bases generales; si cuenta la experiencia del socio único como persona natural).
     Decidir con las respuestas.
   - 3337-21-LE26 (plataforma psicométrica, DGMN): no calza. Camélido 585893-11: sigue sin socio.
2. **Compra Ágil:** la corrida del 14-oct cayó otra vez con 504 en la pág. 1 en los tres intentos. Sonda nueva
   `src/probe_compra_agil.py` + workflow manual `probe-compra-agil.yml`: siete variantes de parámetros (tamaño
   50/15, con y sin `ordenar_por`, ventana 3 d/1 d, sin filtros), dos rondas, código y tiempo; sin correo ni
   commit. **Resultado (run 38568890090):** toda variante tarda 23-29 s y da 504 al pasar 29 s (tope de API
   Gateway), sin importar tamaño, orden ni ventana; los 200 son las que alcanzan a terminar. 3 días publicadas =
   5.400 resultados (no ~800 como en julio): barrer todo no cabe ni con la API sana. `tamano_pagina` mínimo 10.
   El buscador público (`api.buscador.mercadopublico.cl/compra-agil`, x-api-key pública en su JS) tiene el mismo
   tope de 29 s: no sirve de respaldo. La guía oficial (§5.1 Grupo 5) tiene `q` = palabras clave en
   nombre/descripción filtradas en el servidor; segunda sonda con q para medir si responde rápido.

### Pendiente

- Correr la sonda y, según qué variante responda, cambiar `_fetch_pagina` (o pasar a la fuente pública).
- 22-10 18:00: respuestas del foro de 622-64-L126.
- Siguen los del 12-oct.

## Sesión 2026-10-12 (lunes) — diseño del agente de oportunidades, desde la raíz

**Leer primero `docs/DISENO-AGENTE-2026-10-12.md` entero.** Su §10 cuenta la conversación en orden, con las citas
de Sergio y lo que se atacó y corrigió; su §11 dice por dónde retomar. Esta entrada es el resumen.

### Hecho

1. **Pedido de Sergio:** un espacio agéntico aislado (puede ser otra máquina) que cada noche seleccione
   licitaciones con mirada más amplia que el Radar, prepare las presentaciones y en la mañana diga si nos
   presentamos o no, para que él autorice. Después lo amplió dos veces: que se abra a lo que no sabemos hacer si
   deja ingresos, y que no se cierre a una empresa nueva con otra gente («necesitamos circular dinero»).
2. **Diseño escrito, nada construido** (`docs/DISENO-AGENTE-2026-10-12.md`, 12 secciones): repo privado nuevo
   `licitaciones-agente` en GitHub Actions, aislado del Gmail/Drive/`~/.claude` de Sergio; noche = escaneo amplio →
   clasificación con modelo barato → lectura de bases con navegador headless (mismo POST por archivo de la memoria
   `mercado-publico-bajar-bases`) → contraste con el perfil de TL → evaluador adversarial → carpeta por candidata;
   mañana = correo con cuatro categorías (descartada con página / consultar al foro / presentar / solo con socio) e
   issue por candidata con comandos `/foro` `/presentar` `/socio` `/no`; tope de ofertas abiertas; **el agente no
   tiene Clave Única ni credenciales de Mercado Público, por diseño**.
3. **Seis carriles** (§4), cada uno entra al correo solo con su hecho habilitante verificado: lo que sabemos; con
   socio o UTP; TL como la EMT que necesita una UTP grande; venderle al que ganó (OCDS); Convenios Marco; comercio en
   Compra Ágil (solo con margen medido).
4. **Lo que se atacó y sobrevivió** (§2): encontrar no es el cuello de botella (de ~15 bases leídas del 1 al 8-oct
   se presentó 1; las demás murieron por experiencia, títulos, ATE/sin fines de lucro, medios o socio ausente); el
   agente no arregla la experiencia acreditable; la decisión del 3-oct de concentrar se respeta con el tope de
   ofertas.
5. **Investigación** (3 subagentes `investigador`/`claude-code-guide`): Licitalab es lo más cercano en Chile (lee
   bases con IA citando el punto; 2,2/3,2/5 UF/mes + IVA; 14 días gratis); suites RFP extranjeras no calzan; Banco
   Mundial tiene API gratis; opciones de Claude comparadas (Actions, `claude -p`, rutinas en la nube con allowlist,
   Managed Agents); ley y reglamento: Compra Ágil ≤ 100 UTM va por defecto a EMT y locales, no se adjudica solo por
   precio, pago a 30 días; **subcontratación tope 30 %**; UTP con solidaridad y escritura desde 1.000 UTM; nota de
   comportamiento contractual; OCDS trae adjudicaciones pero excluye Compra Ágil. Ficha del investigador en
   `~/.claude/agent-memory/investigador/ref_compras_publicas_ds661_api.md`.
6. **Convenio Marco TI 2239-2-LR26 (100-25.000 UTM) cerró el 9-oct sin pasar por el Radar** (ausente en
   `data/state.json`, búsqueda con control positivo). Causa probable la exclusión `mantención de`
   (`src/config.py:173`) o falta de «software» en las inclusiones; **no verificada** (falta el título exacto). Tamaño:
   convenio anterior 321 adjudicados y solo 124 vendiendo (USD 21,5 M entre todos, dic-22 a may-24); el de 2024 446
   adjudicados, 30 meses. Se perdió un canal, no un ingreso seguro.
7. **Universo de julio medido** (`data/audit-2026-07-08.csv`): 4.029 licitaciones, 36 pasaban el filtro (0,9 %);
   heurística por título: ~1.365 bienes, ~617 obras, ~350 servicios, ~1.700 sin clasificar.
8. **Socios con nombre** (§5.1): Solución Integral SpA (solintegral.cl, Jorge Salinas M., RUT 76.376.518-0,
   herramientas industriales para minería desde 2014, Unilink y Ariba; «vende al estado.. de eso vive», según
   Sergio) como operador del carril de comercio; Dialoga Consultores (d-aloga, Kena Fernández, RUT 78.484.769-1) para
   UTP de participación y consulta indígena. Borradores de correo a los dos en Gmail TL, verificados (FALLA→PASA en
   el de Jorge).
9. Incumplimiento propio: `cd` encadenado por novena vez (memoria `cd-encadenado-cambia-el-directorio`); propuesto
   a Sergio un hook que lo bloquee, sin respuesta.

### Pendiente

- **Sergio:** enviar los borradores a Jorge y a Kena (en el de Kena decide antes si cierra la ronda del 13-08 del
  sitio de d-aloga, trabajada sin encuadre comercial); responder si se agrega el hook contra el `cd` encadenado.
- **Sergio decide §9 del diseño:** clave de API con tope (recomendado) o token de suscripción; prueba de Licitalab
  en paralelo (recomendado); tope de ofertas abiertas (propuesta: dos); nombres de socios operadores.
- **Claude, con la respuesta de Jorge:** su código de proveedor y sus OC por la API `BuscarProveedor`.
- **F0 después del 15-oct** (§7): perfil de TL + casillero de los ~15 casos leyendo cada carpeta de `postulaciones/`
  y las continuidades de los SLEP; lector de bases en Actions sin Chrome; aceptación 14/15; mediciones por carril y
  de margen (empezar por las líneas de Solintegral); Licitalab 14 días; título exacto de 2239-2-LR26 contra las
  exclusiones.
- **01-12-2026:** vence la habilidad de TL en Mercado Público (renovar) y rige la Ley 21.719.
- Siguen los del 8-oct: Compra Ágil en 504, ruido de `digital`, pendientes 2-4 del 14-07.

### Estado del repo

`main`. Commit de esta sesión: `docs/DISENO-AGENTE-2026-10-12.md` (nuevo) y esta entrada. Sin cambios de código.
Push autorizado por Sergio («haz el cierre»).

## Sesión 2026-10-08 (jueves) — correo tarde y cierre del PNUD, desde la raíz

### Hecho

1. **Correo tarde, medido:** las 15 últimas corridas programadas (18-sep a 8-oct) partieron entre 3,5 y 8 h
   después de las 12:00 UTC (hoy 18:28 UTC). GitHub no garantiza la hora del `schedule`.
   Arreglo (`ff2c636`, decisión de Sergio: cron-job.org): cron-job.org dispara `workflow_dispatch` a las
   09:00 America/Santiago L-V con un token fine-grained (solo este repo, Actions read/write) que Sergio pega
   allá y no pasa por Claude. El `schedule` queda de respaldo y se salta si ya hubo un `workflow_dispatch`
   ese día (paso `respaldo`, `gh run list --created`); `concurrency` evita dos corridas juntas.
   La consulta del respaldo se probó a mano (control: 1 schedule hoy, 0 dispatch desde el 1-oct).
2. **PNUD:** el correo mostraba como «Cierre» el `dc:date` del RSS (publicación). El cierre real viene en la
   descripción («Application Deadline: 23-Oct-26») y ahora se lee de ahí (`_deadline`, probado contra el feed
   de COL: 50471 → 2026-10-23). Claude le había dicho a Sergio que esa licitación estaba cerrada: falso.
3. Triage del correo del 8-oct: 2122-34-LE26 (IA para el Registro de Cáncer, Seremi Salud Antofagasta,
   $26 MM con IVA, cierre 20-oct 15:00, preguntas hasta lun 12 18:00) le interesa a Sergio con modelo
   local. Juicio: técnica factible; riesgo en codificación CIE-O-3 y experiencia (20 %); ir solo con un
   registrador de tumores. Las otras tres, no.

4. Corrida de prueba 19:30 UTC trajo **585893-11-LE26** (INDAP Tarapacá, manual Plan Camélido, $20 MM con IVA, cierre 22-10 15:30; foro hasta 15-10 16:00). Bases leídas por subagente: trayectoria en manuales de **camélidos** 17 % (AFIPA no sirve), equipo con veterinario/agrónomo de camélidos del norte, mínimo 70 puntos para adjudicar, diseño/diagramación no subcontratable, ~5 semanas reales para un plan de 11. Recomendación: **no solos**; solo con un especialista en camélidos que aporte la trayectoria. Sergio no decidió.
5. 2122-34-LE26: citas textuales verificadas por subagente; temeraria = menos del 50 % del siguiente (§11.5). Consultas al foro en `postulaciones/seremi-salud-2122-34-ia-cancer/consultas-foro.md` (`270dc4b`); análisis «solos + subcontratar una persona» en las notas internas de ese archivo.
6. Valle Diguillín descartada por Sergio (ver su repo).

### Pendiente

- cron-job.org (job 8607281) **funcionando: Test run 204** tras corregir método (GET→POST), body, falta de
  `Authorization`, horario (`*/15 9`→`0 9 * * 1-5`). Corridas dispatch de prueba 19:27 y 19:30 UTC completas
  (MP 4.806, PNUD 574; rojas solo por Compra Ágil). **Vie 9: confirmar que el dispatch de las 09:00 salió y
  que el `schedule` del día se saltó** (paso «Respaldo»). Token fine-grained vence en 1 año (oct-2027).
- 2122-34-LE26: preguntas al foro (subcontratación, hardware de la Seremi, anexos válidos) antes del lun 12 18:00.
- Siguen: ruido de `digital`, Compra Ágil en 504, pendientes 2-4 del 14-07.

### Estado del repo

`main` con `ff2c636` + esta entrada; push autorizado por Sergio el 8-oct.

## Sesión 2026-10-07 (miércoles, tarde) — triage de los correos del Radar, desde la raíz

### Hecho

1. Leídos los correos del escáner (remitente `onboarding@resend.dev`, etiqueta Licitaciones) del 1, 2, 6 y
   7-oct. Lista corta por título y cierre; bases leídas por dos subagentes en Chrome (pdf.js en memoria):
   - 1177296-23-LP26 Familias de Acogida ($270,7 MM, agencia creativa + ≥70 % pauta, 3 cotizaciones de
     productoras admisibilidad, garantía ~5 %): NO.
   - 584105-39-LE26 plan de medios Energía ($35 MM, ≥90 % pauta, experiencia en compra de medios): NO.
   - 558869-62-LE26 capacitación IA Antofagasta ($55 MM SEP): NO — solo «personas naturales o jurídicas
     sin fines de lucro» con Registro ATE (frase leída en el texto de las bases, dos lugares).
   - 1111089-21-LE26 monitoreo de prensa ANID ($8,5 MM/12 meses): NO — exige captura de radio y TV,
     cobertura 30 %, mínimo 60 puntos.
   - 591-34-LE26 curso IA FONASA ($3 MM): NO — 45 % experiencia certificada en sector público; prohíbe
     subcontratar.
   - 1209-12-L126 curso IA SEREMI Educación Antofagasta ($4,11 MM, online 30 h, 19-30 oct): única viva,
     solo con relator con título TI o certificación IA (sin él da 1,75 contra mínimo 2). Recomendación:
     soltar salvo relator el mismo día (cierra mar 13 15:05, igual que Llanquihue; consultas jue 8 15:05).
2. Descarte por título del resto (encuestas de campo, licencias SLEP Puelche, PRCC, capacitaciones SLEP
   Chiloé, medios radiales).
3. Ruido de `KEYWORDS_INCLUDE_PALABRA` `digital` visto en la corrida del 6-oct: radio portátil VHF SAMU,
   termógrafo digital, sistema radiográfico odontológico, ampliación laboratorio de imagen digital.
4. Correo «ROJO: backend de Gestión de dotación» (13:38 UTC): era una de cinco corridas **manuales** del
   keepalive de `SergioMolinaM/dotacion` (13:15–13:38, 3 fallas, 2 éxitos; la última verde). Ninguna
   corrida programada todavía.

### Pendiente

- Sergio decide la 1209-12-L126 (relator o soltar) antes del jue 8 15:05 si quiere consultar en el foro.
- Auditar el ruido de `digital` (evidencia arriba): probable exclusión de «radio portátil», «termógrafo»,
  «radiográfico», «imagen digital» o exigir co-ocurrencia.
- Compra Ágil sigue en 504: probar página más chica. Sin eso el triage no ve ese canal.
- `dotacion`: confirmar el jue 8 que el keepalive corrió por horario (todas las de hoy son manuales).
- Siguen los pendientes 2-4 del 14-07 y mirar en una semana las keywords de Radar Construcción.

### Estado del repo

`main` sin cambios de código en esta sesión; solo esta entrada. Bases de 558869 en
`Descargas\LIC558869_RES1269_bases.pdf` (fuera del repo).

## Sesión 2026-10-07 (miércoles) — desde la raíz, sesión «Varios»

### Hecho

1. **Keywords de Radar Construcción Industrializada** (`config.py`, commit `62f39ac`): «construcción
   industrializada», «industrialización de la construcción», «plantas industrializadoras», «paneles sip».
   Salen de la evaluación de posibilidades del 7-oct (`marca/POSIBILIDADES-2026-10-07.md`, fila 6).
   Probadas con `matches_keywords`: entra el estudio SIP del Minvu (587-45-L125); quedan fuera «Arriendo
   de oficinas modulares» y «Adquisición de paneles solares». **No entra** la consultoría de
   fiscalización de plantas del Serviu IX (712307-38-LE26): la bloquean las exclusiones «fiscalización de»
   y «consultoría apoyo técnico», que se dejaron como estaban. «vivienda(s) industrializada(s)» no se
   agregó porque la exclusión «vivienda» gana siempre.
2. Corrida del 6-oct verde con 21 oportunidades; **Compra Ágil sigue caída** (el correo lo avisa).

### Pendiente

- Sin cambios: Compra Ágil en 504 (probar página más chica); auditar el ruido de `digital`; pendientes 2-4 del 14-07.
- Mirar en una semana si las keywords nuevas trajeron algo o ruido.

### Estado del repo

`main` con push el 7-oct (autorizado por Sergio: «si sube»).

## Sesión 2026-10-02 (viernes)

### Hecho

Disparador: no llegó la licitación FUCOA **1108660-10-LE26** («SERVICIO DE REDISEÑO DEL PORTAL
INSTITUCIONAL», CNR, $13M, cierre 14-10). Las de envases MMA 608897-60-LE26 (30-sep) y USACH
867990-99-L126 (02-10) sí llegaron: verificado en el `data/state.json` remoto.

1. **Keywords web, digital e IA** (`config.py`). Frases: portal institucional/web, sitio(s) web,
   página(s) web, diseño/desarrollo web, rediseño, aula virtual, plataforma web, redes sociales,
   contenidos digitales, comunicación digital, producción audiovisual, video institucional,
   identidad visual, imagen corporativa, transformación digital, inteligencia artificial.
   Lista nueva `KEYWORDS_INCLUDE_PALABRA` (palabra completa): `web`, `digital`, `ia`.
   "portal" a secas se descartó (trae "portal de acceso", obra vial).
2. **Bug de exclusión por subcadena** (`filters.py`): "erp" excluía "interpretación" y "cuerpos";
   "sap" excluía "ssap". Ahora toda keyword calza desde inicio de palabra (regex). Los prefijos
   ("quirúrgic") siguen funcionando. `audit.py` y `audit_compra_agil.py` alineados.
3. **Compra Ágil caída desde mediados de agosto**: 504 Gateway Timeout (~29 s) en la página 1 casi
   todos los días (muestras: 21-08 a 02-10; 07-08 funcionó; 18-09 cayó en la pág. 23). Se informaba
   como "0 recorridas" sin alarma. Ahora: 3 intentos con esperas 20/60 s ante 5xx/red.
4. **Fuente caída ya no es silenciosa**: universo 0 en MP, CA o PNUD → banner en correo y
   heartbeat, state guardado y `exit 3` → corrida roja en Actions (GitHub avisa por correo).
   `scanner.yml`: paso de commit con `if: always()`.

5. **Tras el verificador (FALLA leve, 7 hallazgos):** barrido de CA cortado a mitad (caso 18-sep)
   ahora cuenta como caída (`fetch_raw_publicadas` devuelve `(items, completo)`); exclusiones
   compuestas que el borde de palabra dejó de cubrir se agregan explícitas (televigilancia,
   videovigilancia, remodelación, electroquirúrgic, cardioquirúrgic, hidrogeológic); «rediseño»
   suelto → «rediseño web/del portal/del sitio/de la página» (dejaba pasar «rediseño de red de agua
   potable»); `save_state` atómico (tmp + `os.replace`); `timeout-minutes: 30` en el job y
   presupuesto de 15 min para el barrido de CA. No corregidos: doble log del 5xx final (cosmético) y
   fatiga de alarma si CA cae a diario (decisión: preferible rojo diario a silencio).

### Verificado

Test offline (scratchpad, 25/25 tras los arreglos del verificador; antes 19/19): títulos reales de las tres licitaciones, reintentos 504/red/429
con mocks, scanner con CA caída → exit 3 con state guardado y banner. Contra el universo de
julio (`audit-2026-07-08.csv`, 4.029 títulos): antes 43 matches, **entran 20, salen 0**.
De esos 20, ~10 son ruido de `digital` (plataformas escolares, biopsia digital, libro de obras).

### Pendiente

1. **No verificado: que los reintentos recuperen Compra Ágil.** Sin token en local. Mirar la
   corrida del lunes 05-10. Si sigue 504 en pág. 1, probar `tamano_pagina` menor o sin
   `ordenar_por` (hipótesis, no medida).
2. **Auditar el ruido de `digital`** tras una semana de correos; si molesta, pasar a frases.
3. Pendientes 2-4 de la sesión 14-07 siguen abiertos (auditoría CA por descripción,
   `utcnow()` deprecado, organismo/monto en el correo).

### Estado del repo

Rama `main`. Modificados: `src/config.py`, `src/filters.py`, `src/audit.py`,
`src/audit_compra_agil.py`, `src/sources/compra_agil.py`, `src/scanner.py`, `src/notifier.py`,
`.github/workflows/scanner.yml`, `continuidad.md`. Sin dependencias nuevas. Sin deploy (Action).

## Sesión 2026-07-14 (martes)

### Hecho

**Fuente nueva: Compra Ágil (ChileCompra, API v2).** `src/sources/compra_agil.py`, cableada en
`scanner.py` y en el heartbeat (`universo_ca`). Trae las Compras Ágiles en estado `publicada` de
los últimos 3 días (`COMPRA_AGIL_DIAS_VENTANA`), pagina hasta agotar y filtra por keywords.

Verificada contra la guía oficial ("Documentación API Compra Ágil", mayo 2026, enlazada desde
https://www.chilecompra.cl/api/ → `Documentacion_API_Compra_Agil.pdf`). Lo que confirmó:

- Base **`api2.mercadopublico.cl`** (no `api.mercadopublico.cl`) y ticket por **header** `ticket`,
  no query param. Sin header → 401; ticket inválido/bloqueado → 403 (§3, §7).
- `GET /v2/compra-agil`; respuesta `{"success":"OK","payload":{"items":[],"paginacion":{}}}` (§6).
- `tamano_pagina` máximo **50** (default 15) y `ordenar_por=FechaPublicacion` es valor válido
  (§5.1 Grupos 6 y 7). Este último importaba: un valor inválido da 400 y la fuente habría
  devuelto 0 en silencio.
- Cuota por ticket y por **día calendario**; 429 al agotarla (§4). El barrido corta en 429 y
  conserva lo acumulado.

**Corregido del borrador:** el link de la ficha era inventado (`DetailsAcquisition.aspx?idcompra=`).
La guía no documenta la ficha pública, así que se verificó a mano abriendo la Compra Ágil
`5627-188-COT26` en el buscador público. El patrón real, que carga sin sesión, es:
`https://buscador.mercadopublico.cl/ficha?code={codigo}` (en `config.py`).

**Auditoría nueva: `src/audit_compra_agil.py`.** Manual (no entra al cron), no envía correo ni
toca `data/state.json`. Baja la ventana, pide el detalle de cada Compra Ágil —único lugar donde
la API entrega `descripcion` (§6.1 vs §6.3)— y escribe `data/audit-compra-agil-YYYY-MM-DD.csv`.

**README:** se cerró la truncadura en `## Audi` (pendiente #1 de la sesión del 09-07) y se
restauró el `## Roadmap sugerido` desde `bc7c2fa`. Ya no queda nada truncado por `ce2b8bf`.

### El hallazgo que importa

Se agregó Compra Ágil matcheando por **`nombre`**, igual que licitaciones, y **no** por descripción.
La razón, medida y no supuesta:

1. Las dos fuentes chilenas matchean solo el título (`mercado_publico.py:74`). El comentario de
   `config.py:4` que dice "Nombre + Descripcion" **está desactualizado**: el código nunca usó la
   descripción.
2. Los nombres de Compra Ágil son genéricos ("COMPRA INSUMOS 114219") y la sustancia vive en la
   descripción. Pero al probar ese caso contra las listas reales, **cae excluido por `"insumos"`**:
   la exclusión pega sobre el nombre *antes* de que la descripción alcance a rescatarlo. Matchear
   la descripción no arregla el caso que motivaba matchear la descripción.
3. Las inclusiones anchas (`redacción`, `encuesta`, `infografía`) son señal en un título y ruido
   cuando aparecen de pasada en un párrafo. Con ~780 Compras Ágiles por ventana, bastaría un 3-5%
   de menciones incidentales para meter 25-40 ítems basura al correo diario.

El problema de fondo no es la descripción: es que las exclusiones fueron calibradas contra títulos
de **licitaciones** (descriptivos) y en Compra Ágil los nombres son genéricos y compran cosas, así
que `"insumos"` / `"compra de"` / `"materiales de"` barren en masa. La auditoría cuenta las dos
poblaciones por separado (`NUEVO_POR_DESCRIPCION` y `EXCLUIDA_NOMBRE` con keyword en descripción)
justamente para decidir cuál de los dos arreglos corresponde.

### Verificado

Dry-run en proceso (sin red, sin correo, `data/state.json` intacto), 20 + 17 chequeos:

- Fuente: paginación hasta `total_paginas`, ticket en header y no en query, `tamano_pagina=50`,
  link a la ficha verificada, `id` prefijado `CA::` para el dedupe, contrato con `notifier`.
- Los cuatro caminos de fallo: token ausente, `RequestException`, JSON inválido, 401, `success=NOK`,
  y un **429 a media paginación** (conserva lo acumulado, no revienta la corrida).
- `scanner.run()` completo con las tres fuentes; heartbeat forzado a mano (solo corre viernes) y
  render de la fila nueva; un heartbeat sin `universo_ca` no revienta.
- Auditoría: una fila por Compra Ágil, clasificación correcta contra las keywords reales, respeta
  `MAX_DETALLES`, tolera detalles caídos, el radar diario **no** pide detalles, y no escribe en `data/`.

### Pendiente

1. **No verificado: que el ticket v1 habilite `api2`.** No hay `MERCADO_PUBLICO_TOKEN` en local y la
   guía no dice si el ticket de licitaciones sirve para la API v2 o hay que pedir uno nuevo. Si no
   sirve, el log dirá `ticket rechazado (403)` y la fuente devuelve 0 sin voltear el resto del radar.
   Lo confirma la primera corrida del cron (12:00 UTC, L-V) o un `workflow_dispatch` a mano.
2. **Correr la auditoría y decidir lo de la descripción:** `python -m src.audit_compra_agil 100` con
   el ticket cargado. Filtrar `NUEVO_POR_DESCRIPCION` (¿señal o ruido?) y mirar cuántas
   `EXCLUIDA_NOMBRE` traen keyword en la descripción (¿hay que aflojar exclusiones en esta fuente?).
3. **`datetime.utcnow()` deprecado** (Python 3.12+) en `src/state.py` y `scanner.py:_weekly_stats`.
   No hay choque aware/naive; solo `DeprecationWarning`. Sigue pendiente de la sesión anterior.
4. El correo no muestra `organismo` ni `monto_clp`, aunque la fuente ya los trae. Para Compra Ágil
   el monto es útil (tope 100 UTM): evaluar agregarlos a `notifier.render_html`.

### Estado del repo

Rama `main`, commit `e031bbc` + este. Archivos: `src/sources/compra_agil.py` y
`src/audit_compra_agil.py` (nuevos); `src/config.py`, `src/scanner.py`, `src/notifier.py`,
`README.md` (modificados). Sin dependencias nuevas.

Sin deploy: es un GitHub Action programado, no tiene hosting. El cierre termina en push.
