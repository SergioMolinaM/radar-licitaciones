# Continuidad — Radar de Licitaciones (código, repo público)

**Este repo es público.** Aquí va solo el estado técnico del radar: código, workflows, fuentes de datos, cuotas y
errores. **Nada de ofertas, precios, decisiones comerciales, clientes ni nombres de personas.** Todo eso va en
`privado/continuidad.md` (repo privado anidado `radar-licitaciones-privado`, ignorado por este repo), junto con
los triages (`privado/triage/`), el diseño del agente (`privado/docs/`) y los reclamos (`privado/soporte/`).

La historia completa hasta el 31-oct-2026 está en `privado/continuidad.md`. Entradas de la más nueva a la más vieja.

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
`main`. `privado/` ignorado por `.gitignore`.
