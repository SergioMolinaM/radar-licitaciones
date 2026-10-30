"""Listado completo de Compra Ágil (30-oct-2026), sin red: la API se simula."""

import unittest
from unittest import mock

import requests

from src.sources import compra_agil as ca


class _Resp:
    def __init__(self, status=200, cuerpo=None, headers=None):
        self.status_code = status
        self._cuerpo = cuerpo
        self.headers = headers or {}

    def json(self):
        if self._cuerpo is None:
            raise ValueError("sin JSON")
        return self._cuerpo


def _pagina(items, total):
    return _Resp(200, {"success": "OK", "payload": {"items": items, "paginacion": {"total_paginas": total}}})


def _item(codigo, nombre):
    return {"codigo": codigo, "nombre": nombre, "fechas": {}, "montos": {}, "institucion": {}}


class _API:
    """Responde según (q o None, página). Un valor callable se evalúa en cada llamada."""

    def __init__(self, respuestas, por_defecto=None):
        self.respuestas = respuestas
        self.por_defecto = por_defecto or _pagina([], 1)
        self.llamadas = []

    def get(self, url, headers=None, params=None, timeout=None):
        clave = (params.get("q"), params.get("numero_pagina"))
        self.llamadas.append(clave)
        r = self.respuestas.get(clave, self.por_defecto)
        if isinstance(r, Exception):
            raise r
        return r() if callable(r) else r


class ListadoTest(unittest.TestCase):
    def setUp(self):
        self.p = [
            mock.patch.object(ca, "PAUSA_ENTRE_SOLICITUDES_S", 0),
            mock.patch.object(ca, "tickets", lambda: [("principal", "T")]),
            mock.patch.object(ca, "LISTADO_TRAMO", ca.timedelta(days=30)),  # un solo tramo, salvo donde se diga
        ]
        for p in self.p:
            p.start()

    def tearDown(self):
        for p in self.p:
            p.stop()

    def _correr(self, api, ultima=None):
        with mock.patch.object(ca.requests, "get", api.get):
            return ca.fetch_compra_agil(cursor=0, ultima=ultima, presupuesto_s=60)

    def test_listado_completo_filtra_por_titulo_y_avanza_la_marca(self):
        api = _API({
            (None, 1): _pagina([_item("1-1-COT26", "Diseño de sitio web municipal"),
                                _item("1-2-COT26", "Adquisición de lijas")], 2),
            (None, 2): _pagina([_item("1-3-COT26", "Servicio de firma electrónica biométrica")], 2),
        })
        matches, r = self._correr(api)
        codigos = {m["codigo"] for m in matches}
        self.assertEqual(codigos, {"1-1-COT26", "1-3-COT26"})
        self.assertTrue(r["listado_ok"])
        self.assertEqual((r["listado_paginas"], r["listado_total"]), (2, 2))
        self.assertIn(ca.CLAVE_LISTADO, r["ultima"])
        self.assertGreaterEqual(r["devueltas"], 3)

    def test_pagina_caida_no_avanza_la_marca_y_sigue_con_las_demas(self):
        api = _API({
            (None, 1): _pagina([_item("1-1-COT26", "Sitio web")], 3),
            (None, 2): _Resp(504, {"message": "Endpoint request timed out"}),
            (None, 3): _pagina([_item("1-3-COT26", "Plataforma blockchain")], 3),
        })
        matches, r = self._correr(api, ultima={ca.CLAVE_LISTADO: "2026-10-29T12:00:00Z"})
        self.assertFalse(r["listado_ok"])
        self.assertEqual((r["listado_paginas"], r["listado_total"]), (2, 3))
        self.assertEqual(r["ultima"][ca.CLAVE_LISTADO], "2026-10-29T12:00:00Z")
        self.assertTrue(r["listado_pendiente"])
        self.assertEqual({m["codigo"] for m in matches}, {"1-1-COT26", "1-3-COT26"})
        self.assertEqual(api.llamadas.count((None, 2)), 2)  # un reintento

    def test_429_en_el_listado_corta_todo_sin_lanzar(self):
        api = _API({(None, 1): _Resp(429, {"errors": [{"mensaje": "límite"}]})})
        matches, r = self._correr(api)
        self.assertEqual(matches, [])
        self.assertIn("429", r["cortado"])
        self.assertFalse(r["listado_ok"])
        self.assertEqual(r["listado_paginas"], 0)
        self.assertNotIn(ca.CLAVE_LISTADO, r["ultima"])
        self.assertTrue(all(q is None for q, _ in api.llamadas))  # no siguió con q

    def test_red_caida_en_la_primera_pagina(self):
        api = _API({(None, 1): requests.ConnectionError("x")})
        _, r = self._correr(api)
        self.assertEqual((r["listado_paginas"], r["listado_total"]), (0, None))
        self.assertFalse(r["listado_ok"])
        self.assertIn("primera página", r["listado_corte"])

    def test_ticket_rechazado_pasa_al_respaldo(self):
        llamadas = {"n": 0}

        def primera():
            llamadas["n"] += 1
            return _Resp(401, {}) if llamadas["n"] == 1 else _pagina([_item("1-1-COT26", "Sitio web")], 1)

        api = _API({(None, 1): primera})
        with mock.patch.object(ca, "tickets", lambda: [("principal", "A"), ("respaldo", "B")]):
            matches, r = self._correr(api)
        self.assertTrue(r["listado_ok"])
        self.assertEqual([m["codigo"] for m in matches], ["1-1-COT26"])

    def test_desde_con_traslape_y_tope(self):
        api = _API({})
        _, r = self._correr(api, ultima={ca.CLAVE_LISTADO: "2026-01-01T00:00:00Z"})
        desde = ca.datetime.strptime(r["listado_desde"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=ca.timezone.utc)
        tope = ca.datetime.now(ca.timezone.utc) - ca.timedelta(days=ca.LISTADO_DIAS_MAX)
        self.assertLess(abs((desde - tope).total_seconds()), 60)

    def test_429_a_mitad_conserva_lo_leido(self):
        api = _API({
            (None, 1): _pagina([_item("1-1-COT26", "Sitio web")], 3),
            (None, 2): _Resp(429, {"errors": [{"mensaje": "límite"}]}),
        })
        matches, r = self._correr(api, ultima={ca.CLAVE_LISTADO: "2026-10-29T12:00:00Z"})
        self.assertEqual([m["codigo"] for m in matches], ["1-1-COT26"])
        self.assertEqual((r["listado_paginas"], r["listado_total"]), (1, 3))
        self.assertIn("429", r["cortado"])
        self.assertFalse(r["listado_ok"])

    def test_total_ilegible_o_recortado_no_cuenta_como_completo(self):
        for pag in ({"total_paginas": "98"}, {}, {"total_paginas": -1}):  # 0 sin ítems es un tramo vacío
            api = _API({(None, 1): _Resp(200, {"success": "OK", "payload": {"items": [], "paginacion": pag}})})
            _, r = self._correr(api, ultima={ca.CLAVE_LISTADO: "2026-10-29T12:00:00Z"})
            self.assertFalse(r["listado_ok"], pag)
            self.assertEqual(r["ultima"][ca.CLAVE_LISTADO], "2026-10-29T12:00:00Z")
        with mock.patch.object(ca, "MAX_PAGINAS_LISTADO", 2):
            api = _API({(None, 1): _pagina([], 5)})
            _, r = self._correr(api, ultima={ca.CLAVE_LISTADO: "2026-10-29T12:00:00Z"})
            self.assertFalse(r["listado_ok"])

    def test_ticket_rechazado_a_mitad_sigue_en_la_misma_pagina(self):
        n = {"p2": 0}

        def p2():
            n["p2"] += 1
            return _Resp(403, {}) if n["p2"] == 1 else _pagina([_item("1-2-COT26", "Sitio web")], 2)

        api = _API({(None, 1): _pagina([], 2), (None, 2): p2})
        with mock.patch.object(ca, "tickets", lambda: [("principal", "A"), ("respaldo", "B")]):
            matches, r = self._correr(api)
        self.assertTrue(r["listado_ok"])
        self.assertEqual(api.llamadas.count((None, 1)), 1)

    def test_marca_corrupta_no_lanza(self):
        _, r = self._correr(_API({}), ultima={ca.CLAVE_LISTADO: 12345})
        self.assertTrue(r["listado_ok"])

    def test_hueco_por_tope_se_informa(self):
        _, r = self._correr(_API({}), ultima={ca.CLAVE_LISTADO: "2026-01-01T00:00:00Z"})
        self.assertTrue(r["listado_hueco"].startswith("2026-01-01"))

    def test_tramos_mueven_la_marca_hasta_el_ultimo_completo(self):
        llamadas = []

        def get(url, headers=None, params=None, timeout=None):
            if params.get("q"):
                return _pagina([], 1)
            llamadas.append((params["publicado_desde"], params.get("publicado_hasta")))
            if len(llamadas) in (2, 3):  # el segundo tramo no responde en sus dos intentos
                return _Resp(504, {})
            return _pagina([_item(f"9-{len(llamadas)}-COT26", "Sitio web")], 1)

        ahora = ca.datetime.now(ca.timezone.utc)
        marca = ca._iso(ahora - ca.timedelta(days=3))
        with mock.patch.object(ca, "LISTADO_TRAMO", ca.timedelta(days=1)), mock.patch.object(ca.requests, "get", get):
            matches, r = ca.fetch_compra_agil(cursor=0, ultima={ca.CLAVE_LISTADO: marca}, presupuesto_s=60)
        self.assertFalse(r["listado_ok"])
        # Todos los tramos con desde y hasta; el primero empieza en marca − traslape.
        self.assertTrue(all(h for _, h in llamadas))
        primero_desde, primero_hasta = llamadas[0]
        self.assertEqual(primero_desde, ca._api_fecha(ca._parse_iso(marca) - ca.LISTADO_TRASLAPE))
        nueva = r["ultima"][ca.CLAVE_LISTADO]
        # state en UTC; la API recibe hora de Chile y el hasta con 1 min de solape
        self.assertEqual(ca._api_fecha(ca._parse_iso(nueva) + ca.timedelta(minutes=1)), primero_hasta)
        self.assertTrue(r["listado_pendiente"].startswith(nueva))
        self.assertEqual(len(llamadas), 3)  # tramo 1 ok, tramo 2 dos intentos, y no sigue

    def test_fecha_para_la_api_en_hora_de_chile(self):
        dt = ca.datetime(2026, 10, 30, 17, 44, 48, tzinfo=ca.timezone.utc)
        self.assertEqual(ca._api_fecha(dt), "2026-10-30T14:44:48Z")  # Chile UTC-3 en horario de verano

    def test_hueco_solo_si_la_marca_quedo_fuera_del_tope(self):
        ahora = ca.datetime.now(ca.timezone.utc)
        dentro = ca._iso(ahora - ca.timedelta(days=ca.LISTADO_DIAS_MAX) + ca.timedelta(hours=1))
        _, r = self._correr(_API({}), ultima={ca.CLAVE_LISTADO: dentro})
        self.assertEqual(r["listado_hueco"], "")

    def test_tramo_vacio_cuenta_como_leido(self):
        api = _API({(None, 1): _Resp(200, {"success": "OK", "payload": {"items": [], "paginacion": {"total_paginas": 0}}})})
        _, r = self._correr(api)
        self.assertTrue(r["listado_ok"])

    def test_q_sigue_despues_del_listado(self):
        api = _API({(None, 1): _pagina([], 1)})
        _, r = self._correr(api)
        self.assertTrue(r["listado_ok"])
        self.assertTrue(any(q is not None for q, _ in api.llamadas))
        self.assertTrue(r["diarios_ok"])


if __name__ == "__main__":
    unittest.main()
