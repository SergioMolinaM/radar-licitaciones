"""Notificación por correo vía Resend API.

Resend tier gratuito: 3.000 correos/mes, 100/día. Sobra para uso diario.
Si no hay RESEND_API_KEY configurada, solo loggea el resumen.
"""

import os
import logging
from datetime import datetime
import requests

logger = logging.getLogger(__name__)

RESEND_URL = "https://api.resend.com/emails"
TIMEOUT = 15


def render_html(items: list[dict]) -> str:
    """Construye el cuerpo HTML del correo, agrupado por fuente."""
    fecha = datetime.now().strftime("%d/%m/%Y")
    por_fuente: dict[str, list[dict]] = {}
    for it in items:
        por_fuente.setdefault(it["fuente"], []).append(it)

    bloques_html = []
    for fuente, lista in sorted(por_fuente.items()):
        filas = []
        for it in lista:
            kws = ", ".join(it.get("keywords_match", []))
            filas.append(f"""
                <tr>
                    <td style="padding:12px 8px;border-bottom:1px solid #eee;vertical-align:top;">
                        <a href="{it['link']}" style="color:#0a4d8c;text-decoration:none;font-weight:600;">{it['titulo']}</a>
                        <div style="color:#666;font-size:12px;margin-top:4px;">
                            <code>{it['codigo']}</code> · Estado: {it['estado']}
                            {f" · Cierre: {it['fecha_cierre']}" if it.get('fecha_cierre') else ""}
                        </div>
                        <div style="color:#999;font-size:11px;margin-top:4px;font-style:italic;">
                            Match: {kws}
                        </div>
                    </td>
                </tr>
            """)
        bloques_html.append(f"""
            <h2 style="color:#0a4d8c;font-size:16px;margin:24px 0 8px;border-bottom:2px solid #0a4d8c;padding-bottom:4px;">
                {fuente} <span style="color:#999;font-weight:400;font-size:13px;">({len(lista)})</span>
            </h2>
            <table style="width:100%;border-collapse:collapse;">
                {''.join(filas)}
            </table>
        """)

    return f"""
    <html><body style="font-family:-apple-system,Segoe UI,sans-serif;max-width:680px;margin:0 auto;padding:24px;color:#222;">
        <h1 style="font-size:20px;margin:0 0 4px;">Radar de Licitaciones</h1>
        <p style="color:#666;margin:0 0 16px;font-size:13px;">
            {fecha} · {len(items)} nueva{'s' if len(items) != 1 else ''} oportunidad{'es' if len(items) != 1 else ''}
        </p>
        {''.join(bloques_html)}
        <hr style="border:none;border-top:1px solid #eee;margin:32px 0 12px;">
        <p style="color:#999;font-size:11px;">
            Sistema de monitoreo institucional · Tercera Letra SpA
        </p>
    </body></html>
    """


def send_email(items: list[dict]) -> bool:
    """Envía resumen. Retorna True si se envió o no había qué enviar."""
    if not items:
        logger.info("Sin nuevas oportunidades — no se envía correo")
        return True

    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        logger.warning("RESEND_API_KEY no configurado — solo log local")
        for it in items:
            logger.info(f"[{it['fuente']}] {it['titulo']} — {it['link']}")
        return True

    destinatario = os.getenv("RADAR_TO_EMAIL")
    remitente = os.getenv("RADAR_FROM_EMAIL", "radar@terceraletra.cl")
    if not destinatario:
        logger.error("RADAR_TO_EMAIL no configurado")
        return False

    payload = {
        "from": remitente,
        "to": [destinatario],
        "subject": f"Radar Licitaciones — {len(items)} nuevas oportunidades ({datetime.now().strftime('%d/%m')})",
        "html": render_html(items),
    }

    try:
        resp = requests.post(
            RESEND_URL,
            json=payload,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        logger.info(f"Correo enviado a {destinatario} con {len(items)} ítems")
        return True
    except requests.RequestException as e:
        logger.error(f"Error enviando correo: {e}")
        return False
