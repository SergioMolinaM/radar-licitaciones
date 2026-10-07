# Continuidad — Radar de Licitaciones

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
