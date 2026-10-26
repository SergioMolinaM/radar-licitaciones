"""Pruebas sin red del filtro internacional y de la fuente PNUD (26-oct-2026).

Correr: python -m unittest discover -s tests -t .
"""

import unittest
from unittest import mock

from src.config import UNDP_FEEDS, UNDP_FEEDS_SIN_KEYWORDS
from src.filters import matches_keywords, matches_keywords_intl
from src.sources import undp


class FiltroInternacional(unittest.TestCase):
    def test_ingles_calza(self):
        self.assertEqual(matches_keywords_intl("Communication strategy for climate action")[0], True)
        self.assertEqual(matches_keywords_intl("National survey on public opinion")[1], ["survey", "public opinion"])

    def test_ingles_excluye_bienes(self):
        self.assertEqual(matches_keywords_intl("Supply of refrigeration equipment for schools"), (False, []))

    def test_espanol_sigue(self):
        self.assertTrue(matches_keywords_intl("Plataforma LMS, Micrositio e Infraestructura Digital")[0])

    def test_sin_keyword_pasa_lo_no_excluido(self):
        self.assertEqual(matches_keywords_intl("Aplicación de prueba piloto a 100 establecimientos", exigir_keyword=False),
                         (True, ["(todo el feed del país)"]))
        self.assertFalse(matches_keywords_intl("Supply of medical equipment", exigir_keyword=False)[0])

    def test_mercado_publico_no_usa_ingles(self):
        # Las keywords en inglés no pueden entrar al filtro de MP ni a las búsquedas de Compra Ágil.
        self.assertFalse(matches_keywords("Communication strategy")[0])


class FeedChile(unittest.TestCase):
    def test_chile_es_chi_y_sin_keyword(self):
        self.assertTrue(UNDP_FEEDS["Chile"].endswith("/CHI.xml"))
        self.assertIn("Chile", UNDP_FEEDS_SIN_KEYWORDS)

    def test_fetch_pasa_exigir_keyword_por_pais(self):
        llamadas = []

        def falso(url, fuente, pais_filtro=None, exigir_keyword=True):
            llamadas.append((fuente, exigir_keyword))
            return [], 1

        with mock.patch.object(undp, "_fetch_feed", side_effect=falso):
            undp.fetch_undp_notices()
        self.assertIn(("PNUD Chile", False), llamadas)
        self.assertIn(("PNUD Bolivia", True), llamadas)


class EmpleosPnud(unittest.TestCase):
    """Casos reales del listado del 26-oct-2026."""

    def _det(self, tipo):
        return {"requisitionFlexFields": [{"Prompt": "Vacancy Type", "Value": tipo}]}

    def test_chile_pasa_siempre(self):
        from src.sources.undp_empleos import _postulable
        req = {"Title": "Asistente de Edición - UCE - NPSA5", "PrimaryLocationCountry": "CL"}
        self.assertTrue(_postulable(req, self._det("National Personnel Service Agreement")))

    def test_remotos(self):
        from src.sources.undp_empleos import _postulable
        casos = [
            ("Foundations, Philanthropies, Family Offices Advisor, IPSA12, Home-Based, UNCDF "
             "[Open to internal and external candidates]", "International Personnel Services Agreement", True),
            ("Procurement Analyst (Open to Nationals of Kenya or with Kenyan work permit)", "Fixed Term", False),
            ("Communications and Research Analyst [Open to Tier 1 & 2 Applicants]", "Fixed Term", False),
            ("SDG Finance and Private Sector Development Research Intern - 36124 (Home Based)", "Internship", False),
            ("National Technical Specialist Roster - Sustainable human development",
             "National Personnel Service Agreement", False),
        ]
        for titulo, tipo, esperado in casos:
            self.assertEqual(_postulable({"Title": titulo, "PrimaryLocationCountry": "CN"}, self._det(tipo)),
                             esperado, titulo)

    def test_cierre_en_hora_de_chile(self):
        from src.sources.undp_empleos import _cierre_chile
        self.assertEqual(_cierre_chile("2026-10-28T03:59:00+00:00"), "2026-10-28")
        self.assertEqual(_cierre_chile(None), "")


if __name__ == "__main__":
    unittest.main()
