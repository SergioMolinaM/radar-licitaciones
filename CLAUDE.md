# Radar de Licitaciones

GitHub Action que cada mañana (cron-job.org → `workflow_dispatch`, 09:00 Chile L-V) escanea Mercado Público,
Compra Ágil y PNUD y manda el correo del Radar. Sin hosting ni deploy: el cierre termina en push.

## Triage y postulación

Leer el correo del Radar, revisar fichas y bases o armar una oferta se hace con la skill
**`tercera-letra-licitaciones`**. Resumen (pedido de Sergio, 15-oct-2026): el objetivo es presentarse y ganar;
se abre todo servicio vigente y se leen los adjuntos sin preguntar; un «no» solo vale con el requisito textual,
su página y sin forma de cubrirlo; decide Sergio. Los papeles y piezas repetidas de toda oferta están en
`../postulaciones/_kit/KIT.md`.

**Este repo es público (31-oct-2026).** Las notas de negocio viven en `privado/`, un repo privado anidado
(`radar-licitaciones-privado`) que este repo ignora: `privado/continuidad.md` (ofertas, decisiones, personas),
`privado/triage/`, `privado/docs/`, `privado/soporte/`. En `continuidad.md` de este repo va **solo** lo técnico
(código, workflows, cuotas, errores), sin ofertas, precios, clientes ni nombres de personas.

Los triages del día van en `privado/triage/AAAA-MM-DD-<fuente>.md` con el formato fijo de la skill §4 (lo vigila
`guard-formato-triage.py`; formato y criterio no se cambian por sesión); las bases bajadas en
`privado/triage/bases-AAAA-MM-DD/<código>/` (fuera de git también en el repo privado: son documentos de terceros).

## Verificación

No hay tests ni token local, y un push no dispara el workflow: ver la memoria `verificacion-sin-red-ni-correo`.
