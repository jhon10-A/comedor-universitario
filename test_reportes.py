"""Pruebas con registros de prueba creados mediante los módulos existentes."""

from copy import deepcopy
from decimal import Decimal
from tempfile import TemporaryDirectory
import unittest

from config import PRECIO_RACION
from pagos import calcular_tarifa, generar_ticket, registrar_pago
from reportes import (
    consultar_pagos_diarios,
    consultar_tickets_diarios,
    generar_reporte_diario,
)
from reservas import registrar_reserva


class PruebasReportes(unittest.TestCase):
    def setUp(self):
        self.fecha = "2026-11-16"
        self.reservas = []
        self.pagos = []

    def registrar(self, estudiante, condicion, fecha=None, turno="almuerzo"):
        reserva = registrar_reserva(
            self.reservas, estudiante, fecha or self.fecha, turno
        )
        return registrar_pago(
            self.pagos, reserva, condicion, calcular_tarifa(condicion)
        )

    def test_calculos_y_filtro_por_fecha_de_servicio(self):
        self.registrar("001", "becario")
        self.registrar("002", "no becario")
        self.registrar("003", "no becario", turno="cena")
        self.registrar("004", "no becario", fecha="2026-11-17")
        registrar_reserva(self.reservas, "005", self.fecha, "almuerzo")
        originales = deepcopy((self.reservas, self.pagos))
        reporte = generar_reporte_diario(self.reservas, self.pagos, self.fecha)
        self.assertEqual(reporte["total_reservas"], 4)
        self.assertEqual(reporte["total_pagos"], 3)
        self.assertEqual(reporte["recaudacion_total"],
                         Decimal(str(PRECIO_RACION)) * 2)
        self.assertIsNone(reporte["total_tickets"])
        self.assertEqual((self.reservas, self.pagos), originales)

    def test_sin_registros(self):
        reporte = generar_reporte_diario([], [], self.fecha, [])
        self.assertEqual(reporte, {
            "fecha": self.fecha,
            "total_reservas": 0,
            "total_pagos": 0,
            "recaudacion_total": Decimal("0.00"),
            "total_tickets": 0,
        })

    def test_fecha_sin_movimientos(self):
        self.registrar("001", "no becario")
        reporte = generar_reporte_diario(
            self.reservas, self.pagos, "2026-11-17", []
        )
        self.assertEqual(reporte["total_reservas"], 0)
        self.assertEqual(reporte["total_pagos"], 0)
        self.assertEqual(reporte["recaudacion_total"], Decimal("0.00"))
        self.assertEqual(reporte["total_tickets"], 0)

    def test_tickets_emitidos_y_reemision(self):
        pago = self.registrar("001", "becario")
        self.registrar("002", "no becario")
        otro = self.registrar("003", "no becario", fecha="2026-11-17")
        with TemporaryDirectory() as carpeta:
            tickets = [
                generar_ticket(self.pagos, pago["id"], carpeta),
                generar_ticket(self.pagos, pago["id"], carpeta),
                generar_ticket(self.pagos, otro["id"], carpeta),
            ]
            originales = deepcopy(tickets)
            reporte = generar_reporte_diario(
                self.reservas, self.pagos, self.fecha, tickets
            )
            self.assertEqual(reporte["total_pagos"], 2)
            self.assertEqual(reporte["total_tickets"], 1)
            self.assertEqual(tickets, originales)
            consulta = consultar_tickets_diarios(tickets, self.fecha)
            consulta[0]["estudiante"] = "modificado"
            self.assertEqual(tickets, originales)

    def test_pago_sin_emision_no_cuenta_como_ticket(self):
        self.registrar("001", "no becario")
        reporte = generar_reporte_diario(self.reservas, self.pagos, self.fecha, [])
        self.assertEqual(reporte["total_pagos"], 1)
        self.assertEqual(reporte["total_tickets"], 0)

    def test_consulta_pagos_devuelve_copias(self):
        self.registrar("001", "becario")
        originales = deepcopy(self.pagos)
        consulta = consultar_pagos_diarios(self.pagos, self.fecha)
        consulta[0]["reserva"]["estudiante"] = "modificado"
        self.assertEqual(self.pagos, originales)

    def test_suma_importes_historicos_sin_recalcular_tarifa(self):
        # Simula importes ya registrados antes de un cambio de tarifa.
        self.registrar("001", "no becario")
        self.registrar("002", "no becario")
        self.pagos[0]["monto"] = Decimal("0.10")
        self.pagos[1]["monto"] = Decimal("0.20")
        reporte = generar_reporte_diario(self.reservas, self.pagos, self.fecha)
        self.assertEqual(reporte["recaudacion_total"], Decimal("0.30"))

    def test_fechas_invalidas(self):
        for fecha in (None, "", "2026-02-30", "20261116", "16/11/2026"):
            with self.subTest(fecha=fecha), self.assertRaises(ValueError):
                generar_reporte_diario([], [], fecha)


if __name__ == "__main__":
    unittest.main()
