# Agente de oportunidades — diseño, 12 de octubre de 2026

Documento interno. Escrito desde la raíz del portafolio contra `ESTADO.md` (leído entero hoy), la continuidad de
`radar-licitaciones`, `marca/PLAN-COMPETITIVIDAD-2026-10-03.md`, `marca/POSIBILIDADES-2026-10-07.md` y
`marca/experiencia/`. Investigación: tres subagentes el 12-oct (mercado de herramientas, opciones de Claude, ley y
reglamento de compras). Nada de esto está construido.

**El encargo (Sergio, 12-oct, en tres mensajes):** un espacio aislado, con agente y skills, que cada noche
seleccione licitaciones con una mirada más amplia que la del Radar, prepare las presentaciones y en la mañana diga
si nos presentamos o no, para que Sergio autorice. Que se abra a lo que no sabemos hacer si deja ingresos, y que no
se cierre a crear un negocio o una empresa nueva con otra gente que se dedique a esto. «Necesitamos circular
dinero.»

---

## 1. Decisiones cerradas que este diseño respeta

| Fecha | Decisión | Respaldo |
|---|---|---|
| 3-oct | Concentrar la cartera en pocas apuestas; una oferta mal calzada «deja huella ante el mismo comprador» | `marca/PLAN-COMPETITIVIDAD-2026-10-03.md` §3 Eje A |
| 7-oct | Norma: toda posibilidad de ingreso se evalúa; se descarta solo por un hecho, nunca por baja probabilidad; primer paso barato se hace ya | `marca/POSIBILIDADES-2026-10-07.md`; memoria `evaluar-todas-las-posibilidades` |
| 8-oct | El Radar se dispara desde cron-job.org (job 8607281) por `workflow_dispatch`; el `schedule` de GitHub queda de respaldo | `radar-licitaciones/continuidad.md`, sesión 8-oct |
| 30-sep | TL hábil en Mercado Público hasta el 01-12-2026; DJ del Registro firmada el 01-10 (N° 1004123) | `ESTADO.md` fila `utem-plataforma-difusion` |
| — | Push, deploy y envíos a terceros se confirman siempre; un deploy de producción por sesión | `~/.claude/CLAUDE.md` §4 |

Este diseño no reabre ninguna. La tensión entre la del 3-oct (concentrar) y la del 7-oct (evaluar todo) se resuelve
en el diseño: el agente **evalúa todo**, y lo que llega a Sergio pasa por un tope de ofertas abiertas (§5.4).

---

## 2. Lo que se atacó y qué sobrevivió

**Encontrar no es lo que nos frena.** Del 1 al 8-oct se leyeron a mano las bases de unas quince licitaciones y se
presentó una (Llanquihue). Las demás cayeron por experiencia acreditable (USACH 10+ proyectos en 24 meses; FONASA
45 % de experiencia en el sector público), títulos del equipo (AGCID, MMA 5500), registro ATE o entidad sin fines
de lucro (558869), compra de medios (584105) o un socio que no apareció (Lirmi, camélidos, Moodle). Un agente que
«prepara todo» cada noche habría armado quince carpetas para cero ofertas más.

**«Autorizo y listo» no existe en Mercado Público.** Ofertar exige Clave Única, la DJ y la carga y firma de los
archivos. Eso queda en manos de Sergio, y se diseña así a propósito (§5.5).

**El primer momento de decidir es el foro de consultas**, que cierra una semana o más antes de las ofertas.

**Sobrevive:** un agente que cada noche lee las bases completas de todo lo que podría calzar, dice temprano por qué
no (con la página), detecta con quién sí, y deja armado lo repetitivo cuando la respuesta es sí. Y sobrevive la
apertura a otros negocios, con la condición de que cada uno entre al correo solo cuando su hecho habilitante esté
verificado (§4).

**Lo que el agente no resuelve:** la experiencia acreditable. Los pedidos de `marca/experiencia/PEDIDOS.md` siguen
abiertos desde el 3-oct. El agente puede medir cuántos puntos se pierden por eso cada mes.

---

## 3. Hechos

### 3.1 Lo que se nos está pasando

- **Convenio Marco de desarrollo y mantención de software y servicios profesionales TI, ID 2239-2-LR26**: 100 a
  25.000 UTM, pymes en UTP, cerró el 9-oct, adjudicación prevista el 23-nov (chilecompra.cl, avisos de julio y
  agosto de 2026). **No está en `data/state.json`** (búsqueda con control positivo, 12-oct). Probable causa: la
  exclusión «mantención de» (`src/config.py:173`) o la falta de «software» entre las inclusiones; **no verificado**,
  falta leer el título exacto. Publicada el 14-jul; el cierre pasó del 25-sep al 9-oct (ChilecompraNews, 24-sep); la
  ficha no cargó con WebFetch, así que una prórroga posterior no está descartada. Tamaño de lo perdido: en el
  convenio anterior hubo 321 adjudicados y **solo 124 vendían** en la tienda, con USD 21,5 M transados entre dic-2022
  y may-2024 entre todos; el de 2024 (2239-19-LR23) adjudicó 446 proveedores, 75 % EMT, vigencia 30 meses
  (chilecompra.cl, 1-jul-2024). Estar adjudicado da un lugar en el catálogo, no ventas; la distribución por
  proveedor no se publica. Después del 23-nov, la lista de adjudicados es materia del carril 4.
- Universo del 8-jul (`data/audit-2026-07-08.csv`): 4.029 licitaciones; el filtro dejaba pasar 36 (0,9 %).
  Heurística por palabras del título, solo orden de magnitud: ~1.365 bienes, ~617 obras, ~350 servicios
  (capacitación/eventos 133, comunicación/software 113, consultoría/estudios 100), ~1.700 sin clasificar.
- Compra Ágil caída (504) desde mediados de agosto: ese canal hoy no se ve.

### 3.2 Ley y reglamento (Ley 19.886 y DS 661/2024; leídos en copia de ACHM, cotejar con BCN antes de citar)

| Hecho | Fuente |
|---|---|
| Compra Ágil hasta 100 UTM, mínimo 3 cotizaciones; la solicitud va por regla general a empresas de menor tamaño (EMT) y proveedores locales | Ley art. 7 n°1 y 56; DS 661 art. 97 |
| En Compra Ágil no se exige adjudicar al menor precio; si no se elige el más barato, se fundamenta en la OC | DS 661 art. 97 |
| Pago: 30 días corridos desde la factura (hasta 60 en licitación con motivo fundado) | DS 661 art. 133; Directiva N°23/2026 |
| Subcontratación: tope 30 % del contrato salvo que las bases fijen más; el subcontratista debe estar hábil | DS 661 art. 128; Ley art. 15 |
| UTP: sin crear sociedad; escritura pública desde 1.000 UTM; solidaridad; no se puede ofertar solo y en UTP a la vez | Ley arts. 51-52; DS 661 art. 48 |
| UTP debe incluir al menos una EMT o es inadmisible | DS 661 arts. 180-183 — **no verificado si aplica a toda UTP o solo al título de fomento a EMT** |
| Nota de comportamiento contractual por incumplimientos; puede ser criterio de evaluación; suspensión e inhabilidad | DS 661 arts. 55, 151, 160, 162; Ley art. 35 septies |
| Datos abiertos OCDS traen adjudicaciones y proveedores (licitación, trato directo, Convenio Marco); **excluyen Compra Ágil** | data.open-contracting.org/en/publication/144 |

**No verificado:** si la interfaz de Compra Ágil (beta) entrega precios unitarios; si la API v1 entrega los
adjuntos; si la experiencia del equipo contratado a honorarios cuenta como del oferente (lo dice cada base); si dos
empresas relacionadas pueden ofertar en el mismo proceso.

### 3.3 Lo que ya existe en el mercado

| Herramienta | Qué hace | Precio | Para nosotros |
|---|---|---|---|
| Licitalab (licitalab.cl) | Alertas, lectura de bases con IA citando el punto, puntaje estimado, Compra Ágil | 2,2 / 3,2 / 5 UF al mes + IVA; 14 días gratis | La comparación natural; no conoce nuestra experiencia ni los carriles de §4 |
| Stotles (Reino Unido) | Informes de presentarse o no con IA | Desde £75/mes; 3 informes gratis | Formato de referencia; no cubre Chile (no verificado) |
| Loopio, Responsive, Arphie, AutogenAI | Redacción de RFP sobre biblioteca propia | Miles de USD al año (fuentes de competidores) | No calzan |
| Banco Mundial | API pública de avisos de adquisiciones | Gratis | Se suma como fuente |
| Agentes de código abierto para Mercado Público | No encontrado (no prueba que no exista) | — | — |

### 3.4 Dónde puede correr Claude (code.claude.com/docs, leído el 12-oct)

| Vía | A favor | En contra |
|---|---|---|
| GitHub Actions con claude-code-action | Ya corre ahí el Radar; aislado; persistencia por commit; acepta clave de API o token de suscripción | Navegador instalable pero no probado contra Mercado Público desde los servidores de GitHub |
| `claude -p` en una máquina propia | Navegador sin restricciones de red; hooks y skills | Necesita equipo encendido; Windows sin sandbox salvo WSL2 |
| Rutinas en la nube (`/schedule`) | Sin servidor | Lista cerrada de dominios (el vigía MMA ya falló por red); navegador no verificado |
| Managed Agents (beta) | Alojado por Anthropic | Clave de API, tokens + USD 0,08 por hora de sesión; navegador no listado |

La documentación limita el token de suscripción a «uso ordinario e individual» y no dice si una corrida nocturna
desatendida cuenta como tal.

---

## 4. Carriles: qué busca el agente

Clasificar las ~4.000 licitaciones con un modelo cuesta casi lo mismo con un carril que con seis, así que el agente
los mira todos desde el principio. **Un carril entra al correo de la mañana solo cuando su hecho habilitante está
verificado**; mientras tanto el agente lo cuenta y lo guarda, sin molestar.

| # | Carril | Qué detecta | Hecho habilitante | Plazo hasta la plata |
|---|---|---|---|---|
| 1 | Lo que sabemos | Datos, plataformas, comunicación, IA, educación, REP | Ya habilitado | Meses (Llanquihue: cierre 13-oct, adjudicación ~30-oct, después contrato y pago) |
| 2 | Con socio o en UTP | Licitaciones donde TL calza en una parte y falta experiencia o un título | Reglas de subcontratación y equipo leídas en cada base | Meses |
| 3 | TL como la EMT que la grande necesita | UTP de consultoras grandes | Alcance de DS 661 arts. 180-183 | Meses |
| 4 | Venderle al que ganó | Adjudicaciones grandes en nuestros sectores; propuesta al adjudicatario por la parte de datos, plataforma o comunicación (tope 30 %) | Bajar las adjudicaciones de OCDS | Semanas a meses, según el adjudicatario |
| 5 | Convenios Marco | Llamados LR de ChileCompra | Vigilarlos como canal propio | Meses (el TI se adjudica el 23-nov) |
| 6 | Comercio en Compra Ágil | Bienes y servicios simples bajo 100 UTM | **Margen medido** con una semana de OC | Semanas (cotización en días, pago a 30 días de la factura) |

Fuera de compras públicas, con el mismo método y sin investigar todavía: fondos (los lleva `financiamiento`),
multilaterales (BID BEO, PNUD, Banco Mundial, UNGM) y portales de proveedores privados (mineras).

---

## 5. Una empresa nueva con otra gente

**La idea.** Una sociedad separada de Tercera Letra, con socios que operan (cotizan, compran, despachan, facturan) en
los carriles que TL no puede ejecutar, sobre todo el 6. TL pone el agente y la selección, y cobra por licencia, por
participación o por las dos. El agente se construye una vez y sirve a las dos empresas. Si funciona para dos, es un
producto que se puede ofrecer a otras pymes.

**Lo que se ataca:**

- **El margen no está medido.** En Compra Ágil compiten miles de pymes que conocen su rubro. La ventaja del agente es
  cobertura y rapidez, no precio. Sin margen, no hay empresa.
- **El socio operador es la parte difícil**, y el agente no lo crea. Tiene que poner capital de trabajo (se le paga
  al proveedor antes de que pague el Estado, 30 días después de la factura) y saber despachar.
- **Otra sociedad es otra contabilidad.** TL tiene hoy cuatro F29 sin declarar y un giro en cobranza en la TGR
  (`ESTADO.md` fila `facturacion`). Usar una de las SpA existentes ahorra la constitución, pero hereda su situación
  tributaria, que no se revisó.
- **Empresas relacionadas.** La nueva sociedad iría en la DJ como relacionada; si dos relacionadas pueden ofertar en
  el mismo proceso **no está verificado**.
- **Protege a TL.** Una entrega tardía de bienes alimenta la nota de comportamiento del RUT que la hizo. Separar el
  comercio en otra sociedad deja limpio el RUT con el que TL licita tecnología.

**Lo que sobrevive:** un vehículo aparte para el comercio, con un socio que opere, **después** de que la medición de
margen dé positiva. Primer paso barato: la medición (§7, F0) y una lista de posibles socios operadores que nombra
Sergio. No se constituye nada antes.

### 5.1 Candidatos que ya conocemos (leído en Gmail TL el 12-oct)

**Solución Integral SpA (solintegral.cl), Jorge Salinas M.** RUT 76.376.518-0. Giro según Kena (correo del 3-ago):
«Comercialización productos para la construcción y minería arriendo de equipos». Su sitio: desde 2014, herramientas
e instrumentos industriales para minería, energía, construcción pesada y logística; representante oficial de DYKEM
en Chile; inscrita en Unilink y Ariba (portales de compras de mineras y grandes empresas); despacho a todo Chile. No
nombra clientes públicos ni menciona Mercado Público. Pagó la factura N° 1 de TL (sitio de d-aloga) por instrucción
de Kena; la relación entre ellos no consta. Dirección distinta en el correo (Providencia 2370 of. 41) y en el sitio
(Santa María 2670 of. 102).
- Calce: es el perfil del socio operador del carril 6 (ya compra, almacena, despacha y factura bienes) y abre el
  canal de compras privadas mineras. TL le aporta el agente que vigila Mercado Público y Compra Ágil para sus líneas.
- **Le vende al Estado y vive de eso** (Sergio, 12-oct). Por verificar: con qué código de proveedor y en qué líneas
  (API `BuscarProveedor` con el ticket y sus OC); cuántas compras públicas hay en sus líneas (herramientas,
  seguridad, medición). Correo exploratorio en borrador el 12-oct.

**Dialoga Consultores (d-aloga), María Eugenia (Kena) Fernández.** RUT 78.484.769-1 (correo del 3-ago). Asuntos
públicos, gestión territorial, relacionamiento comunitario, consulta indígena; ex directora nacional del Sename y ex
coordinadora de las Mesas Ejecutivas CORFO-BID. Cliente de TL desde julio.
- Calce: UTP del carril 2 para licitaciones de participación, consulta indígena, planes comunales y relacionamiento,
  donde TL pone datos y plataforma (`ddls`) y Sergio su trayectoria en política indígena (MDS, Comisionado
  Presidencial). AGCID 1606-31 (participación en 9 comunas) fue un caso de este tipo.
- En contra: las dos firmas son nuevas, así que la experiencia de empresa es baja; sirve donde las bases puntúan el
  equipo. Hay una cuenta abierta: la ronda del 13-08 del sitio se trabajó sin encuadre comercial
  (`_propuestas-archivadas/daloga/DALOGA-CONTINUIDAD.md`); conviene cerrarla antes de proponer una sociedad.
- Riesgo propio: cercanía con la clienta (memoria `cercania-al-cliente-genera-puntos-ciegos`).

Son dos acuerdos distintos y se conversan por separado.

---

## 6. Arquitectura

### 6.1 Dónde vive

Repositorio privado nuevo, `licitaciones-agente`, en GitHub Actions. Sin acceso al Gmail, el Drive ni el `~/.claude`
de Sergio; sus claves (ticket de Mercado Público, clave de API de Anthropic con tope de gasto, Resend) viven solo en
los secretos del repo. Si Mercado Público bloquea la descarga de bases desde los servidores de GitHub, el paso del
navegador pasa a una máquina propia (notebook viejo o mini-PC con Linux y `claude -p`); no se compra nada antes de
comprobarlo.

### 6.2 La noche (cron-job.org dispara; ChileCompra pide consultas masivas entre 22:00 y 07:00)

1. **Escaneo** de todas las fuentes: Mercado Público, Compra Ágil, Convenios Marco, PNUD, Banco Mundial; OCDS una vez
   por semana para las adjudicaciones (carril 4).
2. **Clasificación** con un modelo barato sobre título y descripción de todo lo publicado, asignando carril.
3. **Lectura de bases** de las que pasan: navegador headless con el mismo POST por archivo que funciona en Chrome
   (memoria `mercado-publico-bajar-bases`), PyMuPDF y OCR para las escaneadas. Un subagente **lector** por
   licitación aísla el contexto de PDFs largos y devuelve una ficha corta.
4. **Contraste con el perfil de TL** (`perfil/`: experiencia acreditable desde `marca/experiencia/INDICE.md`,
   registros, títulos, socios conocidos). Puntaje estimado por criterio contra el mínimo de las bases.
5. **Evaluador adversarial**, otro subagente, que defiende el no.
6. **Carpeta por candidata:** ficha de decisión con el requisito fatal y su página, borrador de consultas al foro,
   lista de admisibilidad, anexos prellenados, programa de integridad reutilizado, esquema de propuesta técnica,
   precio de referencia de adjudicaciones anteriores, y con quién ir si es carril 2-4.

### 6.3 La mañana

Correo a las 07:30 (Resend, como el Radar) con cuatro categorías: **descartada** (requisito y página),
**consultar al foro** (con borrador y fecha límite), **presentar**, **solo con socio** (y con quién). La mayoría de
los días debería decir «hoy nada». Cada candidata es un issue en el repo; Sergio comenta desde el teléfono `/foro`,
`/presentar`, `/socio` o `/no`, y el comentario dispara la redacción completa esa noche, que llega como PR.

### 6.4 Tope de ofertas abiertas

El correo pesa cada candidata contra el calendario: ofertas en curso, cierres duros de `ESTADO.md` y horas estimadas.
Con el tope lleno, una candidata buena aparece como «buena, pero choca con X». Valor inicial propuesto: dos ofertas
en preparación a la vez (decide Sergio).

### 6.5 Lo que el agente no puede hacer, por diseño

No tiene Clave Única, credenciales de Mercado Público ni herramientas de envío de correo a terceros. No puede subir
una oferta, escribir en un foro ni contactar a un comprador o a un socio. Los hooks del repo bloquean cualquier
herramienta de envío y ponen tope de gasto por corrida (`--max-budget-usd`, `--max-turns`).

### 6.6 Skills y subagentes del repo

Skills: `perfil-tl`, `leer-bases` (lista de requisitos fatales aprendida de los casos de octubre), `decidir`
(presentarse o no, con puntaje por criterio), `consultas-foro`, `armar-oferta`. Subagentes: `lector`, `evaluador`
(adversarial), `redactor`.

---

## 7. Fases

**F0 — Prueba con casos conocidos** (después del 15-oct, 1-2 sesiones en este repo):
- Perfil de TL y casillero de las ~15 decisiones de octubre con su motivo (MMA 5500, USACH 867990, FUCOA 1108660,
  AGCID 1606-31, Valle Diguillín, Llanquihue, 2122-34, 585893-11, 558869-62, 1111089-21, 591-34, 1209-12,
  1177296-23, 584105-39).
- Lector de bases corriendo en GitHub Actions, sin Chrome.
- **Criterio de aceptación:** el agente llega a la misma decisión que Sergio y al mismo requisito fatal con su página
  en al menos 14 de 15. Si no, no hay autonomía.
- Mediciones: tamaño de cada carril sobre el universo de julio y una semana actual; margen en Compra Ágil con una
  semana de OC en lo más cercano a nosotros (computadores, licencias, impresión, merchandising); costo por noche.
- Licitalab, 14 días gratis, sobre los mismos casos.
- Por qué no llegó 2239-2-LR26.

**F1 — En sombra, dos semanas:** el agente corre cada noche y manda su correo; Sergio sigue con el Radar actual.
Se cuentan los falsos negativos (oportunidades que aparecieron por otra vía) y el costo real.

**F2 — Aprobación y paquete:** issues con comandos, carpeta completa, PR de redacción.

**F3 — Carriles nuevos y empresa nueva**, cada uno cuando su hecho esté verificado.

---

## 8. Decisiones propuestas

**D1. Dónde corre.**
- Elegido: GitHub Actions en un repo privado nuevo.
- Alternativa descartada: la PC de Sergio con `claude -p`, un mini-PC desde el principio, o rutinas en la nube.
- Por qué es mejor para el producto: siempre encendido, aislado del trabajo diario, registro completo en git, y el
  Radar ya corre ahí. El mini-PC queda de respaldo si Mercado Público bloquea a GitHub; las rutinas no tienen
  navegador verificado y ya fallaron por red.
- Costo para nosotros (no es criterio): minutos de Actions, por medir en F0; no se compra equipo.

**D2. Cómo se paga Claude.**
- Elegido: clave de API con tope de gasto.
- Alternativa descartada: token de la suscripción Max.
- Por qué es mejor para el producto: términos claros para corridas desatendidas, tope duro, y no le quita cupo al
  trabajo diario de Sergio.
- Costo para nosotros (no es criterio): por uso, sin medir; se mide en F0 antes de dejarlo correr cada noche.

**D3. Cómo aprueba Sergio.**
- Elegido: issues de GitHub con comandos.
- Alternativa descartada: responder el correo o WhatsApp.
- Por qué es mejor para el producto: deja registro de cada decisión con su motivo, se responde desde el teléfono y
  dispara la siguiente etapa sin servidor propio.
- Costo para nosotros (no es criterio): ninguno.

**D4. El agente no sube ofertas.**
- Elegido: sin Clave Única ni credenciales de Mercado Público.
- Alternativa descartada: que cargue la oferta en el portal.
- Por qué es mejor para el producto: la DJ y la firma son de Sergio, y un error del agente no puede convertirse en una
  oferta presentada.
- Costo para nosotros (no es criterio): el rato de Sergio para revisar, firmar y subir cada oferta (no medido).

**D5. Licitalab como vara.**
- Elegido: probarlo 14 días sobre los mismos casos de F0.
- Alternativa descartada: construir sin comparar, o contratar Licitalab y no construir.
- Por qué es mejor para el producto: si su lectura de bases le gana a la nuestra, se cambia el plan; no cubre la
  experiencia de TL ni los carriles 2-6.
- Costo para nosotros (no es criterio): gratis la prueba; 2,2 UF/mes + IVA si se mantiene.

---

## 9. Lo que decide Sergio

1. D2: clave de API con tope (recomendado) o token de suscripción.
2. D5: prueba de Licitalab en paralelo (recomendado).
3. Tope de ofertas abiertas (propuesta: dos).
4. Nombres de posibles socios operadores para el carril 6, para tenerlos cuando la medición de margen termine.
5. Arranque de F0 después del 15-oct (recomendado, para no restarle horas a Bienes Públicos).

## 10. Cómo se llegó a esto: la conversación del 12-oct, en orden

Para retomar sin empezar de cero. Las citas de Sergio son textuales del chat (con su ortografía de tecleo rápido).

**1. El pedido.** «quiero hacer un entorno, un agente, skills etc. para licitaciones de fomra que todas las noches
serleccióne licitaciones, con una visión más amplia que solo la que tenía hasta ahora, y prepare todo para las
presentaciones yh que en la mañana solo me diga si nos presentamos o no y yo autorice... quiero que sea una gente con
autonomnía [...] quiero un espacio agentico aislado para esto.. puede incluo correr en otra computadora.. pensemos..
no hay apuro».

**2. Primera respuesta (adversarial, antes de diseñar).** Se leyó ESTADO.md entero, el índice, la continuidad del
Radar, el plan del 3-oct y `marca/experiencia/`. Tres subagentes: mercado de herramientas, opciones de Claude, y
después ley y reglamento. Lo que se le dijo a Sergio, y que sigue en pie:
- El cuello de botella no es encontrar: de ~15 bases leídas a mano del 1 al 8-oct se presentó 1 (Llanquihue); las
  demás murieron por experiencia acreditable, títulos, registro ATE o «sin fines de lucro», compra de medios, o un
  socio que no apareció. Un agente que «prepara todo» habría hecho 15 carpetas para 0 ofertas más.
- Choca con la decisión del 3-oct de concentrar; se resuelve con un tope de ofertas abiertas (§6.4).
- «Autorizo y listo» no existe: Clave Única, DJ y firma son de Sergio. El agente no tendrá credenciales (D4), a
  propósito: un error del agente no puede volverse una oferta.
- El primer momento de decidir es el foro de consultas, no el cierre.
- Lo que sobrevive: leer todas las bases de noche y decir temprano por qué no (con página), con quién sí, y dejar
  armado lo repetitivo.
- La prueba antes de construir: las ~15 decisiones de octubre ya tienen veredicto y motivo; el agente tiene que
  reproducirlas (14/15). Sin eso no hay autonomía.
- Lo que el agente no arregla: la experiencia acreditable (`marca/experiencia/PEDIDOS.md`, abierto desde el 3-oct).
- Falso negativo de un subagente corregido en el acto: dijo «PNUD: no encontrado», y el Radar ya lee el RSS del
  PNUD (`src/sources/undp.py`).

**3. Segunda vuelta: «que se abra a más cosas».** Sergio: «pero está contemplado que se abra a más cosas... que
permitan ganar dinero... no solo hacer lo que sabemos si no cosas que no sabemos pero que nos permitan tener
ingresos...??? eso quiero que lo pienses hatens de tomar una decision». Se investigó la ley (subagente) y se midió el
universo de julio. Conclusiones (detalle en §3.2 y §4):
- «Lo que no sabemos» se parte en negocios distintos con hechos distintos. En licitaciones normales no saber cuesta
  puntos por la misma razón por la que hoy perdemos. Donde no saber no cuesta: Compra Ágil (no puntúa experiencia;
  va por defecto a EMT y locales), UTP donde las bases puntúan al equipo, y venderle al que ganó.
- **La subcontratación tiene tope de 30 %** (DS 661 art. 128): TL no puede ganar algo que no sabe hacer y
  pasárselo entero a otro. Por eso el carril 2 es UTP o equipo contratado, no subcontrato total.
- **TL es una EMT**, y si DS 661 arts. 180-183 aplican a toda UTP (no verificado), las consultoras grandes
  necesitan una EMT para ir en UTP: carril 3.
- **Hallazgo duro:** el Convenio Marco TI 2239-2-LR26 cerró el 9-oct sin pasar por el Radar (§3.1).
- La objeción que queda registrada (también en la memoria `evaluar-todas-las-posibilidades`): el recurso escaso es
  el tiempo de Sergio. Evaluar lo hace el agente casi gratis; ejecutar no. Por eso cada carril entra al correo solo
  con su hecho habilitante verificado.

**4. Tercera vuelta: la empresa nueva.** Sergio: «eso y no te cierres a gbenerar un nuevo negocio o nueva empresa
mia con otra gente que se dedique a esto.... quiero que entiendeas que necesitamos circular dinero para sobrevivir tu
y yo». Se respondió con §5: la empresa aparte para el comercio sobrevive **después** de medir margen; se nombraron
los cuatro ataques (margen no medido, socio operador con capital, otra contabilidad con 4 F29 de TL pendientes,
empresas relacionadas no verificado) y la ventaja (protege el RUT de TL de la nota de comportamiento). Para «circular
dinero» rápido, el carril 6 es el de plazo más corto (días a cotizar, pago a 30 días de la factura); las licitaciones
tardan meses.

**5. «¿perdimos mucho con ese convenio marco?»** Respuesta (§3.1): perdimos un lugar en un catálogo por ~30 meses,
no un ingreso seguro. Convenio anterior: 321 adjudicados, 124 vendiendo, USD 21,5 M entre todos en ~18 meses. Lo que
sí se pierde es el canal de contratación directa de 100 a 25.000 UTM sin licitación, útil para productos como
dotación o patentes-ia. El siguiente, si se repite el ciclo de 30 meses, hacia 2029 (no verificado; reaperturas no
verificadas). Se rescata con la lista de adjudicados del 23-nov (carril 4).

**6. Socios con nombre.** Sergio: «revisa soluciones integrales o algo asi y d-aologa y jorge salinas para ver si
podemos hacer acuerdos con ellos». Se leyó Gmail TL (con enviados) y los repos. Resultado en §5.1. Sutilezas:
- Grep dio 0 para «Solución Integral» aunque `marca/experiencia/INDICE.md` lo nombra: falso negativo por
  `.gitignore` (memoria `grep-respeta-gitignore-falso-negativo`). Se repitió con `rg --no-ignore` y control.
- Hay otro «Salinas» en el portafolio: el gerente de Operaciones de CAS-Chile (fila `financiamiento`). No es la
  misma persona hasta que una fuente lo diga; Jorge Salinas M. es el de jsalinas@solintegral.cl.
- La relación entre Kena y Jorge no consta: solo que Solución Integral pagó la factura de d-aloga por instrucción de
  ella.
- Sergio después: «jorge vende al estado.. de eso vive..». Es palabra de Sergio; el sitio de Solintegral no
  menciona Mercado Público. Comprobar con la API antes de la reunión.

**7. «entonces cual es el plan general?»** Se dio el calendario de fases de §7 con fechas: esta semana correos y
decisiones; 19-25 oct prueba con casos conocidos; 26-oct a 8-nov en sombra; noviembre en serio (23-nov lista de
adjudicados del Convenio Marco); diciembre carriles nuevos. En paralelo: **01-12 vence la habilidad de TL en
Mercado Público** (renovar) y rige la Ley 21.719.

**8. Correos.** Sergio: «hazlo». Borradores en Gmail TL, cada uno en su hilo (memoria
`correo-para-sergio-va-como-borrador-gmail`), tras el hook `guard-correo-verificado`:
- Jorge (hilo «Factura D-aloga», respuesta al mensaje 19fd2ca48e75f46f): el verificador dio **FALLA** a la primera
  versión porque decía que el sistema «va a revisar» Compra Ágil, que está caída y solo existe en diseño; quedó
  «estamos diseñando». Propone media hora; nosotros búsqueda y lectura de bases, ellos cotizan, despachan y
  facturan; el reparto se conversa (sin montos).
- Kena (hilo «d-aloga.cl — cambios aplicados…», respuesta a 1a035a5e84fc9316, cc a su Gmail): se sacaron dos
  afirmaciones sin respaldo («aparecen seguido» y «ninguna puede sola») y «la parte indígena» pasó a «yo con mi
  experiencia en política indígena» para no pisar la consulta indígena que ofrece d-aloga. **Ese hilo arrastra la
  ronda del 13-08 del sitio trabajada sin encuadre comercial**: Sergio decide si la cierra antes de enviar.
- Verificaciones en `~/.claude/verificaciones-correo/cc4938a49210cd07*` (Jorge) y `c1f230e96305c92e*` (Kena). Las
  tablas tuvieron que reescribirse una vez porque el hook exige el formato «| fuente: … | conversado: si — …» en
  cada línea.

**9. Foro de la 2122-34.** Ver `postulaciones/seremi-salud-2122-34-ia-cancer/continuidad.md`, entrada del 12-oct:
las seis consultas quedaron **duplicadas** (ya estaban subidas el 8-oct 21:50, sin registro) y el foro deja leer la
competencia (6-9 interesados estimados). Gotcha: en la ficha pública el botón de preguntas aparece deshabilitado
(icono «bloq»), pero su `href` abre la vista pública con todas las preguntas mientras el foro está abierto; el HTML
llega vacío por `fetch` y se llena al navegar la pestaña.

## 11. Para retomar

Primer paso de la próxima sesión, en este orden:
1. Preguntar a Sergio si envió los borradores a Jorge y Kena, y qué respondieron; con la respuesta de Jorge,
   comprobar su código de proveedor y sus OC con la API (`BuscarProveedor`, con el ticket del Radar en Actions).
2. Las cinco decisiones de §9.
3. Después del 15-oct: F0 (§7). Arranca con el perfil de TL y el casillero de los 15 casos, leyendo cada carpeta de
   `postulaciones/` y las continuidades de los SLEP; no se reconstruyen los motivos de memoria.

## 12. No verificado

Adjuntos en la API v1; campos de la API de Compra Ágil (beta); precio unitario en OCDS; alcance de DS 661 arts.
180-183; si cuenta como del oferente la experiencia del equipo contratado; ofertas de empresas relacionadas en un
mismo proceso; descarga de bases con navegador headless desde GitHub; si el token de suscripción cubre corridas
desatendidas; causa exacta de que 2239-2-LR26 no llegara; texto del DS 661 contra BCN.
