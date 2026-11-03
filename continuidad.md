# Continuidad — Radar de Licitaciones (código, repo público)

**Este repo es público.** Aquí va solo el estado técnico del radar: código, workflows, fuentes de datos, cuotas y
errores. **Nada de ofertas, precios, decisiones comerciales, clientes ni nombres de personas.** Todo eso va en
`privado/continuidad.md` (repo privado anidado `radar-licitaciones-privado`, ignorado por este repo), junto con
los triages (`privado/triage/`), el diseño del agente (`privado/docs/`) y los reclamos (`privado/soporte/`).

La historia completa hasta el 31-oct-2026 está en `privado/continuidad.md`. Entradas de la más nueva a la más vieja.

## 2026-11-02 (tarde) — 504 de q: pausa de rotativos y sonda de ventana

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
- Clasificador medido con Haiku, Sonnet y Opus 5.5 sobre el set de prueba, y parte 2 del diseño de selección
  escrita: detalle en el repo privado (`privado/docs/SELECCION-RADAR-2026-11-02.md` §4-8). SDK `anthropic` 2.4.0
  instalado en el PC para la medición.
- Siguen del 02-11: tope o resumen del correo y rediseño de la
  selección (clasificador).

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
