# Radar de Licitaciones

GitHub Action que cada mañana (cron-job.org → `workflow_dispatch`, 09:00 Chile L-V) escanea Mercado Público,
Compra Ágil y PNUD y manda el correo del Radar. Sin hosting ni deploy: el cierre termina en push.

## Triage y postulación

Leer el correo del Radar, revisar fichas y bases o armar una oferta se hace con la skill
**`tercera-letra-licitaciones`**. Resumen (pedido de Sergio, 15-oct-2026): el objetivo es presentarse y ganar;
se abre todo servicio vigente y se leen los adjuntos sin preguntar; un «no» solo vale con el requisito textual,
su página y sin forma de cubrirlo; decide Sergio. Los papeles y piezas repetidas de toda oferta están en
`../postulaciones/_kit/KIT.md`.

Los triages del día van en `triage/AAAA-MM-DD-*.md`; las bases bajadas en `triage/bases-AAAA-MM-DD/<código>/`
(fuera de git: son documentos de terceros).

## Verificación

No hay tests ni token local, y un push no dispara el workflow: ver la memoria `verificacion-sin-red-ni-correo`.
