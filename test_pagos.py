"""Pruebas de v4.0. Ejecutar con python -m unittest -v test_pagos."""

import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch
from uuid import UUID
from xml.etree import ElementTree

from config import PRECIO_RACION
from pagos import calcular_tarifa, generar_ticket, registrar_pago
from reservas import registrar_reserva


class PruebasPagos(unittest.TestCase):
    def setUp(self):
        self.pagos = []
        self.reserva = registrar_reserva([], "2026001", "2026-11-16", "almuerzo")

    def test_tarifas(self):
        self.assertEqual(calcular_tarifa(" Becario "), Decimal("0.00"))
        self.assertEqual(calcular_tarifa("NO BECARIO"), Decimal(str(PRECIO_RACION)))
        for condicion in ("", "docente", None, True):
            with self.subTest(condicion=condicion), self.assertRaises(ValueError):
                calcular_tarifa(condicion)

    def test_registro_ambas_condiciones(self):
        for condicion in ("becario", "no becario"):
            with self.subTest(condicion=condicion):
                pagos = []
                pago = registrar_pago(pagos, self.reserva, condicion,
                                      calcular_tarifa(condicion))
                self.assertEqual(len(pagos), 1)
                self.assertEqual(pago["reserva"], self.reserva)
                self.assertEqual(str(UUID(pago["id"])), pago["id"])
                pago["reserva"]["estudiante"] = "otro"
                self.assertEqual(pagos[0]["reserva"], self.reserva)

    def test_montos_invalidos_no_registran(self):
        for monto in ("abc", None, "NaN", "Infinity", -1, 0, "4.501"):
            with self.subTest(monto=monto), self.assertRaises(ValueError):
                registrar_pago(self.pagos, self.reserva, "no becario", monto)
        self.assertEqual(self.pagos, [])

    def test_duplicado(self):
        registrar_pago(self.pagos, self.reserva, "becario", 0)
        with self.assertRaises(ValueError):
            registrar_pago(self.pagos, self.reserva, "becario", 0)
        self.assertEqual(len(self.pagos), 1)

    def test_ticket_qr_y_reemision(self):
        pago = registrar_pago(self.pagos, self.reserva, "becario", 0)
        with tempfile.TemporaryDirectory() as carpeta:
            ticket = generar_ticket(self.pagos, pago["id"], carpeta)
            contenido = json.loads(ticket["contenido_qr"])
            self.assertEqual(contenido["id"], pago["id"])
            self.assertEqual(contenido["estudiante"], self.reserva["estudiante"])
            self.assertEqual(contenido["monto"], "0.00")
            raiz = ElementTree.parse(ticket["archivo_qr"]).getroot()
            self.assertEqual(raiz.tag, "{http://www.w3.org/2000/svg}svg")
            self.assertTrue(raiz.find("{http://www.w3.org/2000/svg}path").attrib["d"])
            self.assertEqual(generar_ticket(self.pagos, pago["id"], carpeta), ticket)

    def test_identificadores_unicos(self):
        primero = registrar_pago(self.pagos, self.reserva, "becario", 0)
        otra = {**self.reserva, "estudiante": "2026002"}
        segundo = registrar_pago(self.pagos, otra, "becario", 0)
        self.assertNotEqual(primero["id"], segundo["id"])

    def test_pago_inexistente(self):
        with tempfile.TemporaryDirectory() as carpeta:
            with self.assertRaises(ValueError):
                generar_ticket(self.pagos, "inexistente", carpeta)
            self.assertEqual(list(Path(carpeta).iterdir()), [])

    def test_error_escritura_permite_reintento(self):
        pago = registrar_pago(self.pagos, self.reserva, "becario", 0)
        with tempfile.TemporaryDirectory() as carpeta:
            with patch("pagos.Path.mkdir", side_effect=OSError("Sin acceso")):
                with self.assertRaises(OSError):
                    generar_ticket(self.pagos, pago["id"], carpeta)
            self.assertEqual(generar_ticket(self.pagos, pago["id"], carpeta)["id"],
                             pago["id"])


if __name__ == "__main__":
    unittest.main()
