# Continuidad — Radar de Licitaciones

## 2026-10-28 (miércoles, sesión raíz) — Compra Ágil: el daño es el 504 por término, no el 429

### Hecho
- Logs de las corridas del 20 al 28-oct leídos término por término (`gh run view --log`):
  - **504 fijo por término:** «diseño web», «redes sociales», «marketing digital» y «producción audiovisual» dan 504
    (~29 s, tope del API Gateway) en **todas** las corridas del 20 al 28-oct. El radar no ve Compras Ágiles de web,
    redes, marketing ni audiovisual desde hace al menos una semana. El 26-oct, 27 de 54 solicitudes fueron 504; los
    rotativos responden cerca de la mitad. Hoy también «economía circular».
  - **429 sin patrón de cuota diaria:** tras 15-17 (19 y 22-oct), 3 (27-oct, un día después de 54 sin 429) y 45 (hoy,
    12:15 UTC). Mensaje: «Se ha superado el límite de tasa de solicitudes». `Retry-After` nunca viene.
  - «diálogo social» trajo más de 5 páginas (>250): calza con `q` = cualquiera de las palabras.
  - Corrida de hoy `40684308702`: diarios 6/11, rotativos 9/23 intentados (cursor 33→56), 584 devueltas, 429 tras 45.
  - CNA cae ahora por `CERTIFICATE_VERIFY_FAILED` (antes, sin respuesta). No se tocó.
- `src/sources/compra_agil.py`: el 429 se rotula «límite de la API (429)», no «cuota diaria agotada», y el comentario
  del contador suma el dato del 27-oct.
- `src/probe_compra_agil.py`: modo por defecto nuevo, `alternativas`: cada diario que da 504 y sus palabras sueltas
  (encuesta de control positivo, frases de control negativo), dos rondas, 5 s entre consultas. Las sondas del 14 y
  16-oct quedan con `--variantes`. Push con el ok de Sergio («ok», 28-oct).
- Pruebas: 34 tests OK (no cubren compra_agil).

### Pendiente
- Lanzar la sonda (`gh workflow run probe-compra-agil.yml`) ~15:00 Chile, lejos del 429 de las 12:15 UTC y de la
  corrida de mañana; con el resultado, proponer reemplazo de los diarios ciegos (decide Sergio).
- Sergio: ver si salió el reclamo a ChileCompra del 14-oct (borrador en Gmail TL; no verificado desde aquí).
- CNA: certificado SSL.
- Siguen: empleo 37616 cerró el 28-10 00:59 sin decisión registrada; UNICEF CLE 244-2026 (9-nov); UNGM.

### Estado del repo
`main`. Commit de `src/sources/compra_agil.py`, `src/probe_compra_agil.py` y esta continuidad; push autorizado.

## 2026-10-27 (martes, sesión raíz) — revisión de la corrida del 27-oct

### Hecho
- Corrida `40500375502` (workflow_dispatch 12:00 UTC, 1m23s, success), log leído con `gh run view --log`:
  - Mercado Público: 4.794 activas, 80 coincidencias. PNUD Chile 0 entradas (Bolivia 2, Perú 2, Colombia 10, Argentina
    10, Ecuador 2, México 1, Global 494); PNUD 1 coincidencia. Empleos PNUD: 2 avisos. Total tras filtros 103; correo
    con 41 ítems.
  - **state.json subido**: `a2845a6`, push `2793cdf..a2845a6`. El paso con pull antes del push funciona.
  - 🔴 **Compra Ágil:** 504 en «diseño web» y después **429 tras 3 solicitudes, `Retry-After=None`** (el encabezado no
    viene). Diarios 1/11, rotativos 0/125 (cursor 33→33), 18 devueltas. Hoy la cobertura de CA quedó casi en cero.
  - CNA (`/noticias/Paginas` y `/SiteAssets`): sin respuesta.
- Commit del triage del 22-oct, que estaba sin seguimiento.

### Pendiente
- 🔴 Compra Ágil: con 3 solicitudes por corrida no se cubren los 11 términos diarios. Decidir entre espaciar las
  solicitudes, partir los términos en varias corridas al día o usar el segundo ticket (entrada del 22-oct). Sin
  `Retry-After` no hay cuánto esperar: medirlo.
- Sergio: empleo 37616 (cerraba el 28-10 a las 00:59), UNICEF CLE 244-2026 (9-nov), UNGM.

## Sesión 2026-10-26 (lunes, tarde) — PNUD Chile, inglés, empleos para Sergio; UNGM fuera por términos

Sesión raíz. Sergio, tras revisar PNUD Chile en LinkedIn: «tienes que incluir estas cosas en radar licitaciones» y
«agrega todo».

### Hecho

- **Triages del día** (formato §4): `triage/2026-10-26-compra-agil.md`, `-licitaciones.md` y `-fuera-del-radar.md`
  (UNGM y empleos PNUD). Bases bajadas en `triage/bases-2026-10-26/` (fuera de git).
- **Corrida de hoy falló al final:** push de `state.json` rechazado (otra sesión subió `78f35b0` durante los 20 min).
  El correo salió; el del 27-oct repetirá las 186 del 26. Arreglo en `scanner.yml`: `git pull --rebase --autostash`
  antes del push.
- **PNUD Chile tiene feed: CHI.xml** («listings are for CHILE»; CHL da 404, comprobado hoy). El código decía «Chile no
  tiene feed propio» y solo entraba por el global. Ahora entra completo, sin exigir keyword (`UNDP_FEEDS_SIN_KEYWORDS`),
  con exclusiones. Hoy 0 avisos (calza con procurement-notices: último aviso CHL del 8-sep).
- **Keywords en inglés** (`KEYWORDS_INCLUDE_EN` / `KEYWORDS_EXCLUDE_EN`) solo para fuentes internacionales, vía
  `matches_keywords_intl`. No tocan MP ni las búsquedas de Compra Ágil (125 rotativos y 11 diarios idénticos a HEAD;
  `matches_keywords` igual en 4.029 títulos de `data/audit-2026-07-08.csv`, verificador).
- **Fuente nueva `undp_empleos.py`:** empleos del PNUD (Oracle HCM, API pública sin token) en Chile y remotos
  postulables por externos; sección «Para Sergio: empleos PNUD (personas, no empresa)». Filtro: fuera contratos
  nacionales de otro país, «Nationals of», «Tier 1», pasantías. Hoy: 37616 (edición Mineduc UCE, cierra 28-10 00:59) y
  36499 (IPSA12 UNCDF remoto, 30-10). Si falla el detalle de un remoto no se marca visto y se reintenta.
- **UNGM no entra al Radar:** receta técnica probada (GET + token antiforgery + POST /Public/Notice/Search, HTML), pero
  los Términos 5.2 y 5.3 prohíben uso comercial e incluir su material en otro sistema sin permiso escrito. Lectura
  manual para triage sí (hoy: 56 avisos Chile, 9 fichas). Alertas UNGM Pro: costo no verificado.
- UNDP Careers no tiene consultores individuales (113 avisos: NPSA, FTA, IPSA, pasantías); los IC van por
  procurement-notices. CEPAL: cepal.org da 403 desde aquí; sus licitaciones probablemente en UNGM (no verificado).
- Pruebas: `tests/test_undp.py` (10 nuevas); 34 OK. Verificador: **PASA** con 4 observaciones; corregidas la 1, la 2 y
  la 4. La 3 (sin tzdata en Windows se usa UTC-3 fijo; en Ubuntu hay tzdata) queda documentada en el código.

- **869591-4-LE126 (DCCP, valorización de intangibles, 2.º llamado) descartada por Sergio el 26-oct.** Triage en
  `triage/2026-10-26-869591-4-LE126.md`: sin proyectos de valorización, TL sola llega a ≈ 45 puntos; solo con firma socia.

### Pendiente

- Revisar la corrida del mar 27-10 09:00, la primera con los cambios: en el log, `PNUD Chile` y `Empleos PNUD`, y que el
  push de state.json pase. El correo repite las 186 del 26 (esperado). Responsable: Claude, en la sesión del 27.
- Sergio decide el empleo 37616 (cierra 28-10 00:59) y el correo de interés a UNICEF CLE 244-2026 (cierra 9-nov).
- UNGM: decidir entre revisión manual semanal (como el BEO, lunes) o pedir permiso escrito a UNGM. Decide Sergio.
- Leer en el log el `Retry-After` del 429 de Compra Ágil (sigue de la entrada del 22-oct).

### Estado del repo

`main`. `c2b0078` (código, pruebas, workflow y triages del 26-oct) subido con el ok de Sergio («push», 26-oct).
`triage/2026-10-22-compra-agil.md` es de otra sesión: no entra.


## Sesión 2026-10-26 (lunes) — TGR 622-64-L126 descartada, desde la raíz

### Hecho

- Ficha leída hoy: el cierre se movió al **03-11-2026 15:00** (antes 27-10). Foro: 89 preguntas, respondidas el
  23-10 salvo 66 y 69; respuestas hasta el 29-10; viene modificación (70 participantes, dos versiones de 35).
- Nuestra pregunta 20: a socio único le cuenta su experiencia como persona natural de los últimos 5 años. Pero cada
  experiencia exige ser capacitación (79), contrato u OC ≥ $1.000.000 (87), RUT de mandante distinto (37) y
  respaldo del mandante (35). Sergio tiene un curso UST (honorario sin monto escrito) y lo de la DEP, sin respaldo.
- Pesos (bases, p. de evaluación): relator 25, metodología 20, experiencia 20, precio 20, integridad 5, formales 5,
  Sello Mujer 5. TL: 55-63 sin precio contra ~75-80 de una OTEC con 5 cursos.
- **Sergio, 26-oct: descartada.**

### Pendiente

- Ninguno por la TGR. Siguen los de la entrada del 22-oct.

### Estado del repo

`main`. Esta sesión commitea solo `continuidad.md`. `triage/2026-10-22-compra-agil.md` sin seguimiento es de otra
sesión: no se tocó. Sin deploy (es un Action).

## 2026-10-22 (jueves, tarde) — segundo ticket de Mercado Público como respaldo; 429 medido

### Hecho

- **Ticket nuevo de Mercado Público** (emitido el 22-oct, Sergio lo pegó en la sesión raíz). Probado contra la API v1
  (devolvió 1469-284-L126) y contra `api2` de Compra Ágil (OK; control con ticket falso → 401). El ticket del
  secreto `MERCADO_PUBLICO_TOKEN` (22-jun) también funciona en las dos: la corrida de hoy leyó 4.823 licitaciones.
- **Decisión:** el nuevo es solo de **respaldo**. Se usa cuando la API rechaza el principal, nunca ante un 429.
  Alternativa descartada: repartir consultas entre los dos para sumar cuota. Es mejor para el producto porque la cuota
  es por ticket y por día (guía Compra Ágil §4) y la guía dice que la cuota mayor se pide a ChileCompra (§4.3).
  Sumar tickets puede leerse como saltarse el límite y arriesga el bloqueo de los dos, y con eso caen también las
  licitaciones. Costo para nosotros (no fue criterio): igual en las dos opciones.
- Código: `src/sources/_tickets.py` (nuevo, `tickets()`). En `mercado_publico.py`, la v1 manda los errores como JSON
  `{"Codigo","Mensaje"}` con HTTP 2xx (ticket inválido: 203; peticiones simultáneas: 10500, medidos hoy). **Antes
  pasaban callados como 0 licitaciones.** Ahora se loguean, y un 203 pasa al respaldo. El error de `requests` ya no se
  imprime entero porque su URL lleva el ticket. En `compra_agil.py`, un 401/403 pasa al respaldo y repite el término,
  y el 429 deja en el log Retry-After, el mensaje y el número de solicitudes de la corrida. `scanner.yml` recibe
  `MERCADO_PUBLICO_TOKEN_2`.
- **El 429 no parece una cuota diaria fija.** Según los logs de Actions (estimado: el log no contaba solicitudes), el
  19 y el 22-oct llegó tras 15 a 17 solicitudes y el 20 y el 21-oct pasaron entre 45 y 51 sin 429. La guía no da la
  cifra: dice que depende del tipo de ticket (§4.1). El «10.000/día» de `audit_compra_agil.py` no tenía fuente y se
  corrigió el comentario.
- Verificador: **PASA** (96 de 100 comprobaciones en seco, sin red ni correo, y `state.json` intacto). Cuatro no pasan
  y no son defectos: dos esperan el texto antiguo del mensaje y dos prueban un `"203"` como texto, que no está medido.

### Pendiente

1. ~~Cargar el secreto~~ **Hecho:** Sergio cargó `MERCADO_PUBLICO_TOKEN_2` el 22-oct a las 20:22 UTC; aparece en
   `gh secret list`. No se verificó el valor: un secreto no se puede leer, y el respaldo solo corre cuando se rechaza
   el principal.
2. Leer en las próximas corridas la línea `cuota agotada (429) tras N solicitudes; Retry-After=…`. Si Retry-After es
   corto, el límite es por ráfaga y conviene espaciar las consultas. Si apunta al cambio de día, es cuota diaria y
   corresponde pedir a ChileCompra un ticket de mayor cuota (§4.3).
3. La rama `except ValueError` de `fetch_raw_activas` nunca corre: con requests 2.32 el `JSONDecodeError` cae en
   `RequestException`. El log sale igual. Ya pasaba antes del cambio.

### Estado del repo

`main`. Commit de este cambio y push. `triage/2026-10-22-compra-agil.md` es de otra sesión y no entra en este commit.

## 2026-10-20 (martes) — decisiones de cartera desde la sesión raíz «Todo»

### Hecho

- **1725-219-COT26 ENPCCL: descartada por Sergio** («lo de diagramar déjalo»): sin diagramador editorial para 150-200
  pp. en InDesign.
- **SLEP Los Parques 1375754-80: descartada**, cerró el 20-oct 12:00 sin los certificados (Gmail sin ellos).
- **Codegua 4732-27: descartada** (TL sin patente municipal; R1 del foro no acepta provisoria). Detalle en su carpeta.
- **Tralka 1469-284-L126:** no estaba enviada (escritorio de proveedor); se armó y se envió el 20-oct 10:28. Detalle en
  `../postulaciones/utalca-1469-284-tralka/continuidad.md`.
- **752-32-LP26 (GORE Los Lagos) y 5403-11-LP26 (CNA):** bases leídas, preguntas subidas al foro el 20-oct, carpetas
  nuevas en `../postulaciones/gore-los-lagos-752-32-parcc/` y `../postulaciones/cna-5403-11-gobernanza-datos/`.

### Pendiente

- Cada licitación en su carpeta de `postulaciones/` (Los Lagos espera a Pablo Badenier y David; CNA solo con empresa
  socia). Corrida diaria y foros siguen como en la entrada del 19-oct.

### Estado del repo

Solo esta entrada.
## 2026-10-19 (lunes, tarde) — Seremi 2122-34-LE26 ENVIADA (16:16)

### Hecho

- **2122-34-LE26 enviada** a las 16:16, a $8.900.000 neto. El comprobante y el detalle están en
  `../postulaciones/seremi-salud-2122-34-ia-cancer/continuidad.md` (entrada del 19-oct).
- Foro de la Seremi bajado otra vez: son las mismas 106 respuestas del 16-oct, y la v3 cumple R 8/9, 11/60, 14,
  26, 27, 59/76, 62, 64/105 y 71.
- El portal limita el nombre de cada archivo a 70 caracteres. Desde ahora los archivos que se suben llevan nombre
  corto (se anota en el kit).
- Incumplimiento: un `cd` encadenado. El guardia lo envolvió y quedó en memoria.
- **635-166-L126 (Arica): descartada por Sergio.** TTRR y anexos leídos (zip en
  `triage/bases-2026-10-19/635-166-L126/adjuntos-16-29/`, .doc pasados a texto con Word con macros desactivadas). Pide un
  equipo de cuatro perfiles certificados (Moodle, Scrum/PMP, UX/UI) y la experiencia vale 35 %: sola, TL no alcanza.
- Rapa Nui 1108734-32-COT26 y EPJA 1388-22-COT26: no van (Sergio, «de acuerdo con lo otro»). EPCO ya estaba descartada.
- **1375758-7-LE26 (SLEP Santiago Centro): foro leído** (26 respuestas, en `triage/bases-2026-10-19/1375758-7-LE26/`).
  **Sergio: «Vamos solos»** sobre `dotacion`. Repo nuevo `../licitacion-slep-santiago-centro-dotacion` (commit
  `add50d0`), con bases, foro y continuidad. La oferta sigue en una sesión abierta allá.
- Triage `2026-10-19-licitaciones.md` actualizado: candidatas 6 y 7.

### Pendiente

- Hoy: respuestas de foro de Codegua (18:00), Tralka (19:00) y 1067476-41-L126 (20:00). Cada una se mira en la
  sesión de su carpeta; esta sesión queda cerrada. El foro de 4375-137-LE26 cerró sin preguntas.
- Mar 20: revisar la ficha de la Seremi antes de las 15:00; foros de 5403-11-LP26 (16:00) y 752-32-LP26 (23:59), ambas
  CON SOCIO; F29 de septiembre.
- 1375758-7-LE26: en su repo (cierre lun 26-10 16:30).
- Proponer: anotar en la memoria `mercado-publico-bajar-bases` que los adjuntos piden captcha.

### Estado del repo

`main`. Esta entrada, los cambios del triage y `633499f` se commitean y se pushean en este cierre. Las bases bajadas en
`triage/bases-2026-10-19/` quedan fuera de git.

## 2026-10-19 (lunes, mañana) — corrida del Radar y triage del día; pausa hasta la tarde

### Hecho

- Corrida 09:00 OK, pero Compra Ágil agotó la cuota diaria (429). Respondieron 7 de las 11 búsquedas diarias: faltaron diseño
  web, redes sociales, marketing digital y producción audiovisual. De los rotativos corrieron 2 de 125. CNA: 40 + 40 leídas,
  0 llamados. ChileCompra noticias: 43 leídas, 4 avisos.
- Triages `triage/2026-10-19-licitaciones.md` (15 candidatas) y `triage/2026-10-19-compra-agil.md` (5). Bases en
  `triage/bases-2026-10-19/` (fuera de git).
- Foros pegados por Sergio:
  - 1469-286-L126 (U. de Talca), 4 preguntas sacadas de las bases leídas;
  - 1003780-1-LE26 (Nueva Alameda), 4 preguntas sacadas solo de la ficha: **error mío**. Las cuatro ya estaban respondidas
    en las bases, leídas después (Res. 1736, 86 pp.).
- Memorias: `foro-sin-bases-leidas` (nueva) y reincidencia en `cero-errores-cero-inferencias`.
- Desde hoy los adjuntos de Mercado Público («Ver adjuntos») piden reCAPTCHA Enterprise. Chrome se reconectó al
  mediodía, pero el clic en el clip no abre nada en la pestaña de la extensión: los adjuntos los baja Sergio.

### Pendiente (tarde)

- **Seremi 2122-34-LE26:** subir con `SUBIR.md` (cierre mar 20 15:00). **Decisión de Sergio (19-oct, 15:10):** el
  medio de verificación de integridad es solo su declaración firmada y el programa v1.2, sin las de Ismael y Andrés.
  Ellos recibieron el programa el 18-oct y, según Sergio, están de acuerdo (Ismael por WhatsApp). La página firmada de
  ninguno de los dos ha llegado. Ficha revisada a las 15:10: sigue el cierre 20-10 15:00 y el texto no trae
  aclaraciones; la lista de adjuntos no se pudo ver (captcha).
- Foro de 4375-137-LE26 (hoy 17:00): solo si Sergio baja los adjuntos y se leen antes.
- Respuestas de foro de hoy: 1375758-7-LE26 a las 16:30 y 1067476-41-L126 a las 20:00, además de Codegua 18:00 y
  Tralka 19:00.
- Mar 20: foros de 635-166-L126 (12:00, faltan los TTRR), 5403-11-LP26 (16:00) y 752-32-LP26 (23:59). Ninguna pregunta
  sin bases leídas. Compras Ágiles: Rapa Nui 1108734-32-COT26 (12:00) y EPJA 1388-22-COT26 (17:00), decide Sergio.
- Nueva Alameda: decidir si TL va. Hay que revisar si Sergio acredita 3 estudios cuanti + cuali (BT §10), conseguir los
  dos profesionales con 5+ años y cotizar el terreno de 1.500 encuestas.
- Proponer: anotar el captcha en la memoria `mercado-publico-bajar-bases`.

### Estado del repo

`main`. Commit local con los dos triages y esta entrada; sin push.

## 2026-10-18 (domingo) — Seremi Antofagasta 2122-34-LE26 auditada palabra por palabra y lista para subir el lun 19

Detalle completo en `../postulaciones/seremi-salud-2122-34-ia-cancer/continuidad.md` (entrada del 18-oct).

### Hecho

- **Oferta Seremi 2122-34-LE26:**
  - Tres auditorías afirmación por afirmación más el revisor de privacidad, todas guardadas en la carpeta de la
    oferta: v1 con 8 FALSA y 10 CONTRADICE; anexos; final de la v2 con 1 FALSA.
  - **Propuesta v3** (12 pp.), con textos aprobados por Sergio bloque por bloque. Salen las frases falsas sobre
    horario de oficina, «cota superior» y el servidor del RPC. Se agregan egresos, Ley 21.258 y DS 42, la experiencia
    de IA verificada y la nube solo para desarrollo.
  - Anexos fechados el 19-oct. Anexo 2 en la segunda opción, con las tres SpA relacionadas y sus RUT. Anexo 4 con
    País Circular y AFIPA (OC 007-2026). Respaldo de 5 facturas con correos tachados.
  - Programa de integridad v1.2 (contacto@), **rediseñado** sobre la plantilla de la propuesta, en 4 pp. y con
    recuadros gris azulado (Sergio: «sin beige»). Copia en `Downloads`.
  - Declaración de Sergio firmada. Borradores de Gmail a Ismael y a Andrés (este sin destinatario).
- **Reglas nuevas de Sergio:**
  - «cero errores cero inferencias», en `~/.claude/CLAUDE.md` §2 y en las memorias del proyecto, la raíz y el
    verificador;
  - no agregar compromisos con costo (memoria `no-agregar-compromisos-que-perjudican`).
- Corregido en memoria: Radar Circular SpA es de Sergio (RUT aparte para un concurso perdido; **no hay licencia a País
  Circular**, era falso).
- CFT Antofagasta: se le explicó a Sergio lo de Bettersoft (llamada del lun 19; preguntas en
  `cft-antofagasta-1113265-17-permanencia/certificado-u-plus.md`).
- Incumplimiento: `cd` encadenado una vez, frenado por el guardia y anotado en memoria.

### Pendiente

- **Lun 19 (Seremi):**
  - Sergio envía los correos de integridad con el PDF v1.2 adjunto, y en el texto cambia «página 3» por «página 4»
    (la declaración quedó en la p. 4).
  - Con las respuestas se arma el PDF del medio de verificación.
  - Revisar la ficha.
  - **Subir en la tarde con `SUBIR.md`** y bajar el comprobante (cierre mar 20 15:00).
- Web (`web-tercera-letra`): programa de integridad publicado en `/documentos` y `/integridad`, con commit local y **sin
  push ni deploy**. El borrador de Netlify se colgó dos veces desde la sesión: Sergio lo lanza con `!`, y el deploy va
  con DEPLOY-AUTORIZADO.
- Portafolio con la experiencia de IA documental: **después de subir**, en una sesión abierta en `marca`.
- Resto de la semana: entrada del 17-oct (EPCO mar 20, CFT Magallanes mié 21, CNE jue 22, ENPCCL jue 22, Bettersoft
  lun 19).
- Lun 19 09:00: log de la corrida del Radar (diarios X/11, CNA, ChileCompra noticias).

### Estado del repo

`main`. Solo esta entrada. El trabajo de la oferta vive en el repo `postulaciones`.

## 2026-10-18 (domingo, cierre de la sesión del 17-oct) — triage «fuera del radar», fuente chilecompra con PASA, Tralka enviada

### Hecho

- **Tralka 1469-284-L126 ENVIADA** (Sergio, 17-oct: «lo de tralka ya lo mandamos»). Falta mirar el comprobante en «Mis
  ofertas» si se quiere respaldo; respuestas del foro lun 19 19:00 por si piden reemplazar anexos antes del mié 21 16:00.
- **Triage `triage/2026-10-17-fuera-del-radar.md`** (formato §4): las bases que Sergio bajó a Descargas (7 procesos)
  están todas cerradas o en ejecución. Vigente y calza: **869591-4-LE126**, relicitación de la valorización NICSP 31 de
  las plataformas de ChileCompra, cierre **04-nov-2026 15:00**, veredicto **CON SOCIO** (firma o profesionales con 5+
  valorizaciones NICSP 31 / IAS 38; TL sola ≈39-45 puntos si repite la 554-B). Bases del -4 sin bajar: solo se ven en
  «Licitaciones Beta» con sesión de Sergio.
- **Fuente chilecompra.cl:** dos correcciones más después de la entrada del 17-oct: `71d1fbb` (tipo de código genérico,
  LS/R1; «licita»; la fecha de adjudicación no es cierre; cierre numérico dd/mm/aaaa) y `0245b8e` (el filtro de
  adjudicación mira solo la oración del cierre). 24 tests OK. **Verificador: PASA en la cuarta pasada** (corrida real:
  43 notas, ok, mismos 5 avisos). Casos borde bajos que quedan: abreviatura con punto entre «adjudicación» y el ancla,
  punto sin espacio entre oraciones; ya conocidos: un código inventado da un aviso de más, tope de 5 páginas, un solo
  cierre para dos IDs. Todos fallan hacia avisar de más.
- Barrido de «Licitaciones Beta» de otros organismos y de «Consultas al Mercado Beta»: **no hecho**. Lo primero exige
  sesión de Sergio; lo segundo tiene reCAPTCHA Enterprise (prohibido automatizarlo).

### Pendiente

- **Sergio:** iniciar sesión en Mercado Público en Chrome y dar permiso a la extensión para
  `consulta-mercado.mercadopublico.cl`; con eso se recorren Licitaciones Beta y Consultas Beta a mano (revisión semanal)
  y se bajan bases y foro de 869591-4-LE126.
- **Sergio:** decidir a quién se le pide ser socio para 869591-4-LE126 (cierre 04-nov 15:00). Contactarlo es de Sergio.
- Lun 19 09:00: en el log de Actions, «ChileCompra noticias desde …: N leídas»; el primer correo trae los 5 avisos.
- Resto de fechas de la semana: entrada del 17-oct tarde (Seremi, EPCO, CFT Magallanes, CNE).

### Estado del repo

`main`. Push en este cierre de `c16a6a3`, `71d1fbb`, `0245b8e` (fuente chilecompra), `b577f09` (otra sesión) y el commit
del triage con esta entrada.

## 2026-10-17 (sábado, tarde) — Seremi Antofagasta 2122-34-LE26 lista para subir

Detalle en `../postulaciones/seremi-salud-2122-34-ia-cancer/continuidad.md` (entradas del 17-oct tarde y noche).

### Hecho

- **Mediciones en Modal** (US$0,33 en total, cubierto por créditos; $0 cobrado): GPU L4 con Qwen3 8B/14B en lote,
  0,26-2,8 s por documento, 18-33 h para 100.000; CPU de 4 núcleos y 16 GB, 23-142 s, ≈1.630 h. La tabla del agente
  (30 s por documento) estaba ~10-45 veces sobre lo real. Equipo C (RTX PRO 4500, $10,4 MM) → **B (RTX PRO 4000 24 GB)**.
  El servidor del RPC no alcanza para la Etapa 3; sí para el uso anual. PC de Sergio (8 GB RAM, sin GPU) descartado.
- **Sergio: «estoy dispuesto a pagar el costo y trabajar gratis»** para ganar la primera experiencia de IA con
  mandante público. Cotización real por subagente → **precio al costo $8.900.000 neto ($10.591.000 con IVA)**, 4 viajes.
- Oferta completa en `postulaciones/seremi-salud-2122-34-ia-cancer/entregables/` (propuesta v1 10 pp., Anexos 1-5, 7,
  8, integridad, facturas con el correo del contacto tachado) y `SUBIR.md`. Revisor FALLA → corregido; verificador
  FALLA ×2 → corregido (sin tercera pasada).

### Pendiente

- **Lun 19:** Seremi 2122-34: medio de verificación del programa de integridad, OK a firma escaneada y a M1 ≥ 98 % /
  M8 ≥ 50 %, confirmar Anexo 2, teléfono de Guerra si acepta; **subir lun 19 en la tarde** (cierre mar 20 15:00).
  1606-35 y 1113265-17 ya tienen sus preguntas; llamar a Bettersoft (CFT); 19:00 respuestas Tralka (confirmar en «Mis
  ofertas» si Sergio la subió; cierre mié 21 16:00); foro 1782-17 GORE Antofagasta (jue 22). Corrida del Radar 09:00:
  log «diarios X/11», las líneas «CNA /noticias/...» (primera corrida real del aviso CNA) y «ChileCompra noticias
  desde …: N leídas» (fuente nueva; el primer correo trae 5 avisos si siguen abiertos). Menores de esa fuente en la
  entrada siguiente.
- **Mar 20:** F29 septiembre; 1317954-9 EPCO 23:55; 17:00 respuestas foro CNE.
- **Mié 21:** reemplazar en CFT Magallanes el respaldo con el RUN visible (antes de 16:00).
- **Jue 22:** regla de salida CNE (Negroni y un Integrante 2); 1725-219-COT26 ENPCCL.
- Aviso CNA a David: Sergio verifica terceraletra.cl en Resend y crea RADAR_CNA_TO; envía el borrador a la CNA.
- Si adjudican EDEVAL: confirmar por escrito los 45 días antes de aceptar la OC.

### Estado del repo

`main`. Esta sesión solo agrega esta entrada. La fuente chilecompra (entrada siguiente) quedó commiteada en local por
otra sesión, sin push: se sube con este push. `triage/2026-10-17-fuera-del-radar.md` sin commitear es de otra
sesión: no se toca.

## 2026-10-17 (sábado) — fuente nueva: noticias de chilecompra.cl (plataforma nueva y consultas al mercado)

Hueco: la API v1 de Mercado Público no devuelve los procesos de la «nueva plataforma modular» (869591-4-LE126:
«Los parámetros no son válidos») y las Consultas al Mercado (…-RFIPRI26) viven tras reCAPTCHA (prohibido
automatizarlo; no se intentó). Así se perdieron 869591-2-LE126 (plan de adopción, cerró 2-oct) y 1122317-2-RFIPRI26.

### Hecho

1. **`src/sources/chilecompra.py`** lee `https://www.chilecompra.cl/wp-json/wp/v2/posts` (API pública de WordPress,
   sin secretos) desde `state["cc_ultima"]` menos 48 h (`after` en hora de Chile: medido por el verificador con la
   nota 57124; primera corrida: 30 días). Se queda con licitaciones, consultas al mercado, convenios marco,
   compras coordinadas para proveedores y extensiones de plazo; saca IDs (LE126, LP26, LR26, RFIPRI26, RFIPUB26,
   RFI26, L126…; descarta el ID truncado «2317-3-RFIPRI26» de la nota del 5-oct) y el cierre del texto (la fecha más
   tardía tras «hasta / cierre / plazo / extiende…»; con hora si la trae). Lo cerrado no se manda; las horas se leen
   como UTC−4 para no descartar antes de tiempo. Sin filtro de palabras clave (Radar amplio). Ítems `CC::<id nota>`
   en `seen`: una extensión de plazo es nota nueva y vuelve a avisar.
2. **Posts «Organismo – fecha»** (categoría 8 «Normativa»; 45 entre 150 notas): cada uno es solo un PDF con el
   **manual de compras/adquisiciones** del organismo (abierto el de SLEP Aysén, 56931; los 45 enlaces son
   `Manual-de-…pdf` salvo dos oficios/cartas). No son oportunidades: se excluyen por categoría.
3. **Correo:** sección propia «ChileCompra: plataforma nueva y consultas al mercado». Si la API falla, va a
   «Fuente caída» (salida 3, Actions en rojo) y `cc_ultima` no avanza; un día sin notas no es caída. Fila en el
   heartbeat. Workflow sin cambios.
4. **Tests** (primeros del repo, `unittest`, sin red): `tests/test_chilecompra.py` + 7 notas reales en
   `tests/fixtures/chilecompra-posts-2026-10-17.json` y 5 casos sintéticos. `python -m unittest discover -s tests -t .`
   → 20 OK.
5. **Corrida seca real** (chilecompra.cl real, demás fuentes stub, sin correo, state en copia; `data/state.json`
   intacto): 44 notas en 30 días, **5 avisos**: 897096-1-LE126 (cierra 28/10 15:00), 869591-4-LE126 (04/11 15:00),
   1122317-4/-5-RFIPRI26 (18/10 18:00), 1122317-17-LR26 impresoras (09/11 15:15), 1122317-3-RFIPRI26 vehículos
   (20/10 23:55). Segunda corrida: 0 repetidos. Caída simulada: «Fuente caída», salida 3.
6. Verificador: FALLA (descartaba licitaciones de capacitación/talleres/seminarios con ID; extensión «vencía el 16,
   se extiende al 30» quedaba en el 16; título sin invitación con ID se perdía) → corregido con casos de prueba;
   sobre sus 93 notas de 60 días el resultado sigue en 5 abiertas.

### Pendiente

- Lun 19 09:00: primera corrida en Actions; buscar en el log «ChileCompra noticias desde …: N leídas». El primer
  correo traerá los 5 avisos de arriba si siguen abiertos.
- Menor: 1122317-5-RFIPRI26 (lubricantes) cierra a las 17:00 y el aviso conjunto dice 18:00 (una nota, un cierre).
- Un proceso que además salga en la API v1 (p. ej. un LR26) puede aparecer en dos secciones: no se cruza.
- Notas con cierre en tabla («16 de octubre Cierre de recepción de ofertas a las 15.00») toman la fecha que sigue
  a «cierre»; coincide hoy porque la apertura es el mismo día.

### Estado del repo

`main`. Commit local (sin push: lo hace la sesión principal) con `src/sources/chilecompra.py`, `src/scanner.py`,
`src/notifier.py`, `tests/` y esta entrada. `triage/2026-10-17-fuera-del-radar.md` es de la sesión principal: no se
commitea aquí.

## 2026-10-17 (sábado) — sesión raíz: Ñuñoa enviada, descartes y foros

Detalle de cada oferta en `../postulaciones/<carpeta>/continuidad.md`.

### Hecho

- **ENVIADA 1224957-658-COT26 Ñuñoa** (17-oct 10:12; $420/h, $5.997.600 con IVA). Cómo se llenan los campos de
  Compra Ágil (valor unitario neto × cantidad + IVA, detalle de 255 caracteres, fecha de vigencia) quedó en
  `postulaciones/_kit/KIT.md`.
- **Descartadas por Sergio:** 4027-283-COT26 Antuco («no hay imprenta») y 1233607-3-LE26 SLEP Iquique.
- **Foros subidos por Sergio:** 1606-35-LE26 AGCID (va con su experiencia de periodista, editor y autor) y
  1113265-17-LE26 CFT Antofagasta (va con Camino a la U; requisito habilitante del certificado de U+ de Bettersoft).
- 2122-34-LE26 Seremi Antofagasta: bases bajadas, equipo cotizado ($10,4 MM), oferta en preparación por agente.
- CNE 610-20-LE26: equipo Negroni (JP) + David; antecedente 2023 (ganó Centro de Energía U. de Chile).
- Alerta «sin inicio de actividades» eliminada del kit y de los SUBIR.md (Sergio: TL tiene inicio y está hábil).

### Pendiente

- **Lun 19:** 1606-35 y 1113265-17 ya tienen sus preguntas; llamar a Bettersoft (CFT); 19:00 respuestas Tralka
  (Sergio cree que ya la subió: confirmarlo en «Mis ofertas»; cierre mié 21 16:00); foro 1782-17 GORE Antofagasta (jue 22).
- **Mar 20:** 2122-34-LE26 Seremi (precio, anexos, revisor; subir antes del mediodía); F29 septiembre; 1317954-9 EPCO
  23:55; 17:00 respuestas foro CNE.
- **Mié 21:** reemplazar en CFT Magallanes el respaldo con el RUN visible (antes de 16:00).
- **Jue 22:** regla de salida CNE (Negroni y un Integrante 2); 1725-219-COT26 ENPCCL.
- Si adjudican EDEVAL: confirmar por escrito los 45 días antes de aceptar la OC.

### Estado del repo

Sin cambios de código del Radar en esta sesión; solo esta continuidad.

## Sesión 2026-10-17 (sábado) — pares evaluadores CNA para David y aviso automático en el Radar

Abrió el 16-oct en la noche con dos asuntos: el ingeniero eléctrico para la CNE 610-20-LE26 y los pares
evaluadores de la CNA (pedido de David Blanco en lo personal; Sergio también postularía).

### Hecho

1. **CNE 610-20-LE26:** Sergio consiguió a Juan José Negroni (Santo Tomás) como ingeniero eléctrico y quiere que vaya
   de **Jefe de Proyecto**, con David en el equipo. Análisis entregado: Negroni puntúa de jefe solo si tiene 7 años en
   demanda (proyección, planificación, tarificación); si lo suyo es transmisión, calza en Integrante 2. David no puede
   ser Integrante 2. En cualquier reparto falta una persona. **Otra sesión ya dejó el borrador** a Negroni (cc David,
   17-oct 11:45, «…te propongo como Jefe de Proyecto»); el de esta sesión no se creó para no duplicar. Le falta pedir
   el CV de David, el permiso de sus universidades para honorarios y la disponibilidad de 70 días (se le dijo a Sergio
   que lo agregue a mano). La CNE sigue en la otra sesión.
2. **CNA, histórico de convocatorias leído en crudo** (`../postulaciones/cna-pares-evaluadores/historico-convocatorias-2026-10-16.md`;
   fuentes bajadas en `fuentes/`, fuera de git): Ley 20.129 art. 19 exige llamados «a lo menos una vez cada dos años»
   y 10 años de ejercicio. Llamados documentados: pregrado 2016, institucional universidades+TP 2020 (885 elegidos,
   registro vigente desde 01-07-2021), solo TP 16-ene a 06-mar-2026. Nada abierto ni anunciado para universidades,
   pregrado ni postgrado (no leídas: actas posteriores al 22-jul-2026, Transparencia, Diario Oficial). Ni David ni
   Sergio están en el registro. Honorarios no publicados. Dos subagentes fallaron (investigador sin shell; general
   colgado dos veces): la lectura la terminó la sesión principal.
3. **Borrador a la CNA** (convocatoriapares@cnachile.cl, Gmail TL, `r-5742713182224881496`): fecha de la próxima
   convocatoria en las tres áreas, si pregrado/postgrado reciben antecedentes permanentes y cómo recibir aviso.
   Verificador FALLA (acotaba a universidades, llamaba «académico» a David) → PASA. Lo envía Sergio. WhatsApp a David
   enviado por Sergio (texto corregido: no prometer que el Radar le avisa directo todavía).
4. **Aviso CNA en el Radar** (`src/sources/cna.py` nuevo, `src/notifier.py`, `src/scanner.py`, workflow,
   `requirements.txt`): cada corrida lee por la API SharePoint las 40 últimas de `/noticias/Paginas` y
   `/noticias/SiteAssets`; un llamado a pares de los últimos 14 días manda un correo aparte «CNA: llamado a pares
   evaluadores» a RADAR_TO_EMAIL y, en envío separado y primero, a RADAR_CNA_TO (secreto nuevo, vacío hoy). Marcas
   `CNA:<FileRef>` y `extra:CNA:<FileRef>` en `seen`, fuera de las cifras del heartbeat. Filtro probado contra 471
   noticias y 536 archivos: calza todos los llamados históricos (2015, dic-2015, 2016, 2017, 2020, 2026), 0 falsos
   positivos. cnachile.cl no entrega el certificado intermedio: se agrega el público de DigiCert
   (`src/sources/certs/geotrust-ev-rsa-ca-g2.pem`, vence 02-07-2030) a certifi. Un fallo de la CNA no tumba el correo
   de licitaciones (va a «Revisión parcial»). Logs sin direcciones (repo público). Verificador FALLA (5 hallazgos) →
   PASA; luego cuatro ajustes menores, recompilado y filtro re-corrido.

### Pendiente

- **Para que el aviso le llegue a David:** Sergio verifica terceraletra.cl en Resend (DNS, gratis), cambia el secreto
  RADAR_FROM_EMAIL a una dirección del dominio y crea RADAR_CNA_TO. Hasta entonces el aviso llega solo a Sergio, con
  nota para reenviarlo. Medido en docs de Resend: onboarding@resend.dev solo entrega a la cuenta dueña.
- Lun 19, corrida de las 09:00: confirmar en el log las líneas «CNA /noticias/Paginas: 40 leídas…» y
  «CNA /noticias/SiteAssets…» (primera corrida real; no se probó en Actions).
- Sergio: enviar el borrador a la CNA; respuesta de la CNA.
- Error aceptado del filtro: «Se cierra la convocatoria de pares» daría un aviso de más (para no perder «se cierra el
  30 de noviembre»).
- `../postulaciones/cna-pares-evaluadores/` sin commitear: `fuentes/` son documentos de terceros (no van al índice).

### Estado del repo

`main`. Commit de cierre con el aviso CNA (`src/sources/cna.py`, `src/sources/certs/`, `src/notifier.py`,
`src/scanner.py`, `.github/workflows/scanner.yml`, `requirements.txt`) y esta entrada. Push autorizado por Sergio
(«si push y cierre por favor», 17-oct). Sin deploy (es un Action).

## Sesión 2026-10-17 (sábado) — portafolio de experiencia de TL (trabajo en `marca`)

### Hecho
1. Inventario de experiencia de TL por dos subagentes (repos y OneDrive): facturas solo desde folio 1 (03-08-2026); con pago documentado AFIPA, Agencia Circular y d-aloga; 12 plataformas propias en línea; CUECH y UST son honorarios de Sergio. Resumen en memoria `experiencia-tercera-letra` (raíz y este proyecto) y fila nueva en `postulaciones/_kit/KIT.md`.
2. Portafolio PDF en `marca/documentos/portafolio.pdf` (detalle en `marca/continuidad.md`, entrada 17-oct).
3. Guardia `guard-productos-inventados.ps1` arreglado (la última ficha de una sección heredaba los alias de la tabla siguiente; caso nuevo en el arnés, control negativo con la versión vieja).

### Pendiente
- Lun 19 09:00: primera corrida del Radar con las keywords nuevas y 11 diarios (log «diarios X/11», truncados, ruido de software/plataforma).
- Cambios sin commitear de otra sesión en este repo (`.github/workflows/scanner.yml`, `requirements.txt`, `src/notifier.py`, `src/scanner.py`, `src/sources/cna.py`, `src/sources/certs/`): no se tocan; los commitea quien los hizo.

### Estado del repo
`main`. Esta sesión solo agrega esta entrada; los archivos de arriba son de otra sesión.

## Sesión 2026-10-16 (viernes) — «Otros»: triage del día, fuera del Radar y seis ofertas

Detalle de cada oferta en `../postulaciones/<carpeta>/continuidad.md`.

### Hecho

1. **Triage del correo del 16-oct** (39 avisos) y **búsqueda fuera del Radar** (términos caídos de la API):
   `triage/2026-10-16-{ca-hoy,ca-semana,licitaciones,fuera-del-radar,859378-388}.md`. La otra sesión corrigió los
   huecos del Radar con ese archivo.
2. **Enviadas por Sergio hoy:** 859378-388-COT26 EDEVAL/UV ($2.899.160 neto; web $1.100.000 + video $1.799.160;
   45 días en el detalle; con Ramón Badillo, $1,2 MM brutos + $150.000 traslados; propuesta v5) y 757-457-COT26
   Minsal DIPOL ($1.168.067 neto; propuesta v2 + CV).
3. **Foros subidos por Sergio:** 1469-284-L126 Tralka (7 de 8), 610-20-LE26 CNE (12), 1233607-3-LE26 SLEP Iquique,
   4732-27-LE26 Codegua (17).
4. **Preparadas sin subir:** 1469-284-L126 Tralka (Anexo 3 v2, verificador PASA; $1.850.000 neto; cierra 21-oct
   16:00); 1224957-658-COT26 Ñuñoa (propuesta v3 + ficha técnica v1; modelos abiertos en servidores de TL;
   $483/h neto = $6.897.240 con IVA; 30 % al mes 1 + 11 cuotas; costos en `costos.md`, medición en Modal en curso;
   falta revisor). Análisis listos: 553368-111-COT26 UTA, 1375754-80-COT26 Los Parques, 696713-81-COT26 Fiscalía,
   4732-27-LE26 Codegua, 1782-17-LE26 GORE Antofagasta, 1113265-17-LE26 CFT Antofagasta.
5. **Descartadas por Sergio:** 2460-1011, 721703-140, 1238111-118 (Claude Team sin margen), 2296-633 (sin
   certificados), 2320-147, 1891-13; en la noche, 553368-111-COT26 UTA (sin videos con IA acreditables) y
   696713-81-COT26 Fiscalía (exige Comunicador Audiovisual titulado). 1375754-80-COT26 Los Parques: se suelta para
   no quitarle horas a 2122-34-LE26 Antofagasta (Sergio: «sí vamos, por supuesto»), salvo que el lunes temprano lleguen
   sin esfuerzo tres certificados; pedirlos igual a AFIPA, País Circular y d-aloga (sirven para Tralka y GORE).
   Ñuñoa: medición en Modal (US$0,35) deja $3,2-4,4 MM para TL → presentar.
6. Kit: `postulaciones/_kit/propuesta_compra_agil.py` (generador con el formato EDEVAL v7). `marca/PRODUCTOS.md`:
   URL de Firulais confirmada por Sergio.
7. Memorias nuevas: `codigos-completos`, `una-cosa-a-la-vez`, `honestos-sin-desnudarse`. Incumplimiento: abrí
   demasiados frentes en paralelo (Sergio: «vamos en orden… si pones todo a la vez hacemos doble trabajo»); además
   dos subagentes encadenaron `cd` (frenado por el guardia, anotado).

### Pendiente

- **Lun 19:** 1224957-658-COT26 Ñuñoa 15:00 (medición, revisor, subir); 4027-283-COT26 Antuco 11:00 (sin
  empezar); 553368-111-COT26 UTA 12:00 (sin videos con IA acreditables: soltar); foro 1606-35-LE26 AGCID 12:00;
  foro 1113265-17-LE26 CFT Antofagasta 23:59; 19:00 respuestas Tralka → anexos 1, 2, 4 y difusión de integridad.
- **Mar 20:** 1233607-3-LE26 SLEP Iquique 15:00 (oferta sin armar); 2122-34-LE26 Seremi Antofagasta 15:00
  ($26 MM; foro leído el 16-oct: subcontratación prohibida, sin profesionales de salud exigidos, producción 100 %
  local sin GPU en el RPC —el hardware puede ir en la oferta—, instalación presencial; veredicto PRESENTAR solos;
  Sergio decide hardware con GPU y precio; ver su continuidad); 1317954-9 EPCO 23:55; 1375754-80-COT26 Los Parques
  12:00 solo con 3 certificados; 696713-81-COT26 Fiscalía: soltar salvo comunicador audiovisual titulado.
- **Mié 21:** subir Tralka. **Jue 22:** 1725-219-COT26 ENPCCL (sin empezar), foro 1782-17-LE26 GORE Antofagasta.
- Si adjudican EDEVAL: confirmar por escrito los 45 días antes de aceptar la OC (la ficha decía 1 día).

### Estado del repo

`main`: esta entrada y los cinco triages del 16-oct. Push autorizado por Sergio («cerramos», 16-oct).

## Sesión 2026-10-16 (viernes, tarde) — huecos del Radar y formato estable de triage

### Hecho

1. **Keywords (`56b4dd2`):** de las 17 que `triage/2026-10-16-fuera-del-radar.md` encontró fuera del Radar, 15 entran
   ahora. Conectores opcionales en inclusión cuando la keyword los trae («ESTUDIO PERCEPCIÓN» calza «estudio de
   percepción»); 28 keywords nuevas (audiovisual, software, plataforma, indicadores, convivencia, plan municipal de
   cultura, diseño gráfico, intranet, e-learning, datos…), «video» como palabra; exclusiones de ruido medido
   (licencias de software, pav., laringoscop, endoscop…). Julio: 63 → +30, salen 0; triages 15-16 oct: 0
   regresiones (licencias Claude Pro siguen entrando). Verificador FALLA («licencia» global, «ley rep» con
   conectores) → PASA. Siguen fuera: 1113265-17-LE26 (título «Adquisición…», cierra 06-nov, buscar a mano) y
   1261-37-LR26 (humedales, a propósito). Rotativos de Compra Ágil: 92 → 121.
2. **Semántica de `q` medida** (sonda `probe_compra_agil.py`, run 38938450758): calza CUALQUIER palabra, «sitio web»
   = «sitio» ∪ «web» exacto; también busca fuera del nombre. Diarios de Compra Ágil 15 → 11: salen «sitio web»,
   «página web», «portal web», «plataforma web» (las cubre «diseño web», que trae todo «web»; siguen rotando, 125
   rotativos). Primer intento («web» y «audiovisual» solas) dio FALLA en el verificador: perdía la cobertura diaria
   de «diseño» y «producción», por la que llegaban el folleto de Antuco 4027-283 (PRESENTAR) y 4066-425. Versión
   final PASA. Log ahora «diarios X/11».
3. **Pedido de Sergio: «que el agente no pregunte y cambie todo cada sesión... formatos, forma de ver las cosas».**
   Skill `tercera-letra-licitaciones` §4 nueva: esqueleto fijo del triage (H1, Resumen con 9 columnas fijas, Cómo se
   leyó, Candidatas con veredicto en el título, Ruido), cinco veredictos, qué no se pregunta y qué se confirma, y
   regla de estabilidad (proponer en una línea, seguir con lo vigente; cambia solo si Sergio lo pide). Guardia
   `~/.claude/hooks/guard-formato-triage.py` (PostToolUse, triages desde el 17-oct) con arnés 14/14, sumado a
   `test-guardias.ps1` (todos pasan) y control positivo en vivo. Memoria `criterio-estable-entre-sesiones`.

### Pendiente

- **Lun 19, primera corrida con todo esto:** log «diarios X/11», términos truncados (>250) en «diseño web»,
  «producción audiovisual» y las keywords de una palabra (plataforma, software, indicadores, convivencia); ruido de
  «software» y «plataforma» en el correo.
- Los triages del 16-oct no siguen el formato nuevo (son anteriores al guardia); no se reescriben.

### Estado del repo

`main`. Push autorizado por Sergio («haz todo lo necesario para que esto funcione», 16-oct). Los cinco triages del
16-oct sin commitear son de otra sesión: no se tocan.

## Sesión 2026-10-16 (viernes) — tres ofertas enviadas: SEC, Illapel y Los Ríos

Sesión `radar-licitaciones-35` (abrió el 15-oct en la noche). Detalle de cada oferta en
`../postulaciones/<carpeta>/continuidad.md` (entrada «⇢ 16-oct-2026 — Cotización enviada»).

### Hecho

1. **SEC 1614-61-COT26, enviada antes de las 10:00:** $2.490.000 IVA incluido (el precio de `como-ganamos.md` §4; una v6 a
   $2.963.100 fue un error de lectura y quedó renombrada «NO SUBIR»), vigencia 15-11-2026, propuesta v5, CV de Sergio
   corregido en el PDF (`sec-…/CV Sergio Molina 2026-10 (corregido).pdf`: especialización 1991, contacto@terceraletra.cl) y
   título de doctor.
2. **Illapel 3512-182-COT26, enviada ~09:50:** $5.200.000 (se mantuvo tras el análisis: con 20 días el plazo ya hace el
   trabajo que hacía la rebaja), despacho $0, vigencia 15-12-2026. Propuesta **v16**: Sergio la editó en Word (v14/v15) y
   encima van las correcciones del verificador; resumen ejecutivo con producto principal, cuadro «lo que pide la
   Municipalidad» y cuadro «más allá de las bases» (plazo, Vecindato©, tres miradas, dashboard, acompañamiento en SIRECC);
   §1 «Comprensión del requerimiento»; §8 Experiencia con las plataformas de TL (URL verificadas 200 hoy). Oferta económica
   con firma escaneada (autorizada); carta de Lorena firmada a mano (llegó 08:10). Verificador PASA.
3. **Los Ríos 5418-72-COT26, enviada ~11:30, variante «con Fernandez»:** $7.170.940 (al tope; $6.026.000 neto), **60 días
   19/26/15**, **sin encuestadores**, 4 días de terreno, firma escaneada. Respaldos de Kena desde fuentes públicas (~9 años con
   documento: Seremi DS 33/2014 y BGI 2017, actas de Peñalolén 2018-2022, Decreto 148/2025 SENAME); su CV sin contacto ni el
   diplomado ODCA; Kena aceptó por WhatsApp. Propuesta v4 editada por Sergio en Word. Viaje cotizado: $1,12-1,43 MM. 16
   adjuntos desde `SUBIR-HOY/`. Verificador PASA tras tres rondas; revisor PASA.
4. **Criterio de redacción de Sergio aplicado a las tres:** nada de «DDLS» ni jerga ante el evaluador («herramienta digital
   de participación ciudadana de Tercera Letra»), «dashboard» en vez de «tablero», resumen que se lee de un vistazo, sin
   lenguaje de IA. Memorias nuevas: `aprobar-antes-de-generar` (incumplí una vez: generé el resumen sin mostrarlo) y
   `compra-agil-formulario` (detalle ≤255 caracteres, despacho, sin campo de plazo, vigencia = validez de la oferta).

### Pendiente

- **Hoy 17:00:** foro CNE 610-20-LE26 (`postulaciones/cne-610-20-demanda-ia/PEGAR-EN-FORO.txt`). No se tocó en esta sesión.
- Comprobantes de envío de las tres en el correo; captura del «acepto» de Kena; «sí» de Viviana Rivera (SEC).
- **CV maestro de Sergio:** sigue diciendo TL «desde 2019» y CORFO «Coordinador General» (debe ser «apoyo en la coordinación
  general»); no hay fuente Word, solo PDF.
- Sáb 17 foro SLEP Iquique 1233607-3; lun 19 foro AGCID 1606-35 y lista de Sebastián → EPCO (cierra mar 20 23:55).
- **Construir Vecindato©** antes del día 3 si Illapel adjudica (prometido en futuro en la propuesta); revisar «Vecindato» en
  INAPI y nic.cl.
- `postulaciones/` sigue con carpetas sin commitear (Illapel, SEC, Los Ríos, EPCO, foros, `_kit/`) con CV y respaldos de
  terceros: commitear solo tras revisar qué entra al índice. `respaldos/kena-fuentes/` trae el decreto con su RUN visible.
- Si adjudican: Los Ríos acepta OC en 24 h hábiles; Illapel, el mismo día; renovar la habilidad en Mercado Público antes del
  01-12-2026.

### Estado del repo

`main`. Esta sesión solo agrega esta entrada. Quedan sin commitear cuatro triages del 16-oct
(`triage/2026-10-16-ca-hoy.md`, `-ca-semana.md`, `-fuera-del-radar.md`, `-licitaciones.md`) que no son de esta sesión: no se
tocaron ni se incluyen; los commitea la sesión que los escribió.

## Sesión 2026-10-15 (jueves, tarde) — ofertas del 16-oct: Illapel, SEC, Los Ríos y EPCO

Sesión `radar-licitaciones-34`. A media tarde Sergio cerró la otra sesión («Ajuste del agente»), que llevaba las
mismas ofertas: desde ahora todo vive acá. Detalle de cada oferta en `../postulaciones/<carpeta>/continuidad.md` y
`SUBIR.md`.

### Hecho

1. **Illapel 3512-182-COT26** (`postulaciones/illapel-3512-182-plan-seguridad/`), vigente **v11**
   (`entregables/… Plan de Seguridad Illapel v11.pdf`). Decisiones de Sergio: abogada **Lorena Escalona González**
   (CV en `equipo/`, versión sin datos personales en `entregables/`), $500.000 brutos, la oferta muestra solo **12
   horas**, trabajo remoto; precio $5.200.000; **plazo 20 días** («baja al mínimo los plazos»; el criterio vale 20 %);
   la encuesta va en **Vecindato** (nombre elegido tras búsqueda rápida; DataVecinal/Vecindatos chocan con «Dato
   Vecino» del INE), módulo de encuesta cerrada que **se construye** sobre DDLS desde el 16-oct; la difusión y el
   alcance son del municipio; papel solo como el Word/PDF del producto 2 (lo exigen las bases). Datos de seguridad
   desde `agoralab/ddls/data/seguridad-comunal.json` (CEAD 2025): incivilidades 62 % sobre la tasa del país, robos
   violentos un cuarto. §4.4 «tres miradas» (vecinos, Consejo Comunal, cifras). Verificador: FALLA ×3 → PASA (v10);
   revisor: FALLA ×3 → PASA con umbral de 5 personas repuesto (v11).
2. **DDLS es de Tercera Letra** (código y plataforma); de David y Pablo es solo la metodología VLR/ISO-ODS
   (Sergio). Memoria `ddls-propiedad`.
3. **SEC 1614-61-COT26**, vigente **v5** (`Propuesta tecnica - Curso IA Directivos SEC v5.pdf`): Sergio relator
   único (opción C, §11 declara los tres requisitos del §4 que no cumple); coordinadora técnica **Viviana Rivera
   Barrientos** (no es co-relatora: no tiene docencia en IA); plataformas de TL con URL verificadas (200); tablero en
   vivo con datos públicos en sesiones 6 y 8. Verificador PASA.
4. **Los Ríos 5418-72**: honorario de **Kena $1.800.000** brutos (25/50/25, ~60 h); Sergio le envió el WhatsApp.
5. **EPCO 1317954-9**: psicólogo **Sebastián Rodríguez Gómez de la Torre** (`Downloads\CV SR 2026.docx`), rol
   acotado ~6 h, $200.000; se le pidió la lista de estudios de clima.
6. Investigador: el DS 661 no fija plazo para aceptar la OC ni desde cuándo corre el plazo; aceptar el mismo día.
7. Nombres de archivo: «<Pieza> - <tema> vN» (pedido de Sergio; KIT.md §4 y memoria `nombres-archivos-oferta`).
8. Incumplimiento propio: `cd` encadenado una vez (lo frenó el guardia).

### Pendiente

- **Vie 16:** 09:00 corrida del Radar (log «diarios X/15»). 10:00 SEC: aceptación de Viviana, fecha del CV (1991),
  ficha de proveedor, subir v5. 16:00 Illapel: carta firmada de Lorena (llega la noche del 15), CV de Sergio (dice
  2019 y CUECH de TL), firmar oferta, subir v11. 17:00 foro CNE 610-20-LE26 (`PEGAR-EN-FORO.txt`). Los Ríos:
  papeles de Kena antes de 18:00 → variante «con Fernandez» (tachar, revisor, generar); si no, «solo Sergio»; 22:00.
- Sáb 17 foro SLEP Iquique 1233607-3-LE26; lun 19 foro AGCID 1606-35-LE26 y lista de Sebastián → ajustar EPCO
  (21 h → ~6 h); mar 20 23:55 cierra EPCO.
- **Construir Vecindato** (encuesta cerrada sobre DDLS: sector, sexo, edad, ítems de victimización, cuentas de
  digitación, consentimiento, umbrales) desde el 16-oct; pasa por el revisor antes de abrir.
- Revisar en INAPI y nic.cl «Vecindato» antes de usarlo fuera de Illapel.
- `postulaciones/` tiene carpetas nuevas sin commitear (Illapel, SEC, EPCO, Los Ríos, foros, `_kit/`) con CV y
  respaldos de terceros: commitear solo tras revisar qué entra al índice.

### Estado del repo

`main`, sin cambios de código en esta sesión; solo esta entrada. Push autorizado por Sergio («haz el cierre y push»,
15-oct). La próxima sesión se abre en `radar-licitaciones`.

## Sesión 2026-10-15 (jueves) — triage para ganar, kit de postulación, ajustes de Compra Ágil

### Hecho

1. **Primera corrida real de la búsqueda q (09:00, run 38731386940):** diarios 7/15, rotativos 8 de 34 intentados,
   20 min de presupuesto agotados; 57 Compras Ágiles en el correo, 45 con «(en descripción, sin verificar)».
   Medido: `q` calza palabras sueltas, no la frase («economía circular» trajo una aguja circular), así que la
   etiqueta era falsa; pero de esas 45 salieron 10 de las 19 candidatas del triage (Los Ríos, CFT, Illapel). El
   reintento inmediato de 9 diarios recuperó 1 y costó ~4 min.
2. **Ajustes (sin commitear hasta el cierre):** ítems sin keyword en el nombre van a la sección
   `FUENTE_PALABRA_SUELTA` («Compra Ágil · por palabra suelta»), al final del correo, con match «búsqueda «término»»;
   el segundo intento de los diarios fallidos va después de los rotativos, que dejan 30 s por fallido + un TIMEOUT
   de reserva; si ningún diario respondió en la primera pasada, el reintento va de inmediato. Verificador: FALLA
   (regresión: con todos los diarios recuperados en el reintento no corrían rotativos) → corregido; arneses en
   `%TEMP%\radar-test-15oct\` 10/10, 17/17 y 9/9 reintentos con rotativo de 60 s. Prueba real: corrida del 16-oct.
3. **Pedido de Sergio: triage para ganar.** «me dice que no a todo… debe evaluar para presentarse y ganar».
   Skill global nueva `~/.claude/skills/tercera-letra-licitaciones/SKILL.md`: abrir todo, leer adjuntos sin
   preguntar, «cómo ganamos» por candidata, NO solo con requisito textual + página + sin forma de cubrirlo, ordenar
   por plata y plazo. `CLAUDE.md` nuevo en este repo que la apunta. `triage/bases-*/` fuera de git.
4. **Kit de postulación** `postulaciones/_kit/KIT.md` (pedido: «agrupe toda la memoria de presentaciones en un solo
   lugar»): papeles de la empresa copiados de Descargas a `_kit/empresa/` (fuera de git), datos fijos, alertas y
   versión buena de cada pieza. Inventario por subagente. Verificador FALLA (12 puntos) → PASA; revisor PASA (5
   archivos con datos de terceros sacados del índice de git de `postulaciones`, siguen en disco; reescribir el
   historial lo decide Sergio).
5. **Ficha de Mercado Público:** se vio una vez «Proveedor sin inicio de actividades» en `/ficha/idoneidad/` mientras
   la sección SII daba error de servidor; no se reprodujo. Carpeta tributaria del 15-oct 13:20 y la DJ de inicio de
   actividades del SII (folio 18745554101, en el kit) dicen 08-10-2020. Llanquihue no se afecta (§8.6.1 pp. 11-12
   pide RUT de la sociedad y cédula; §13.2.2 c pide a sociedades Ley 20.659 vigencia y estatuto). Si adjudica:
   cédula legalizada ante notario (§13.2.2 f).
6. **«Vamos con todo»:** subagentes preparando ofertas en `postulaciones/`: SEC 1614-61 (curso IA, cierra 16-oct
   10:00), Illapel 3512-182 (plan seguridad, 16-oct 16:00; Sergio pidió carta de compromiso a una amiga abogada por
   WhatsApp), Los Ríos 5418-72 (16-oct 22:00; ojo: la sesión raíz también lo trabaja), CNE 610-20 (foro hasta
   16-oct 17:00), SLEP Iquique 1233607-3 y AGCID 1606-35 (foros 17 y 19-oct), EPCO Coquimbo 1317954-9 (20-oct).

7. **Resultado de las ofertas (tarde):** SEC v3 (con socio/OTEC recomendado; $2.490.000; falta coordinador
   técnico; reexportar PDF desde el Word v3), Los Ríos v2 en dos variantes «solo Sergio» y «con Fernandez»
   ($6.902.000 aprobado por Sergio; Kena entra, debe mandar papeles antes del 16-oct 18:00; DDLS va: «la parte
   informática es mía»), EPCO v3 (psicólogo 21 h por $400.000 brutos; precio $900.000), foros listos en
   `PEGAR-EN-FORO.txt` de CNE, SLEP Iquique y AGCID. **Illapel pasó a la sesión radar-licitaciones-34** a pedido de
   Sergio (subagente detenido; dejó v4 sin verificar y el CV de Lorena Escalona sin datos personales). Todas las
   propuestas con el formato de la edición de Sergio del CFT v5 (memoria `estilo-propuestas-de-sergio`).

### Pendiente

- Vie 16: SEC antes de 10:00; foro CNE antes de 17:00; Los Ríos antes de 22:00 (papeles de Kena a las 18:00).
  Sáb 17 18:00 foro SLEP Iquique; lun 19 12:00 foro AGCID; mar 20 EPCO (CV y respaldos del psicólogo).
- Vie 16 09:00: mirar la corrida (log «diarios X/15», sección por palabra suelta al final).
- Sergio: carta de la abogada para Illapel; subir ofertas y pegar foros según el calendario.
- Otra sesión: CV maestro, un solo respaldo de experiencia, traer `marca/experiencia/` al kit; F0 del agente.

### Estado del repo

`main`. Commit de cierre con `.gitignore`, `CLAUDE.md`, `src/config.py`, `src/notifier.py`,
`src/sources/compra_agil.py`, `triage/2026-10-15-*.md` y esta entrada. Push autorizado por Sergio («push», 15-oct).

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
   **Segunda sonda (run 38570157442):** q tampoco es rápido (5-29 s; «capacitación» 504 ×2). Barrer 110 términos
   no cabe.
3. **Opción 1 implementada (decisión de Sergio: «dale con la opción 1»):** el radar diario ya no barre el
   listado. Busca con `q` 15 términos diarios (`COMPRA_AGIL_TERMINOS_DIARIOS`) con segundo intento, y con el
   tiempo que sobra rota los otros 92 de `KEYWORDS_INCLUDE` desde `state["ca_cursor"]` (pedido de Sergio: «hacer
   otras búsquedas por otro lado con las palabras que falten»). Cada término busca desde su última búsqueda
   exitosa y no truncada (`state["ca_ultima"]`, piso 3 d, techo 14 d). Sobre resultados q no se aplican las
   exclusiones «adquisición», «compra de», «suministro» (casi todo título CA empieza así: botaban los 9 de IA).
   Si el nombre no trae keyword, el match se rotula «(en descripción, sin verificar)». Caída (rojo) solo si ningún
   diario responde, y entonces no rota; diarios fallidos, corte por 429 y términos >250 resultados van como aviso
   amarillo «Revisión parcial» sin rojo. `web`, `digital`, `ia` no se buscan con q (declarado en config).
   Presupuesto 20 min, job 40 min. Verificador: FALLA (8 hallazgos) → FALLA (2 menores) → **PASA**. Arnés offline
   43/43 en el scratchpad de la sesión (no versionado). **No probado aún contra la API real:** primera corrida
   real = cron-job.org del jue 15-oct 09:00.
4. **Borrador a ChileCompra en Gmail TL** (sin destinatario; asunto «API Compra Ágil (v2): consultas de listado
   cortan a los 29 segundos (504) desde agosto 2026»), verificado (hash 305083f79499a0ba, 3 pasadas). No hay correo
   de soporte de la API verificado: el canal oficial es el formulario de requerimientos de ChileCompra con
   ClaveÚnica (ChileAtiende). Lo envía o pega Sergio.

### Pendiente

- **Jue 15-oct:** mirar la corrida de las 09:00 (log «Compra Ágil: diarios X/15 ok, rotativos Y/92») y el
  correo: cuántos «en descripción» trae y si son ruido. Si un término trunca seguido, subir `MAX_PAGINAS_TERMINO`.
- Sergio: enviar el borrador a ChileCompra por el formulario.
- 22-10 18:00: respuestas del foro de 622-64-L126.
- Siguen los del 12-oct.

### Estado del repo

`main`, todo commiteado y pusheado: sonda `7176d77`/`fec7560` (workflow manual `probe-compra-agil.yml`, se puede
volver a correr), búsqueda q `20943e8`, esta entrada en el commit de cierre. Sin deploy (es un Action). Bases
leídas hoy en `Descargas\` (fuera del repo): `Bases_765-25-L126.pdf`, `Bases_622-64-L126.pdf`,
`PDF3337-21-LE26.pdf` (ficha, no bases).

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
