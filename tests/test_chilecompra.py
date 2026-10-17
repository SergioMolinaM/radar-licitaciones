"""Pruebas de src/sources/chilecompra.py sin red.

Fixture: 7 notas reales de chilecompra.cl bajadas el 17-oct-2026 de
/wp-json/wp/v2/posts (campos id, date, date_gmt, link, title, content, categories;
la 54564 se bajó sin date_gmt y prueba ese camino).
Correr: python -m unittest discover -s tests -t .
"""

import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

import requests

from src.sources import chilecompra as cc

FIXTURE = Path(__file__).parent / "fixtures" / "chilecompra-posts-2026-10-17.json"
POSTS = {p["id"]: p for p in json.loads(FIXTURE.read_text(encoding="utf-8"))}
AHORA = datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)  # sábado 17-oct, 09:00 en Chile


class _Resp:
    def __init__(self, cuerpo, paginas=1, status=200):
        self._cuerpo, self.status_code = cuerpo, status
        self.headers = {"X-WP-TotalPages": str(paginas)}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")

    def json(self):
        return self._cuerpo


class _Sesion:
    def __init__(self, respuesta=None, error=None):
        self.respuesta, self.error, self.llamadas = respuesta, error, []

    def get(self, url, params=None, **kw):
        self.llamadas.append(params)
        if self.error:
            raise self.error
        return self.respuesta


class PostAItem(unittest.TestCase):
    def test_licitacion_plataforma_nueva_15_oct(self):
        it = cc.post_a_item(POSTS[57119], AHORA)
        self.assertIsNotNone(it)
        self.assertEqual(it["codigo"], "869591-4-LE126")
        self.assertEqual(it["fecha_cierre"], "04/11/2026 15:00")
        self.assertEqual(it["estado"], "Licitación")
        self.assertEqual(it["id"], "CC::57119")
        self.assertEqual(it["fuente"], cc.FUENTE)
        self.assertTrue(it["link"].startswith("https://www.chilecompra.cl/2026/10/"))

    def test_se_descarta_cuando_pasa_el_cierre(self):
        # 15:00 de Chile leída como UTC-4 = 19:00 UTC
        self.assertIsNotNone(cc.post_a_item(POSTS[57119], datetime(2026, 11, 4, 18, 59, tzinfo=timezone.utc)))
        self.assertIsNone(cc.post_a_item(POSTS[57119], datetime(2026, 11, 4, 19, 1, tzinfo=timezone.utc)))

    def test_extension_ya_cerrada_no_se_manda(self):
        # 869591-2-LE126, plan de adopción digital: extendida hasta el 2-oct
        cierre, _ = cc.extraer_cierre(cc._texto(POSTS[56581]["content"]["rendered"]), cc._publicada(POSTS[56581]))
        self.assertEqual(cierre.strftime("%d/%m/%Y"), "02/10/2026")
        self.assertIsNone(cc.post_a_item(POSTS[56581], AHORA))

    def test_consulta_al_mercado_dos_ids_y_hora_mas_tardia(self):
        it = cc.post_a_item(POSTS[56995], AHORA)
        self.assertEqual(it["codigo"], "1122317-4-RFIPRI26, 1122317-5-RFIPRI26")
        self.assertEqual(it["fecha_cierre"], "18/10/2026 18:00")
        self.assertEqual(it["estado"], "Consulta al mercado")

    def test_id_cortado_y_digitos_separados(self):
        # La nota dice «ID 2317-3-RFIPRI26» y «Hasta el 2 0 de octubre»
        it = cc.post_a_item(POSTS[56913], AHORA)
        self.assertEqual(it["codigo"], "1122317-3-RFIPRI26")
        self.assertEqual(it["fecha_cierre"], "20/10/2026 23:55")

    def test_manual_de_compras_no_es_oportunidad(self):
        self.assertIn(cc.CATEGORIA_NORMATIVA, POSTS[56931]["categories"])
        self.assertIsNone(cc.post_a_item(POSTS[56931], AHORA))

    def test_compra_coordinada_para_organismos_no_es_oportunidad(self):
        self.assertIsNone(cc.post_a_item(POSTS[56999], AHORA))

    def test_hora_explicita_gana_y_sin_date_gmt(self):
        p = POSTS[54564]  # SERVIU DS 52: «abierta hasta el 5 de junio» y «hasta las 10:00 horas del 5 de junio»
        self.assertNotIn("date_gmt", p)
        cierre, con_hora = cc.extraer_cierre(cc._texto(p["content"]["rendered"]), cc._publicada(p))
        self.assertEqual((cierre.strftime("%d/%m/%Y %H:%M"), con_hora), ("05/06/2026 10:00", True))
        self.assertIsNone(cc.post_a_item(p, AHORA))
        self.assertIsNotNone(cc.post_a_item(p, datetime(2026, 6, 1, tzinfo=timezone.utc)))


def _sintetica(titulo, texto, categorias=(1,)):
    """Nota inventada (casos que el verificador encontró el 17-oct; no son notas reales)."""
    return {"id": 1, "date": "2026-10-15T12:00:00", "date_gmt": "2026-10-15T15:00:00",
            "link": "https://www.chilecompra.cl/x/", "title": {"rendered": titulo},
            "content": {"rendered": f"<p>{texto}</p>"}, "categories": list(categorias)}


class CasosSinteticos(unittest.TestCase):
    def test_licitacion_de_capacitacion_no_se_descarta(self):
        p = _sintetica("ChileCompra licita servicio de capacitación para compradores",
                       "ID 869591-7-LE126. Cierre de recepción de ofertas: 30 de octubre de 2026, a las 15:00 horas.")
        self.assertEqual(cc.post_a_item(p, AHORA)["fecha_cierre"], "30/10/2026 15:00")

    def test_capacitacion_sin_id_se_descarta(self):
        p = _sintetica("Participa en los talleres gratuitos de noviembre", "Inscríbete hasta el 30 de octubre.")
        self.assertIsNone(cc.post_a_item(p, AHORA))

    def test_extension_redactada_con_fecha_vieja_primero(self):
        p = _sintetica("Se extiende el plazo de la licitación de aseo",
                       "El plazo, que vencía el 16 de octubre, se extiende al 30 de octubre. ID 2239-9-LR26.")
        self.assertEqual(cc.post_a_item(p, AHORA)["fecha_cierre"], "30/10/2026")

    def test_titulo_sin_invitacion_con_id_y_cierre(self):
        p = _sintetica("Nuevo Convenio Marco de Aseo: conoce las bases",
                       "Las empresas pueden ofertar en el ID 2239-9-LR26 hasta el 30 de octubre.")
        self.assertIsNotNone(cc.post_a_item(p, AHORA))

    def test_nota_de_resultados_sin_cierre_se_descarta(self):
        p = _sintetica("Compra Coordinada de telefonía logra ahorros",
                       "Los proveedores que participaron en la licitación ID 1122317-5-LR26 ofertaron...")
        self.assertIsNone(cc.post_a_item(p, AHORA))


class ExtraerIds(unittest.TestCase):
    def test_formatos(self):
        texto = "IDs 869591-4-LE126, 2239-5-LR26, 1122317-4-RFIPUB26, 3233-5-RFI26, 869591-12-LP26 y 1469-284-L126"
        self.assertEqual(sorted(cc.extraer_ids(texto)), sorted(
            ["869591-4-LE126", "2239-5-LR26", "1122317-4-RFIPUB26", "3233-5-RFI26", "869591-12-LP26", "1469-284-L126"]))

    def test_no_toma_fechas_ni_montos(self):
        self.assertEqual(cc.extraer_ids("2026-10-15 y 100-1.000 UTM"), [])


class Fetch(unittest.TestCase):
    def test_exito(self):
        ses = _Sesion(_Resp(list(POSTS.values())))
        items, res = cc.fetch_avisos_chilecompra(ultima=None, ahora=AHORA, session=ses)
        self.assertTrue(res["ok"])
        self.assertEqual(res["leidas"], 7)
        self.assertEqual(sorted(i["id"] for i in items), ["CC::56913", "CC::56995", "CC::57119"])
        self.assertEqual(res["ultima"], "2026-10-15T14:57:17")  # date_gmt de la nota 57119
        self.assertEqual(ses.llamadas[0]["after"], "2026-09-17T08:00:00")  # 30 días atrás, hora de Chile (UTC-4)

    def test_relee_48_horas_desde_la_marca(self):
        ses = _Sesion(_Resp([]))
        _, res = cc.fetch_avisos_chilecompra(ultima="2026-10-15T14:57:17", ahora=AHORA, session=ses)
        self.assertEqual(ses.llamadas[0]["after"], "2026-10-13T10:57:17")
        self.assertEqual(res["ultima"], "2026-10-15T14:57:17")  # sin notas nuevas no retrocede

    def test_red_caida(self):
        items, res = cc.fetch_avisos_chilecompra(
            ultima="2026-10-15T14:57:17", ahora=AHORA, session=_Sesion(error=requests.ConnectionError("sin red")))
        self.assertEqual((items, res["ok"], res["ultima"]), ([], False, "2026-10-15T14:57:17"))

    def test_http_500(self):
        items, res = cc.fetch_avisos_chilecompra(ahora=AHORA, session=_Sesion(_Resp([], status=500)))
        self.assertEqual((items, res["ok"], res["ultima"]), ([], False, None))

    def test_json_que_no_es_lista(self):
        items, res = cc.fetch_avisos_chilecompra(ahora=AHORA, session=_Sesion(_Resp({"code": "rest_invalid"})))
        self.assertFalse(res["ok"])


if __name__ == "__main__":
    unittest.main()
