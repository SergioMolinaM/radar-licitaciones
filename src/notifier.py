"""Notificación por correo vía Resend API.

Resend tier gratuito: 3.000 correos/mes, 100/día. Sobra para uso diario.
Si no hay RESEND_API_KEY configurada, solo loggea el resumen.
"""

import os
import logging
from datetime import datetime
from html import escape
import requests

from .config import FUENTE_PALABRA_SUELTA

logger = logging.getLogger(__name__)

RESEND_URL = "https://api.resend.com/emails"
TIMEOUT = 15


def _render_aviso_caidas(caidas, parciales=()) -> str:
    html = ""
    if caidas:
        html += f"""
        <div style="background:#fdecea;border-left:4px solid #c62828;padding:10px 12px;margin:0 0 16px;font-size:13px;color:#7f1d1d;">
            <strong>Fuente caída:</strong> {', '.join(caidas)}. Esta corrida no revisó esa fuente;
            lo que haya publicado ahí no aparece en este correo.
        </div>
    """
    if parciales:
        html += f"""
        <div style="background:#fff8e1;border-left:4px solid #f9a825;padding:10px 12px;margin:0 0 16px;font-size:13px;color:#5d4037;">
            <strong>Revisión parcial:</strong> {'; '.join(parciales)}.
        </div>
    """
    return html


def render_html(items: list[dict], caidas=(), parciales=()) -> str:
    """Construye el cuerpo HTML del correo, agrupado por fuente."""
    fecha = datetime.now().strftime("%d/%m/%Y")
    por_fuente: dict[str, list[dict]] = {}
    for it in items:
        por_fuente.setdefault(it["fuente"], []).append(it)

    # Lo que la búsqueda de Compra Ágil trajo por una palabra suelta va al
    # final: trae ruido, pero también candidatas reales (15-oct: 10 de 19).
    def _orden(par):
        fuente = par[0]
        return (fuente == FUENTE_PALABRA_SUELTA, fuente)

    bloques_html = []
    for fuente, lista in sorted(por_fuente.items(), key=_orden):
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
        {_render_aviso_caidas(caidas, parciales)}
        {''.join(bloques_html)}
        <hr style="border:none;border-top:1px solid #eee;margin:32px 0 12px;">
        <p style="color:#999;font-size:11px;">
            Sistema de monitoreo institucional · Tercera Letra SpA
        </p>
    </body></html>
    """


def send_email(items: list[dict], caidas=(), parciales=()) -> bool:
    """Envía resumen. Retorna True si se envió o no había qué enviar.

    Sin ítems nuevos no se envía, aunque haya fuentes caídas: ese caso lo
    avisa GitHub Actions, porque el scanner sale con error.
    """
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
        "html": render_html(items, caidas, parciales),
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


def _render_aviso_cna_html(avisos: list[dict], nota: str = "") -> str:
    filas = "".join(f"""
        <li style="margin:0 0 10px;">
            <a href="{escape(a['link'])}" style="color:#0a4d8c;font-weight:600;text-decoration:none;">{escape(a['titulo'])}</a>
            <span style="color:#666;font-size:12px;"> · publicada el {escape(a['fecha'])}</span>
        </li>""" for a in avisos)
    aviso_nota = (f'<p style="background:#fff8e1;border-left:4px solid #f9a825;padding:10px 12px;font-size:13px;color:#5d4037;">'
                  f"{escape(nota)}</p>") if nota else ""
    return f"""
    <html><body style="font-family:-apple-system,Segoe UI,sans-serif;max-width:600px;margin:0 auto;padding:24px;color:#222;">
        <h1 style="font-size:18px;margin:0 0 12px;">La CNA publicó un llamado a pares evaluadores</h1>
        {aviso_nota}
        <ul style="padding-left:18px;">{filas}</ul>
        <p style="color:#666;font-size:13px;line-height:1.5;">
            Revisar en la noticia las bases, los requisitos y el plazo de postulación.
        </p>
        <hr style="border:none;border-top:1px solid #eee;margin:20px 0 12px;">
        <p style="color:#999;font-size:11px;">Aviso automático del Radar de Tercera Letra SpA</p>
    </body></html>
    """


def _enviar_aviso_cna(para: list[str], avisos: list[dict], nota: str = "") -> bool:
    clave = os.getenv("RESEND_API_KEY")
    if not clave:
        logger.warning("Aviso CNA no enviado - falta RESEND_API_KEY")
        for a in avisos:
            logger.info(f"[CNA] {a['titulo']} — {a['link']}")
        return False
    payload = {
        "from": os.getenv("RADAR_FROM_EMAIL", "radar@terceraletra.cl"),
        "to": para,
        "subject": "CNA: llamado a pares evaluadores",
        "html": _render_aviso_cna_html(avisos, nota),
    }
    # El repo es público y sus logs también: se loguea la cantidad, no las direcciones.
    try:
        resp = requests.post(RESEND_URL, json=payload,
                             headers={"Authorization": f"Bearer {clave}"}, timeout=TIMEOUT)
        resp.raise_for_status()
        logger.info(f"Aviso CNA enviado ({len(para)} destinatario(s))")
        return True
    except requests.RequestException as e:
        codigo = getattr(e.response, "status_code", None)
        logger.error(f"Error enviando aviso CNA ({len(para)} destinatario(s)): HTTP {codigo or type(e).__name__}")
        return False


def destinatarios_cna_extra() -> list[str]:
    return [d.strip() for d in os.getenv("RADAR_CNA_TO", "").split(",") if d.strip()]


def send_aviso_cna_extra(avisos: list[dict]) -> bool:
    """Aviso a RADAR_CNA_TO (David), aparte del principal. Con el remitente de prueba
    onboarding@resend.dev, Resend solo entrega a la cuenta dueña y rechaza (403) a
    cualquier otro: hace falta un dominio verificado en RADAR_FROM_EMAIL."""
    return _enviar_aviso_cna(destinatarios_cna_extra(), avisos)


def send_aviso_cna(avisos: list[dict], fallo_extra: bool = False) -> bool:
    """Aviso a RADAR_TO_EMAIL. Si el envío a RADAR_CNA_TO falló, lo dice en el correo."""
    destinatario = os.getenv("RADAR_TO_EMAIL")
    if not destinatario:
        logger.error("Aviso CNA no enviado - falta RADAR_TO_EMAIL")
        return False
    nota = ("No se pudo enviar este aviso a los destinatarios de RADAR_CNA_TO (ver el log de la corrida; "
            "con el remitente onboarding@resend.dev, Resend solo entrega a la cuenta dueña). Reenviarlo a mano: "
            "el Radar reintenta mientras la noticia tenga menos de 14 días.") if fallo_extra else ""
    return _enviar_aviso_cna([destinatario], avisos, nota)


def _render_heartbeat_html(stats: dict) -> str:
    """Cuerpo del heartbeat semanal - corto, sin ruido visual."""
    fecha = datetime.now().strftime("%d/%m/%Y")
    return f"""
    <html><body style="font-family:-apple-system,Segoe UI,sans-serif;max-width:520px;margin:0 auto;padding:24px;color:#222;">
        <h1 style="font-size:18px;margin:0 0 4px;">Radar de Licitaciones - Reporte semanal</h1>
        <p style="color:#666;margin:0 0 20px;font-size:13px;">
            Viernes {fecha} - confirmacion de que el sistema esta corriendo
        </p>
        {_render_aviso_caidas(stats.get('caidas'), stats.get('parciales'))}
        <table style="width:100%;border-collapse:collapse;font-size:14px;">
            <tr><td style="padding:8px 0;color:#666;">Licitaciones activas en Mercado Publico</td>
                <td style="padding:8px 0;text-align:right;font-weight:600;">{stats['universo_mp']:,}</td></tr>
            <tr><td style="padding:8px 0;color:#666;">Compras Agiles devueltas por la busqueda ({stats.get('ca_terminos', '')})</td>
                <td style="padding:8px 0;text-align:right;font-weight:600;">{stats.get('universo_ca', 0):,}</td></tr>
            <tr><td style="padding:8px 0;color:#666;">Entradas escaneadas en PNUD</td>
                <td style="padding:8px 0;text-align:right;font-weight:600;">{stats['universo_undp']:,}</td></tr>
            <tr><td style="padding:8px 0;color:#666;border-top:1px solid #eee;">Matches con keywords hoy</td>
                <td style="padding:8px 0;text-align:right;font-weight:600;border-top:1px solid #eee;">{stats['matches_totales_hoy']}</td></tr>
            <tr><td style="padding:8px 0;color:#666;">Nuevas oportunidades notificadas esta semana</td>
                <td style="padding:8px 0;text-align:right;font-weight:600;color:#0a4d8c;">{stats['nuevos_semana']}</td></tr>
            <tr><td style="padding:8px 0;color:#666;">Total IDs en memoria (ventana 90 dias)</td>
                <td style="padding:8px 0;text-align:right;font-weight:600;">{stats['total_seen']:,}</td></tr>
        </table>
        <p style="color:#666;font-size:12px;margin:24px 0 0;line-height:1.5;">
            Si este correo deja de llegar un viernes, el sistema podria estar caido -
            revisar <a href="https://github.com/SergioMolinaM/radar-licitaciones/actions" style="color:#0a4d8c;">GitHub Actions</a>.
        </p>
        <hr style="border:none;border-top:1px solid #eee;margin:20px 0 12px;">
        <p style="color:#999;font-size:11px;">Tercera Letra SpA - monitoreo institucional</p>
    </body></html>
    """


def send_heartbeat(stats: dict) -> bool:
    """Envia el reporte semanal. Retorna False si Resend no configurado o falla."""
    api_key = os.getenv("RESEND_API_KEY")
    destinatario = os.getenv("RADAR_TO_EMAIL")
    remitente = os.getenv("RADAR_FROM_EMAIL", "radar@terceraletra.cl")

    if not api_key or not destinatario:
        logger.warning("Heartbeat no enviado - falta RESEND_API_KEY o RADAR_TO_EMAIL")
        return False

    fecha = datetime.now().strftime("%d/%m")
    payload = {
        "from": remitente,
        "to": [destinatario],
        "subject": f"Radar Licitaciones - reporte semanal ({fecha})",
        "html": _render_heartbeat_html(stats),
    }
    try:
        resp = requests.post(
            RESEND_URL, json=payload,
            headers={"Authorization": f"Bearer {api_key}"}, timeout=TIMEOUT,
        )
        resp.raise_for_status()
        logger.info(f"Heartbeat enviado a {destinatario}")
        return True
    except requests.RequestException as e:
        logger.error(f"Error enviando heartbeat: {e}")
        return False
