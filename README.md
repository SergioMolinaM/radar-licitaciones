# Radar de Licitaciones — Tercera Letra SpA

Monitoreo diario automatizado de oportunidades institucionales en:

- **Mercado Público (ChileCompra)** — API oficial. Única fuente para Chile.
- **PNUD Procurement Notices** — RSS feeds por país (Bolivia, Perú, Colombia, Argentina, Ecuador, México) más feed global con filtro geográfico. **Chile no tiene feed PNUD propio**; las oportunidades chilenas vienen exclusivamente vía Mercado Público.

Filtrado por keywords alineadas al perfil de Tercera Letra (comunicación estratégica, estudios cualitativos, evaluación de políticas, economía circular, educación). Deduplicación persistente. Notificación por correo vía Resend.

Corre en GitHub Actions, lunes a viernes 09:00 hora Chile (invierno), costo cero.

---

## Arquitectura

```
radar-licitaciones/
├── .github/workflows/scanner.yml   # Cron diario
├── src/
│   ├── config.py                   # Keywords, feeds, endpoints
│   ├── filters.py                  # Match por keywords inclusión/exclusión
│   ├── state.py                    # Persistencia de IDs ya notificados
│   ├── notifier.py                 # Envío correo vía Resend
│   ├── scanner.py                  # Orquestador
│   └── sources/
│       ├── mercado_publico.py      # API ChileCompra
│       └── undp.py                 # RSS PNUD
├── data/state.json                 # IDs vistos (commiteado automáticamente)
├── requirements.txt
└── .env.example
```

---

## Setup local (PowerShell)

```powershell
# 1. Clonar y entrar
git clone https://github.com/<tu-usuario>/radar-licitaciones.git
cd radar-licitaciones

# 2. Entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Configurar variables locales
Copy-Item .env.example .env
# Editar .env con tus credenciales

# 4. Probar
$env:MERCADO_PUBLICO_TOKEN = "tu-ticket"
$env:RESEND_API_KEY        = "re_xxx"
$env:RADAR_TO_EMAIL        = "sergio@terceraletra.cl"
$env:RADAR_FROM_EMAIL      = "radar@terceraletra.cl"
python -m src.scanner
```

---

## Setup GitHub Actions

1. Crear repo privado en GitHub y subir el proyecto.
2. Settings → Secrets and variables → Actions → New repository secret. Crear:
   - `MERCADO_PUBLICO_TOKEN` — solicitar en https://api.mercadopublico.cl
   - `RESEND_API_KEY` — obtener en https://resend.com (tier free: 3.000 correos/mes)
   - `RADAR_TO_EMAIL` — destinatario (ej: sergio@terceraletra.cl)
   - `RADAR_FROM_EMAIL` — remitente (debe ser dominio verificado en Resend)
3. Settings → Actions → General → Workflow permissions → **Read and write**.
4. Probar manualmente: Actions → Radar Licitaciones → Run workflow.

---

## Personalización

**Keywords** — editar `src/config.py`:

- `KEYWORDS_INCLUDE` — añadir términos relevantes (case-insensitive, match por substring).
- `KEYWORDS_EXCLUDE` — descarta licitaciones que contengan estos términos. Útil para evitar ruido recurrente.

**Países PNUD** — `UNDP_FEEDS` en `config.py`. Importante: PNUD usa códigos propietarios, **no ISO3 estándar** (ej: BHU no BTN para Bután). La lista canónica está en https://procurement-notices.undp.org/proc_notices_rss_feed.cfm. Países sin oficina PNUD activa (Chile, Uruguay, Paraguay) no tienen feed.

**Frecuencia** — editar el `cron` en `.github/workflows/scanner.yml`. Sintaxis: UTC. Ejemplos:

- `'0 12 * * 1-5'` — lunes a viernes 12:00 UTC (09:00 Chile invierno).
- `'0 12,20 * * *'` — diario 09:00 y 17:00 Chile invierno.

---

## Cómo extender

**Agregar fuente nueva** (ejemplo: BID, Banco Mundial, ChileCompra Empresas Públicas):

1. Crear `src/sources/<fuente>.py` con función que retorna `list[dict]` siguiendo el esquema:

   ```python
   {
       "fuente": str,           # nombre humano
       "id": str,               # ID único estable con prefijo (ej: "BID::12345")
       "codigo": str,           # código original sin prefijo
       "titulo": str,
       "estado": str,
       "fecha_cierre": str,
       "link": str,
       "keywords_match": list[str],
   }
   ```

2. Importar en `scanner.py` y agregar a `todos.extend(...)`.

El sistema de deduplicación y notificación funciona automáticamente.

---

## Notas operativas

- El primer run notificará todas las licitaciones matching del día (puede ser ruidoso). Después solo notifica nuevas.
- El `state.json` se commitea automáticamente con cada ejecución exitosa. Si la notificación falla, no se actualiza el state (reintenta al día siguiente).
- IDs en `state.json` se purgan automáticamente tras 90 días.
- Si el ticket de Mercado Público expira o el endpoint cambia, la API de PNUD sigue funcionando (degradación elegante).

---

## Roadmap sugerido

- Fase 2: BID Consulting Opportunities (scraping del portal IDB).
- Fase 2: Banco Mundial eConsultant2 (requiere login, evaluar costo/beneficio).
- Fase 3: Resumen semanal con análisis de tendencias.
- Fase 3: Clasificación por línea de negocio (Tercera Letra core / RADAR / Camino a la U).
