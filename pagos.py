"""v4.0: registro de pagos (RF06) y tickets QR (RF07).

Los pagos se conservan en la lista del llamador, en memoria como las reservas.
Se asume beca completa (S/ 0.00). El no becario paga PRECIO_RACION.
Instalar la dependencia con python -m pip install -r requirements.txt.
Ejecutar la demostración con python pagos.py.
"""

import json
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

import qrcode
from qrcode.image.svg import SvgPathImage

from config import NOMBRE_COMEDOR, PRECIO_RACION
from reservas import registrar_reserva


def calcular_tarifa(condicion):
    """Devuelve soles como Decimal para becario o no becario."""
    if not isinstance(condicion, str):
        raise ValueError("La condición debe ser becario o no becario.")
    condicion = condicion.strip().lower()
    if condicion == "becario":
        return Decimal("0.00")
    if condicion == "no becario":
        return Decimal(str(PRECIO_RACION)).quantize(Decimal("0.01"))
    raise ValueError("La condición debe ser becario o no becario.")


def registrar_pago(pagos, reserva, condicion, monto):
    """Registra el importe exacto para una reserva y evita pagos duplicados.

    reserva es el diccionario devuelto por registrar_reserva. monto admite
    números o texto decimal. Para becarios se registra un importe cero.
    Los identificadores y fechas de registro se generan automáticamente.
    """
    tarifa = calcular_tarifa(condicion)
    try:
        importe = Decimal(str(monto))
    except ArithmeticError:
        raise ValueError("El monto debe ser un número válido.") from None
    if not importe.is_finite() or importe != tarifa:
        raise ValueError(f"El monto debe ser exactamente S/ {tarifa:.2f}.")

    # Reutiliza las validaciones de la versión de reservas existente.
    reserva_validada = registrar_reserva(
        [], reserva["estudiante"], reserva["fecha"], reserva["turno"]
    )
    if any(pago["reserva"] == reserva_validada for pago in pagos):
        raise ValueError("La reserva ya tiene un pago registrado.")
    pago = {
        "id": str(uuid4()),
        "reserva": reserva_validada,
        "condicion": condicion.strip().lower(),
        "monto": tarifa,
        "registrado_en": datetime.now(timezone.utc).isoformat(),
    }
    pagos.append(pago)
    return {**pago, "reserva": reserva_validada.copy()}


def generar_ticket(pagos, pago_id, directorio="tickets"):
    """Emite un SVG QR para un pago registrado y devuelve sus datos.

    El UUID del pago identifica también su ticket. Reemitir conserva el código.
    El QR contiene JSON con identificador, reserva, condición e importe en PEN.
    Un fallo de escritura permite reintentar con el mismo identificador.
    """
    pago = next((pago for pago in pagos if pago["id"] == pago_id), None)
    if pago is None:
        raise ValueError("El pago no está registrado.")
    datos = {
        "id": pago["id"],
        **pago["reserva"],
        "condicion": pago["condicion"],
        "monto": str(pago["monto"]),
        "moneda": "PEN",
    }
    contenido = json.dumps(datos, ensure_ascii=False, sort_keys=True)
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,
                       box_size=10, border=4)
    qr.add_data(contenido)
    qr.make(fit=True)
    carpeta = Path(directorio)
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / f"ticket_{pago['id']}.svg"
    qr.make_image(image_factory=SvgPathImage).save(str(ruta))
    return {**datos, "contenido_qr": contenido, "archivo_qr": str(ruta)}


def demostracion():
    """Registra ambos tipos de estudiante y genera sus tickets en ./tickets."""
    pagos = []
    reservas = []
    print(f"{NOMBRE_COMEDOR} - v4.0")
    for estudiante, condicion in (("2026001", "becario"),
                                  ("2026002", "no becario")):
        reserva = registrar_reserva(reservas, estudiante,
                                    date.today().isoformat(), "almuerzo")
        pago = registrar_pago(pagos, reserva, condicion, calcular_tarifa(condicion))
        ticket = generar_ticket(pagos, pago["id"])
        print(f"{estudiante} | {condicion} | S/ {pago['monto']:.2f}")
        print(f"Ticket {ticket['id']} | QR {ticket['archivo_qr']}")


if __name__ == "__main__":
    demostracion()
