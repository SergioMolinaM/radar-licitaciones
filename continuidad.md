# Continuidad — Radar de Licitaciones (código, repo público)

**Este repo es público.** Aquí va solo el estado técnico del radar: código, workflows, fuentes de datos, cuotas y
errores. **Nada de ofertas, precios, decisiones comerciales, clientes ni nombres de personas.** Todo eso va en
`privado/continuidad.md` (repo privado anidado `radar-licitaciones-privado`, ignorado por este repo), junto con
los triages (`privado/triage/`), el diseño del agente (`privado/docs/`) y los reclamos (`privado/soporte/`).

La historia completa hasta el 31-oct-2026 está en `privado/continuidad.md`. Entradas de la más nueva a la más vieja.

## 2026-11-24 — Compra Ágil 429 tras 6 solicitudes; sesión de ofertas

### Hecho
- Run 45389350675 (24-11 09:00, 1 min 49 s): listado de Compra Ágil cortado por 429 tras 6 solicitudes (Retry-After
  None); lo publicado de 2026-11-23T10:00:57Z a 2026-11-24T12:00:40Z queda para la próxima corrida. Diarios de q sin
  respuesta (19 términos). Correo con 16 ítems (Compra Ágil 7, Mercado Público 6, PNUD Bolivia 2, PNUD Chile 1).
- Sin cambios de código. Ofertas y decisiones en `privado/continuidad.md`.
- Ficha pública `buscador.mercadopublico.cl/ficha?code=` carga los campos con 20-30 s de demora; los adjuntos se ven y
  el GUID sale por `dispatchEvent` igual que en `resumen-cotizacion`. Sin sesión, `resumen-cotizacion` redirige a Home.
- Formulario de Compra Ágil: si el grupo de pestañas de Claude desaparece, el formulario a medio llenar se pierde; al
  reabrir, los adjuntos del intento anterior reaparecen y se duplican (se eliminan con JS sobre el enlace «Eliminar»).
- `python -I` ignora `PYTHONIOENCODING`: para imprimir UTF-8 en pwsh se usa `python -I -X utf8`.

### Pendiente
- Relanzar a media tarde por el 429 temprano (decisión del 18-11).
- Lo de las entradas anteriores sigue (sombra, textos viejos, `fecha_cierre`, CSV de costos).

### Estado del repo
`main` con esta entrada; sin cambios de código. `firestore-debug.log`, `node_modules/` y `package.json` sin
seguimiento, de otra sesión: no tocados.

## 2026-11-23 — Corrida sin 429 (29 min, 81 páginas, 215 ítems); sesión de ofertas

### Hecho
- Run 45170208649 (23-11 09:00, 29 min 26 s): listado de Compra Ágil sin 429, 81 páginas desde 2026-11-20T10:00:44Z,
  3.604 publicadas, 83 con keyword en el título, marca 2026-11-23T12:00:57Z. Correo con 215 ítems (Compra Ágil por
  título 78, Mercado Público 13, por palabra suelta 124). Diarios «digital» y «audiovisual» sin respuesta; rotativos
  electrónica, papel y trabajo en pausa. Segunda corrida seguida sin 429.
- Sin cambios de código. Las ofertas del día y sus decisiones van en `privado/continuidad.md`.
- Adjuntos de Compra Ágil sin descarga a Descargas: en la ficha `resumen-cotizacion/<código>` se anula
  `HTMLAnchorElement.prototype.click` y `window.open` por JS y se dispara `dispatchEvent(new MouseEvent('click'))` sobre el
  enlace; el GUID queda en `performance.getEntriesByType('resource')` (`comprador/descargar?id=<GUID>`) y el archivo se
  baja con `curl -L` a `servicios-compra-agil.mercadopublico.cl/v1/adjuntos-compra-agil/descargar/<GUID>`. Subir
  `performance.setResourceTimingBufferSize(2000)` antes: con el búfer lleno no aparece la entrada.
- Chrome: hacer clic real en varios adjuntos seguidos dispara el aviso de «descargar varios archivos» y la pestaña deja
  de responder (timeouts de 30 s); el tabId de la pestaña cambia tras cada recarga: releer `tabs_context_mcp`.
- Docx de anexos con casilla de control de contenido (`w14:checkbox`): se marca poniendo `w14:checked w14:val="1"` y el
  texto `☒`; Word (COM) convierte docx a PDF en este equipo (no hay docx2pdf ni pdftoppm).
- Sesión de la noche (sin cambios de código): en pwsh 7 no existe `[Runtime.InteropServices.Marshal]::GetActiveObject`;
  para ver o cerrar un documento abierto en Word se llama a `powershell.exe` (5.1). El grupo de pestañas de Claude en
  Chrome desapareció entre dos turnos («tab group no longer exists»): `tabs_context_mcp` con `createIfEmpty` y pestaña
  nueva. Los adjuntos de Compra Ágil se suben con `file_upload` sobre el input oculto, uno por llamada.

### Pendiente
- Triage del 23-11: escrito solo lo que cerraba el 24-11 (`privado/triage/2026-11-23-compra-agil.md`); quedan 151
  ítems abiertos del correo.
- Relanzamiento automático a media tarde tras un 429 temprano (decidido el 18-11): sin hacer; hoy no hizo falta.
- Lo de las entradas anteriores sigue (sombra, textos viejos, `fecha_cierre`, CSV de costos).

### Estado del repo
`main` con esta entrada; sin cambios de código. `firestore-debug.log`, `node_modules/` y `package.json` sin
seguimiento, de otra sesión: no tocados.

## 2026-11-20 — Corrida sin 429 (37 min, 145 páginas); sesión de triage y ofertas

### Hecho
- Run 44732153388 (20-11 09:00, 37 min 39 s): listado de Compra Ágil sin 429, 145 páginas desde
  2026-11-18T14:00:39Z, 6.896 publicadas, 141 con keyword en el título, marca 2026-11-20T12:00:44Z; q 'municipal'
  cortada a 5 páginas; correo con 328 ítems. Primera corrida sin 429 desde el 11-11 (después de la mantención de la
  API anunciada para la noche del 19-11; relación no verificada).
- Sin cambios de código. El triage, las ofertas y sus decisiones van en `privado/continuidad.md`.
- Chrome: subagentes en paralelo comparten el grupo de pestañas de Claude; una sesión puede navegar o cerrar el grupo de
  otra (visto el 20-11). Las pestañas que quedan fuera del grupo no se pueden cerrar con `tabs_close_mcp`.

### Pendiente
- Relanzamiento automático a media tarde tras un 429 temprano (decidido el 18-11): sin hacer; hoy no hizo falta.
- Lo de las entradas anteriores sigue (sombra, textos viejos, `fecha_cierre`, CSV de costos).

### Estado del repo
`main` con esta entrada; sin cambios de código. `firestore-debug.log`, `node_modules/` y `package.json` sin
seguimiento, de otra sesión: no tocados.

## 2026-11-19 — Compra Ágil 429 (noveno día); relanzada a mano por la tarde; mantención anunciada de la API

### Hecho
- Run 44519833120 (19-11 09:00, 2 min 10 s): listado 9 páginas desde 2026-11-15T12:00:39Z, 293 publicadas, 1 con
  keyword; 429 tras 10 solicitudes (Retry-After None). Hueco definitivo por el tope de 4 días: 2026-11-14T18:00:38Z a
  2026-11-15T12:00:39Z. Correo con 12 ítems. Noveno día seguido.
- Run 44580442971 (relanzada a mano, 17:44 UTC, 15 min 47 s; decisión de Sergio del 18-11): 119 páginas, 5.632
  publicadas, 117 con keyword; 429 tras 120 solicitudes. Marca 2026-11-18T16:00:39Z; sin leer de ahí a
  2026-11-19T17:44:57Z. Correo con 120 ítems. Igual que el 12-11: la corrida de la tarde lee mucho más que la de las 09:00.
- Aviso de ChileCompra en la portada de Mercado Público (19-11): la API de Compra Ágil «podría presentar
  indisponibilidades» desde las 20:00 del 19-11 hasta ~08:00 del 20-11 por mantención programada.
- Respaldo por el buscador web (subagentes, publicadas 18 y 19-11). Los GUID de los adjuntos de Compra Ágil se ven en el
  registro de recursos de la página al hacer clic en cada archivo de la ficha; luego `curl -L -o` al endpoint público.
- Formulario `resumen-cotizacion`: si la página se recarga antes de enviar, se pierden los campos y los adjuntos
  reaparecen tarde y se duplican al resubir (medido en una oferta del 19-11).
- Sin cambios de código.

### Pendiente
- Programar el relanzamiento automático a media tarde cuando la corrida de las 09:00 corte por 429 en las primeras
  solicitudes (decidido por Sergio el 18-11; hoy se hizo a mano). Es el primer trabajo técnico del 20-11.
- Lo de las entradas anteriores sigue (sombra, textos viejos, `fecha_cierre`, CSV de costos).

### Estado del repo
`main` con esta entrada; sin cambios de código. `firestore-debug.log`, `node_modules/` y `package.json` sin
seguimiento, de otra sesión: no tocados.

## 2026-11-18 — Compra Ágil 429 a la 2.ª solicitud (octavo día); respaldo por el buscador web

### Hecho
- Run 44299778514 (18-11 09:00): Compra Ágil respondió 429 tras 2 solicitudes. Octavo día seguido. El tope
  `LISTADO_DIAS_MAX` (4 días) sigue dejando huecos definitivos mientras dure el 429.
- Respaldo por buscador.mercadopublico.cl para las publicadas del día.
- Adjuntos de Compra Ágil: `GET servicios-compra-agil.mercadopublico.cl/v1/adjuntos-compra-agil/descargar/<GUID>`
  es público (sin sesión) y baja el archivo con `curl -L -o`.
- Sin cambios de código.

### Pendiente
- Relanzar sola a media tarde tras un 429 temprano: sigue sin decisión de Sergio (recomendado el 17-11).
- Lo de las entradas anteriores sigue (sombra, textos viejos, `fecha_cierre`, CSV de costos).

### Estado del repo
`main` con esta entrada; sin cambios de código. `firestore-debug.log`, `node_modules/` y `package.json` sin
seguimiento, de otra sesión: no tocados.

## 2026-11-17 — Compra Ágil 429 a la 10.ª solicitud (séptimo día); barrido web cortado por el buscador

### Hecho
- Run 44079068418 (17-11 09:00, 2 min 2 s): listado 9/17 páginas del tramo 2026-11-13T12:00:44Z, 450 publicadas, 5
  con keyword; 429 tras 10 solicitudes (Retry-After None). Marca sigue en 2026-11-12T16:00:43Z. Hueco definitivo por
  el tope de 4 días: 2026-11-12T16:00:43Z a 2026-11-13T12:00:44Z. Sin leer: 13-11 12:00Z a 17-11 12:00Z. Correo con 16
  ítems (Compra Ágil 5, Mercado Público 11). Diarios de q sin respuesta (19 términos). Séptimo día seguido.
- Respaldo por el buscador web (subagente, publicadas 16 y 17-11): 41 fichas; desde ~13:30 el buscador falló en casi
  todos los términos («No ha sido posible obtener el listado»); quedaron sin buscar ~20 términos. Sin 403 ni captcha.
- La ficha `compra-agil.mercadopublico.cl/resumen-cotizacion/<código>` sin sesión redirige a `mercadopublico.cl/Home`;
  con sesión carga el formulario. Tras enviar, la URL pasa a `cotizacion-publicada?quote=<código>`.
- Sin cambios de código.

### Pendiente
- Relanzar sola a media tarde tras un 429 temprano: sigue sin decisión de Sergio (recomendado el 17-11).
- Lo de las entradas anteriores sigue (sombra, textos viejos, `fecha_cierre`, CSV de costos).

### Estado del repo
`main` con esta entrada; sin cambios de código. `firestore-debug.log`, `node_modules/` y `package.json` sin
seguimiento, de otra sesión: no tocados.

## 2026-11-16 — Compra Ágil 429 a la 9.ª solicitud (sexto día); barrido web como respaldo

### Hecho
- Run 43862655108 (16-11 09:00, 1 min 47 s): listado 8/24 páginas del tramo 2026-11-12T14:00:43Z y 429 tras 9
  solicitudes (Retry-After None). Marca sigue en 2026-11-12T16:00:43Z; sin leer hasta 2026-11-16T12:00:35Z. Correo
  con 9 ítems (8 Mercado Público, 1 empleo PNUD). Sexto día seguido sin Compra Ágil por la API.
- Respaldo por el buscador web (subagente, publicadas 12 al 16-11): 350 fichas, sin 403 ni captcha. Sin cambios de
  código del radar.

### Pendiente
- Con el tope de 4 días, la corrida del 17-11 deja sin leer 2026-11-12T14:00Z a ~13-11 12:00Z (casi todo ya cerró).
- La propuesta de relanzar sola a media tarde tras un 429 temprano sigue sin decisión de Sergio.
- Lo de las entradas anteriores sigue (sombra, textos viejos, `fecha_cierre`, CSV de costos).

### Estado del repo
`main` con esta entrada; sin cambios de código.

## 2026-11-13 — filtro de tiers en empleos PNUD; Compra Ágil 429 a la 4.ª solicitud

### Hecho
- Run 43421530977 (13-11 09:00, 1 min 42 s): Compra Ágil 429 tras 4 solicitudes (3/67 páginas del tramo
  2026-11-12T14:00:43Z, Retry-After None), así que la relanzada de la tarde del 12-11 no evitó el 429 temprano.
  Marca sigue en 2026-11-12T16:00:43Z; sin leer de 14:00:43Z al 13-11 12:00:57Z. Correo con 2 ítems
  (1076403-15-LE26 y el empleo PNUD 38051). Quinto día seguido sin Compra Ágil por la mañana.
- `src/sources/undp_empleos.py`: nueva `_tiers()`. El empleo 38051 «Open to Tier 0 & 1 & 2» pasaba porque el
  filtro buscaba el texto «tier 1». Ahora un aviso queda fuera si el título restringe a tiers sin el 3 (el portal:
  «Tier 3 or no tier indicated: … other external candidates»), también en Chile. Lee rangos, «Tier X & Tier 3»,
  «or», «through», romanos, «Tier(s)» y números de vacantes. Ante una palabra que no conoce, o con «external» o
  «above», deja pasar el aviso.
  Se descartó la regla de lista negra por patrón (primera versión): el verificador midió que con «Tiers 1-3»,
  «Tier 2 and Tier 3» o «1, 2 and external» escondía avisos postulables.
  Es mejor para el producto porque el correo deja de mostrar empleos internos y un aviso abierto no se pierde
  por una redacción nueva.
  Costo, no criterio: nada.
  Medido: 64 tests OK. Portal real: 7 remotos, pasa solo el 36167; los 23 títulos con tier de los 106 vigentes se
  leen bien. Quedan 4 variantes sintéticas que dejan pasar un aviso no postulable («Tier 3 Support Analyst (Open
  to Tier 1 & 2)», «Tier 1 & 2, Ref 3»), aceptadas. Verificador: FALLA, FALLA (redacciones con palabra
  desconocida), corregido; la tercera pasada la corrí con sus scripts (46 variantes, 42 bien).

### Pendiente
- Compra Ágil: la propuesta de relanzar sola a media tarde tras un 429 temprano sigue sin decisión de Sergio.
- Lo de las entradas anteriores sigue (sombra, textos viejos, `fecha_cierre`, CSV de costos).

### Estado del repo
`main` con el cambio del filtro y esta entrada.

## 2026-11-12 — solo configuración (sesión de la raíz)

- `.gitignore`: se agrega `.claude/worktrees/` (copias de trabajo de subagentes que aparecían sin seguimiento). Sin cambios de código.

## 2026-11-12 — sin cambios de código; sesión de ofertas

### Hecho
- Sin cambios en `src/` ni en los workflows. La sesión armó y envió una Compra Ágil y avanzó una licitación (detalle
  en `privado/continuidad.md` y en las carpetas de `postulaciones/`).
- Ficha pública de Compra Ágil (`buscador.mercadopublico.cl/ficha?code=…`): los campos de descripción, plazo y
  presupuesto cargan vacíos; el adjunto baja por `GET servicios-compra-agil.mercadopublico.cl/v1/adjuntos-compra-agil/
  descargar/<GUID>` sin sesión (medido el 12-11 con Invoke-WebRequest, 190.356 bytes). El formulario
  `resumen-cotizacion` pierde los campos al recargar pero conserva los adjuntos, que aparecen tarde.

- Run 43213982753 (12-11 09:00): Compra Ágil 429 a la **1.ª** solicitud (Retry-After None); exit 3; correo con 10
  ítems (MP 5.106 escaneadas, PNUD 553, ChileCompra 5). Ninguna otra corrida usó la API ese día. Cuarto día seguido
  sin Compra Ágil (09 y 10-11 504; 11 y 12-11 429). El respaldo de las 19:35 UTC saltó bien (1 corrida del día).
- Run 43298566921 (relanzada por Sergio, 20:15 UTC): listado leyó 199 páginas, 9.428 publicadas, 198 con keyword en
  título, desde 2026-11-08T22:00:43Z; 429 tras 200 solicitudes en la pág. 31/41 del último tramo. Marca
  **2026-11-12T16:00:43Z**; sin leer 16:00:43Z a 20:16:10Z (lo retoma la corrida del 13-11). Correo con 203 ítems.
  No se perdió nada por `LISTADO_DIAS_MAX`. El 429 de la mañana y los 200 de la tarde siguen sin umbral a la vista.

### Pendiente
- 13-11: ver si la corrida de las 09:00 vuelve a dar 429 temprano tras la relanzada de la tarde (posible efecto de
  ventana del límite; no verificado).
- Propuesta (no aplicada, decide Sergio): relanzar sola una vez a media tarde cuando la de las 09:00 corte por 429
  en las primeras solicitudes; hoy la relanzada de las 17:15 Chile funcionó.
- Lo de las entradas anteriores sigue (sombra, textos viejos, `fecha_cierre`, CSV de costos).

- Fuera de este repo (sin cambios de código del radar): `postulaciones/_kit/compra-agil/oferta.py` suma dos
  `CondPageBreak` (títulos que no quedan solos al pie y tabla de cotización entera), por el verificador.

### Estado del repo
`main` con esta entrada; sin cambios de código. `.claude/` sin seguimiento, como antes. Nada a medio camino.

## 2026-11-11 — Compra Ágil con 429 tras 7 solicitudes; exclusión de recaudación con POS o tarjetas

### Hecho
- Run 43016589355 (11-11 09:00, 1 min 42 s, success): el listado de Compra Ágil leyó 6 páginas (58 publicadas, 0 con
  keyword) y cortó por 429 tras 7 solicitudes (Retry-After None). Marca 2026-11-09T00:00:43Z; sin leer de ahí a
  2026-11-11T12:00:43Z. Hueco por el tope de 4 días: 2026-11-05T18:00:38Z a 2026-11-07T12:00:43Z. Los diarios de q no
  respondieron. Correo con 25 ítems (Mercado Público 22, ChileCompra 1, PNUD 1, empleo PNUD 1).
- Respaldo manual por el buscador web (subagente, publicadas 10 y 11-11, 22 términos): sin 403 ni captcha; el buscador
  da «No ha sido posible obtener el listado» intermitente y se resuelve reintentando o buscando por día. 356 fichas.
  Fichas escaneadas leídas con Tesseract.js dentro de la página.
- `src/config.py`: `KEYWORDS_EXCLUDE` suma «máquinas pos», «máquina pos», «terminales pos», «terminal pos», «tarjetas
  bancarias», «tarjeta bancaria» (aprobado por Sergio el 11-11). Motivo: la recaudación con POS exige ser adquirente o
  subadquirente inscrito en la CMF (1561-28-LP26 bases p. 9 §3.6; 5416-51-LP26 p. 41 §2.1).
  Se descartó «pos» suelto: el patrón corta al inicio de palabra y no al final, y excluía «postulación», «posgrado» y
  «posicionamiento». También «equipos pos»: excluía «EQUIPOS POSTA» en el audit del 08-07.
  Es mejor para el producto porque saca del correo procesos que TL no puede ofertar sin perder ninguno que sí.
  Costo, no criterio: nada.
  Medido: 0 títulos excluidos de más en `data/audit-2026-07-08.csv` (4.029); los dos títulos del 11-11 quedan
  excluidos. `python -m unittest discover -s tests`: 64 OK. Commit `ab51d4f`.
- La búsqueda de texto de Claude Code (Grep) dio 0 sobre `tercera-letra\` en un término que está en un archivo
  (control positivo falló): no se usó para afirmar ausencias.

### Pendiente
- 12-11: ver si la API de Compra Ágil vuelve o sigue el 429 temprano (09-11 504, 10-11 504, 11-11 429).
- Lo de las entradas anteriores sigue (sombra, textos viejos, `fecha_cierre`, CSV de costos).

### Estado del repo
`main` con `ab51d4f` y esta entrada, subidos. Nada a medio camino.

## 2026-11-10 (tarde) — Compra Ágil con 504 de nuevo; respaldo por el buscador web

### Hecho
- Run 42812057365 (10-11 09:00): Compra Ágil 504 en el listado y en los 16 diarios (29 solicitudes, 0 devueltas);
  exit 3; correo con 12 ítems (Mercado Público 11, ChileCompra 1). El ticket solo vive en los secretos del repo: la API
  no se probó desde el equipo.
- Respaldo manual por `buscador.mercadopublico.cl/compra-agil` (publicadas 09 y 10-11, 19 términos): funcionó sin
  captcha. Las bases en formato nuevo de licitaciones bajaron por curl con el postback `descargar_pdf_baseFirmada`.
- Propuesta (no aplicada, la decide Sergio): lanzar el barrido web sin esperar pedido cuando el correo diga «Fuente
  caída: Compra Ágil».

### Pendiente
- Ver si la API vuelve en la corrida del 11-11. Lo de las entradas anteriores sigue.

### Estado del repo
`main` con esta entrada, sin cambios de código.

## 2026-11-10 — Términos del socio tecnológico

### Hecho
- `src/config.py`: 66 términos nuevos en `KEYWORDS_INCLUDE` (agentes de IA y WhatsApp, automatización y flujos,
  gestión documental, firma e identidad, pagos y recaudación, nube, analítica y BI, monitoreo de redes, atención
  ciudadana, desarrollo de sistemas, ciberseguridad), 8 siglas en `KEYWORDS_INCLUDE_PALABRA` (bpm, ocr, crm, rpa, api,
  nube, aws, app), 20 en `KEYWORDS_INCLUDE_EN` y 3 diarios de Compra Ágil (chatbot, whatsapp, automatización).
  «hosting» salió de `KEYWORDS_EXCLUDE`. Motivo comercial en `privado/continuidad.md`.
- Ruido medido contra `data/audit-2026-07-08.csv` (4.030 títulos): pocos calces; se evitó «cloud» y «mensajería»
  sueltas (Adobe Creative Cloud, mensajería-estafeta). Queda «automatización portón» como ruido aceptado.
- `python -m unittest discover -s tests`: 64 OK. Prueba del filtro con 12 títulos de muestra.

### Pendiente
- Ver en las próximas corridas si la rotación de Compra Ágil se alarga demasiado o sube el 429 con los términos nuevos.
- Lo del 09-11 sigue.

### Estado del repo
`main` con el cambio de `src/config.py` y esta entrada, sin push hasta revisar si el push dispara algún workflow.

## 2026-11-09 — Compra Ágil responde 504 en todo

### Hecho
- Run 42613417488 (09:00) y run 42628768485 (relanzada 10:48 Chile): el listado de Compra Ágil dio 504 en la
  primera página (dos intentos de ~33 s) y los 16 diarios de q también. 0 ítems de Compra Ágil; exit 3 por fuente
  caída; correos con 8 y 3 ítems (Mercado Público y PNUD). Marca sin mover: 2026-11-05T18:00:38Z.
- El 06-11 (run 42214348990) el listado leyó 145 páginas (7.058 publicadas) y cortó por 429 tras 146 solicitudes.
- Se relanzó porque desde el 09-11 18:00:38Z el tope de 4 días (`LISTADO_DIAS_MAX`) deja sin leer lo publicado
  entre la marca y el tope. No se cambió el código: lo de ese tramo probablemente ya cerró (no verificado).
- Mercado Público: la página de adjuntos (ViewAttachment) carga un reCAPTCHA Enterprise invisible; fuera del
  navegador llega sin la lista de archivos. En Chrome funciona, una pestaña nueva por licitación.

- Respaldo con la API caída: barrido manual del buscador web (`buscador.mercadopublico.cl/compra-agil`, Estado
  «Publicada», desde la fecha de la marca) en Chrome, término por término. Resultados en 10-16 s; `page_number` en la
  URL vuelve a la pág. 1 (se pagina con los botones); sin captcha. 16 términos en ~26 min.

### Pendiente
- 10-11: ver si la API de Compra Ágil vuelve. Hueco esperado 2026-11-05T18:00:38Z a ~2026-11-06T12:00Z.
- Sigue lo del 05-11 y el 04-11 (sombra, textos viejos, `fecha_cierre`, CSV de costos; sombra vence el 15-11).

### Estado del repo
`main` con esta entrada. Sin cambios de código. Cierre de la sesión de la tarde: sin cambios técnicos nuevos; lo
comercial del día quedó en `privado/continuidad.md`. Cierre de la noche: tampoco hay cambios de código. Adjuntos de
Compra Ágil leídos en Chrome sin descargar: se captura el blob con `URL.createObjectURL` al hacer clic en el adjunto de
la ficha y se extrae el texto con pdf.js 4.0.379 de cdnjs dentro de la página; `javascript_tool` corta la salida en
~1.000 caracteres, así que se lee por tramos.

## 2026-11-05 — 429 a la segunda solicitud; el presupuesto de 36 min sigue sin medirse

### Hecho
- Run 42023483040 (09:00): 49 s. Listado cortado por 429 tras 2 solicitudes (1/35 páginas, 50 publicadas, Retry-After
  None). Marca sin mover: 2026-11-03T16:00:38Z; sin leer de 2026-11-03T14:00:38Z a 2026-11-05T12:00:34Z. Correo con 7
  ítems, sin Compra Ágil. Mismo patrón que el 27-oct y el 3-nov. Causa no verificada.
- Run 42029420922 (relanzada por pedido de Sergio, 09:42): 18 min. 121 páginas, 5.900 publicadas, 121 con keyword en
  título; 429 tras 122 solicitudes en la pág 55 de 62 del tramo 04-11 14:00. Marca 2026-11-04T14:00:38Z. Correo con 92
  ítems. El presupuesto de 36 min sigue sin agotarse: la corrida cortó por 429 a los 18 min.
- La lectura de adjuntos por `/v1/auth/publico` ya no basta: `listar` responde 403 con ese token solo.

### Pendiente
- Sin leer de 2026-11-04T14:00:38Z en adelante: lo retoma la próxima corrida. Sin búsqueda q en la relanzada.
- El 429 llegó a las 122 solicitudes; el 04-11 hubo 163 sin 429 y hoy a las 09:00 llegó a las 2. No hay umbral fijo a la vista; causa no verificada.
- El resto sigue del 04-11: merge de la sombra con `timeout-minutes` ~80, textos viejos, `fecha_cierre`, CSV de costos.

### Estado del repo
`main` en sync con origin, sin cambios de código. Rama de la sombra sin merge. `.claude/` sin seguimiento.

## 2026-11-04 — listado de Compra Ágil con presupuesto de 36 min

### Hecho
- Run 41825528757 (09:00): sin 429, 120 páginas en 18 min, 5.743 publicadas, correo con 382 ítems. El listado se
  cortó por presupuesto en la pág 12 del tramo 03-11 16:00; quedó sin leer hasta 04-11 12:00 (marca
  2026-11-03T16:00:38Z). Partió con un día de atraso por el 429 del 03-11.
- Primera corrida con rotativos por palabra medida: 5 rotativos no respondieron como frase; `e-learning`, `datos` y
  `gestión` a pausa; diario `digital` sin respuesta; diarios 15/16, rotativos 11/129.
- **Decisión:** `PRESUPUESTO_LISTADO_S` de 18 a 36 min; `timeout-minutes` de `scanner.yml` y de
  `probe-compra-agil.yml` de 50 a 70.
  Se descartó dejar los 18 min: un día normal son ~134 páginas según el modelo del verificador (~112 más 2 h de
  traslape) y 18 min leen 120, así que el listado se atrasa.
  Es mejor para el producto porque un día perdido por 429 se recupera casi entero en una corrida y lo publicado se
  lee antes de que cierre.
  Costo, no criterio: la corrida dura ~36 min un día normal y hasta ~55 en el peor caso realista; Actions gratis por
  ser repo público.
- Verificador: FALLA por dos líneas (timeout de la sonda; comentario «~20 min» en `scanner.yml`), corregidas.
  Simuló 429 en listado y en q: no se pierde marca, correo ni state. 64 tests OK. La API está modelada con el log: el
  primer dato real es la corrida del 05-11.

### Pendiente
- 05-11: mirar el log. Modelo del verificador: ~208 páginas, corrida de ~47 min, correo ~09:47, ~250-275 solicitudes
  (máximo sin 429 registrado: 214; la del 04-11 hizo 163). Sin plazo global en el scanner: si el job llegara a 70 min moriría antes
  de enviar el correo y guardar state; cota teórica ~107 min, riesgo preexistente, y el respaldo no lo rescata.
- Merge de la sombra: su rama trae `timeout-minutes: 65` en la misma línea; subirlo a ~80.
- Textos viejos sin corregir: `compra_agil.py:26-28` (~800 ítems, ~16 páginas); tras 429 en el listado el correo
  dice «sin respuesta» de diarios que no se pidieron; en `--universo` el corte dice 36 min y su límite es 40.
- Siguen del 03-11: verificador, merge y secrets de la sombra (fecha límite 15-11); CSV de costos de Anthropic;
  `fecha_cierre` de la API contra la ficha.

### Estado del repo
`main` con el cambio del listado subido. Rama de la sombra sin merge.

## 2026-11-03 — 429 en la corrida de las 09:00; prueba del universo; tope de la API

### Hecho
- Run 41632068088 (09:00): el listado de Compra Ágil recibió 429 a la 2.ª solicitud («límite de tasa», sin
  Retry-After). Se cortó Compra Ágil entera (listado y q) como está programado; la marca quedó en
  2026-11-02T12:00:38Z y la próxima corrida retoma desde 10:00:38Z (dentro del tope de 4 días). Correo con 10 ítems,
  sin Compra Ágil. Ninguna otra corrida de este repo usó la API entre el 2-nov 20:36 UTC y el 3-nov 12:00 UTC.
  Mismo patrón que el 27-oct (429 tras 3). Causa no verificada. La primera corrida con rotativos por palabra no
  alcanzó a medirse.
- Las 52 páginas del tramo 2-nov 10:00-16:00 UTC no son anomalía: el 30-oct 12-18 UTC fueron 34, y el 2-nov fue el
  primer día hábil tras el fin de semana largo.
- Sonda `--universo` (run 41676625042, 16:40 UTC): 24 h completas, 112 páginas, sin 429, **5.494 ítems**; 108 pasan
  el filtro por título. El diseño suponía ~900 por día (promedio de 3 días con fin de semana).
- API de Anthropic: la primera corrida de `privado/clasif/universo.py` falló con 400 «usage limits» (tope mensual
  de la organización US$10, gastado US$10,10). El tope se subió a US$25 con autorización. El gasto sale del crédito
  promocional (US$200 del 26-oct, **vence el 16-nov-2026**), que se consume primero. Recarga automática desactivada.
- Diferencia sin explicar: ~US$8,3 de Opus que el contador de gasto incluye y el CSV de costos (hasta 3-nov 17:58
  UTC) no muestra. Consulta a soporte, conversación 215476685979195: el bot no la resolvió.
- Prueba del universo clasificada (US$7,62): 142 «calza», el filtro por título deja pasar 31; la cascada Haiku → Opus
  pierde 1 de 142 y cuesta ~US$1,62/día hábil. Detalle en el repo privado.
- Cascada en sombra construida por subagente en la rama `worktree-agent-a3f30267570d183b2` (commits `e7baa8d` y
  `0ca0cdd`): `src/sombra.py`, lotes en paralelo (6 hilos), topes US$2,50/corrida, 12 min y fecha límite
  2026-11-15 23:59 Chile; correo de sombra aparte; 84 tests OK en la rama. Diff leído; **sin merge**.

### Pendiente
- Verificador sobre la rama de la sombra, merge y push; secrets `ANTHROPIC_API_KEY` (lo pone Sergio con
  `gh secret set`) y `RADAR_CLASIF_SISTEMA` (texto SISTEMA de `privado/clasif/clasificar.py`).
- Exportar mañana el CSV de costos de Anthropic por clave (diferencia de ~US$8,3).
- El cierre que trae la API de Compra Ágil puede no calzar con la ficha (2109-766: API 03-11 18:00, ficha 04-11
  18:00): revisar `fecha_cierre` antes de usarla para ordenar o marcar «cierra hoy».
- Primera corrida con rotativos por palabra sin medir (la de hoy cortó por 429): mirar el log del 04-11.

### Estado del repo
`main` con 2 commits del 02-11 más esta continuidad, sin push hasta el cierre. `privado/` con cambios sin commit.

## 2026-11-02 (tarde y noche, cierre) — 504 de q resuelto por palabra; clasificador medido; sonda del universo

### Hecho
- `q=` no se apaga: de los 191 ítems que solo trajo hoy, 2 calzan (895072-133-COT26, 5952-109-COT26) y no
  tienen keyword en el título, así que el listado no los ve. Cruce con `privado/clasif/set.jsonl`.
- Corrección a la entrada de la mañana: hoy fueron 12 solicitudes con 504 (~33 s cada una, ~6,7 min), no 14; los
  ~14 min son la búsqueda q entera, que gastó su presupuesto de 15. Diarios 12/12 (digital y audiovisual en el
  reintento), rotativos 14 de 24 intentados.
- Logs de 19 corridas (19-oct a 2-nov): 66 de 133 rotativos dieron 504 cada vez que se buscaron y nunca
  respondieron (sin fecha en `ca_ultima`); 11 más nunca se alcanzaron.
- Sonda `--palabras` (run 41520717922): de las 93 palabras de los 77 términos sin respuesta, 73 responden (200,
  3-7 s) y 20 dan 504, todas comunes (servicios, gestión, diseño, datos, producción, educación, desarrollo…).
- **Decisión:** el rotativo se pide como frase, igual que antes; si no responde, se pide palabra por palabra y
  se queda con la intersección de las palabras que respondieron completas. Las frases y palabras que fallan entran
  en pausa por apariciones (1/2/4/8, `state["ca_pausa"]`), no por días.
  Se descartaron dos alternativas. La pausa por días: el verificador midió que con la rotación real vence antes de
  que el término vuelva, así que no ahorraba nada en unas 2,5 semanas. Partir todos los rotativos en palabras con
  unión: palabras como «municipal» o «programa» (10 a 14 páginas en 3 días) llenaban el correo de ruido.
  Es mejor para el producto porque las frases que responden no cambian (ítems idénticos a HEAD, simulado) y las 77
  que no traían nada recuperan cobertura de título y descripción.
  Costo, no criterio: hasta 1,5 min más de búsqueda q por corrida (15,3 a 16,5 min contra 15 de presupuesto) y
  ~26 min de job estimado.
- Correo: el aviso distingue «no respondieron hoy» de «siguen en pausa y no se pidieron», y nombra los términos sin
  ninguna palabra que respondiera. El aviso de truncados es verdadero también para los rotativos.
- Verificador: FALLA (pausa por días; textos del correo), FALLA (textos del correo, doble solicitud de palabras de
  diarios), FALLA (3 textos), PASA. 64 tests OK.
- Términos que siguen sin cobertura de descripción porque todas sus palabras dan 504: gestión de medios, evaluación
  de política(s), e-learning, gestión de datos. Sus títulos los revisa el listado.

- Sonda `--ventana` (run 41517074064, 20:12 UTC): los 8 términos muertos dan 504 a los 29,5 s con ventanas de
  3 d, 1 d, 6 h y 1 h. La ventana no es la causa. Control «encuesta» con `publicado_hasta`: 200 con 0 ítems en las 4
  (q + hasta probablemente anula la búsqueda; no usar hasta con q).
- Buscador web (`buscador.mercadopublico.cl/compra-agil`, otro backend): «diseño web» 30-oct a 2-nov = 61
  resultados. Datos Abiertos de Compra Ágil solo publica cotizaciones mensuales del mes anterior: no sirve.

- Decisión del 02-11: «biometría», «biométrico», «biométrica» y «blockchain» pasan a términos diarios de q (16
  diarios). «cadena de bloques» sigue rotativa: q la parte en «cadena» (20) y «bloques» (31), casi todo ajeno.
  Costo, no criterio: 4 solicitudes más por corrida (~30 s); Actions gratis por ser repo público.

- Respaldo del cron (`scanner.yml`): el conteo de corridas de hoy filtra `--workflow scanner.yml`. Medido el
  02-11: sin filtro 3 (radar + 2 sondas), con filtro 1. Antes, una sonda manual hacía saltar el respaldo.
- CNA funciona: run 41441187390 leyó 40 noticias en /noticias/Paginas y 40 en /noticias/SiteAssets. El pendiente
  `CERTIFICATE_VERIFY_FAILED` del 31-oct estaba resuelto desde `3a14b63` (30-oct).

- Sonda `--universo` (para la prueba del 03-11): baja todo el listado de Compra Ágil de las últimas 24 h en tramos
  de 6 h y lo sube como artefacto `universo` (retención 3 días). Probada sin red con la API simulada (4 tramos, 8
  ítems, completo=True).

- Clasificador medido con Haiku, Sonnet y Opus 5.5 sobre el set de prueba, y parte 2 del diseño de selección
  escrita: detalle en el repo privado (`privado/docs/SELECCION-RADAR-2026-11-02.md` §4-8, `privado/clasif/`).

- Fuera de este repo, desde esta sesión: repos privados `gestor-documental` y `procesos-ia` creados en GitHub;
  respuestas del MINVU (AP001T0009186) y de CORFO (AH004T0008055) cotejadas en sus proyectos y aclaraciones
  ingresadas (AP001T0009436, AH004T0008155); `ESTADO.md` al día.

### Pendiente
- **Mar 3-nov, después de la corrida de las 09:00 (decisión del 02-11):** `gh workflow run probe-compra-agil.yml -f modo=--universo`; `gh run download <id> -n universo -D
  <scratchpad>`; `python privado/clasif/universo.py <scratchpad>/universo.json` (~US$1,2: Opus y Haiku sobre ~900
  ítems); se revisa `privado/clasif/universo-resultado.md`.
- Mar 3-nov 09:00: primera corrida con rotativos por palabra. En el log: «rotativos que no respondieron como
  frase», «palabras sin respuesta», duración de la búsqueda q, que no haya 429, e ítems del correo.
- El buscador web (`api.buscador.mercadopublico.cl`) responde lo que la API oficial no. Usarlo exige su credencial
  embebida: no se hace sin autorización de ChileCompra; decisión pendiente (requerimiento `INC-1408539-R5Z0W4`).
- Siguen del 02-11: tope o resumen del correo y clasificador dentro del radar; los dos dependen de la prueba del
  universo (orden de construcción en `privado/docs/SELECCION-RADAR-2026-11-02.md` §8).

### Estado del repo
`main`: el commit de cierre quedó sin push (lo frenó el clasificador de permisos; lo sube Sergio). `privado/` al día con su remoto.
Nada a medio camino. 64 tests OK. SDK `anthropic` 2.4.0 instalado en el PC (solo para `privado/clasif/`).

## 2026-11-02 — primera corrida con listado completo de Compra Ágil

### Hecho (medido en el log del run 41441187390, workflow_dispatch 12:00:19 → 12:24:55 UTC)
- Listado: 12 tramos de 6 h desde 2026-10-30T12:00:38Z, 62 páginas, 2.628 publicadas, 64 con keyword en el
  título, marca `__listado__` en 2026-11-02T12:00:38Z. ~10 min, dentro del presupuesto de 18.
- Búsqueda `q=`: 14 términos con HTTP 504 (digital, audiovisual, diseño gráfico, construcción industrializada…),
  ~14 min sin resultado. Correo enviado con 278 ítems nuevos.
- Medición del correo (subagente, título por título): 24 calzan, 30 dudosos, 224 ruido; `q=` trae 191 ítems con 2
  que calzan (el servidor busca cada palabra por separado). 134 de 278 cerraban en < 24 h al llegar el correo.
- radar-emprende no depende de este radar (grep con control positivo).

### Pendiente (técnico; ajustes aprobados el 02-11)
- Apagar `q=` o dejarla solo como respaldo (confirmar antes que el filtro del listado no pierde lo de descripción).
- Tope o resumen del correo. `--workflow scanner.yml` en el conteo del respaldo.
- Rediseño de la selección y ritmo de Compra Ágil (varias pasadas al día): diseño en
  `privado/docs/SELECCION-RADAR-2026-11-02.md` (parte 1 escrita). Prueba de clasificador en `privado/clasif/`
  (set de 1.143 ítems etiquetados, `build.py` y `clasificar.py`); clave de API verificada con Haiku 5.5; falta
  correr los tres modelos (medición de costo autorizada el 02-11).

## 2026-10-31 — separación del repo: código público, notas de negocio privadas

### Hecho
- Movidos a `privado/` (repo privado anidado): `continuidad.md` completa hasta el 30-oct, `triage/` (21 triages y
  `correo-radar-2026-10-29.txt`; las `bases-*` siguen fuera de git), `docs/DISENO-AGENTE-2026-10-12.md`,
  `soporte/reclamo-chilecompra-2026-10-29.txt`. Motivo: la Política de Seguridad v1.1 de TL (§4) pide información
  interna en repos privados; el revisor encontró notas de ofertas y nombres de personas en este repo público.
- Se descartó pasar todo el repo a privado: con la facturación de GitHub de octubre (737 min privados, US$4,42 de
  US$12 incluidos y en alza) el radar en privado podía agotar la cuota en noviembre y cortar las Actions de los demás
  repos privados. Las Actions de repos públicos no consumen cuota.
- Lo ya publicado sigue en el historial de este repo; reescribirlo es trabajo aparte (no hecho).

### Pendiente (técnico)
- Lun 2-nov 09:00: primera corrida con el listado completo de Compra Ágil; revisar en el log páginas por tramo,
  429, tiempo total (< 50 min) e ítems del correo.
- CNA: `CERTIFICATE_VERIFY_FAILED`.
- Respuesta de ChileCompra al incidente de la API (detalle en `privado/continuidad.md`).

### Estado del repo
`main`. `privado/` ignorado por `.gitignore`. Sin nombres de personas en este repo: dos comentarios de
`src/config.py` los tenían (30-oct y 02-11) y se quitaron el 02-11; siguen en el historial de git.
