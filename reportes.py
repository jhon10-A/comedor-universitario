"""v5.0: resumen diario de los registros disponibles del comedor (RF11).

El día corresponde a la fecha de servicio de la reserva, también para pagos
y tickets. No corresponde a la fecha de cobro o de emisión del QR.
El llamador aporta las listas en memoria de reservas, pagos y, si dispone de
ella, la lista de resultados de generar_ticket. None indica que el registro
de tickets no está disponible; una lista vacía indica cero tickets registrados.
Los módulos actuales no registran raciones servidas, asistencia ni merma.
"""

from datetime import date
from decimal import Decimal

from config import NOMBRE_COMEDOR
from reservas import consultar_reservas


def consultar_pagos_diarios(pagos, fecha):
    """Devuelve copias de los pagos cuya reserva corresponde a la fecha."""
    return [
        {**pago, "reserva": pago["reserva"].copy()}
        for pago in pagos
        if pago["reserva"]["fecha"] == fecha
    ]


def consultar_tickets_diarios(tickets, fecha):
    """Devuelve tickets únicos por UUID de pago o None si faltan registros.

    tickets contiene los diccionarios devueltos por pagos.generar_ticket.
    La reemisión del mismo identificador cuenta como un solo ticket.
    """
    if tickets is None:
        return None
    unicos = {
        ticket["id"]: ticket.copy()
        for ticket in tickets
        if ticket["fecha"] == fecha
    }
    return list(unicos.values())


def generar_reporte_diario(reservas, pagos, fecha, tickets=None):
    """Resume reservas, pagos, recaudación en soles y tickets del día.

    fecha debe usar AAAA-MM-DD. Se suman los montos registrados como Decimal,
    incluidos los pagos de importe cero, sin recalcular tarifas actuales.
    El resultado no modifica las listas recibidas ni crea registros.
    """
    try:
        fecha_valida = date.fromisoformat(fecha)
    except (TypeError, ValueError):
        raise ValueError("La fecha debe ser válida y usar AAAA-MM-DD.") from None
    if fecha_valida.isoformat() != fecha:
        raise ValueError("La fecha debe usar el formato AAAA-MM-DD.")

    reservas_dia = consultar_reservas(reservas, fecha)
    pagos_dia = consultar_pagos_diarios(pagos, fecha)
    tickets_dia = consultar_tickets_diarios(tickets, fecha)
    recaudacion = sum(
        (Decimal(str(pago["monto"])) for pago in pagos_dia), Decimal("0.00")
    )
    return {
        "fecha": fecha,
        "total_reservas": len(reservas_dia),
        "total_pagos": len(pagos_dia),
        "recaudacion_total": recaudacion,
        "total_tickets": None if tickets_dia is None else len(tickets_dia),
    }


def mostrar_reporte_diario(reporte):
    """Imprime los totales y señala la falta de un registro de tickets."""
    print(f"{NOMBRE_COMEDOR} - v5.0")
    print(f"Fecha de servicio: {reporte['fecha']}")
    print(f"Reservas: {reporte['total_reservas']}")
    print(f"Pagos registrados: {reporte['total_pagos']}")
    print(f"Recaudación: S/ {reporte['recaudacion_total']:.2f}")
    tickets = reporte["total_tickets"]
    if tickets is None:
        print("Tickets emitidos: no disponible (sin registro de emisiones)")
    else:
        print(f"Tickets emitidos: {tickets}")


def demostracion():
    """Muestra una sesión vacía sin crear estudiantes, pagos ni tickets."""
    print("Sesión nueva: los módulos mantienen sus registros en memoria.")
    reporte = generar_reporte_diario([], [], date.today().isoformat())
    mostrar_reporte_diario(reporte)


if __name__ == "__main__":
    demostracion()
