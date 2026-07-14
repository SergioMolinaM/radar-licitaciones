# Continuidad — Radar de Licitaciones

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
