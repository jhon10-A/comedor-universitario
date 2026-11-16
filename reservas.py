"""v3.0: reservas de raciones (RF04) y control de aforo (RF05).

Las reservas se mantienen en memoria y se reinician al cerrar el programa.
Cada estudiante puede reservar una ración por fecha y turno.
"""

from datetime import date

from config import AFORO_MAXIMO, HORARIO_ALMUERZO, NOMBRE_COMEDOR, PRECIO_RACION


def consultar_reservas(reservas, fecha=None, turno=None):
    """Devuelve copias de las reservas, con filtros opcionales de fecha y turno."""
    if turno is not None:
        turno = turno.strip().lower()
    return [
        reserva.copy()
        for reserva in reservas
        if (fecha is None or reserva["fecha"] == fecha)
        and (turno is None or reserva["turno"] == turno)
    ]


def cupos_disponibles(reservas, fecha, turno):
    """Calcula los cupos restantes para una fecha y un turno concretos."""
    ocupados = len(consultar_reservas(reservas, fecha, turno))
    return max(0, AFORO_MAXIMO - ocupados)


def registrar_reserva(reservas, estudiante, fecha, turno):
    """Registra una ración o lanza ValueError si los datos o el aforo lo impiden.

    estudiante es el código del estudiante; fecha usa el formato AAAA-MM-DD.
    La lista recibida pertenece al llamador, sin estado global compartido.
    """
    estudiante = estudiante.strip()
    turno = turno.strip().lower()
    if not estudiante or not turno:
        raise ValueError("El código del estudiante y el turno son obligatorios.")
    try:
        fecha_valida = date.fromisoformat(fecha)
    except (TypeError, ValueError):
        raise ValueError("La fecha debe ser válida y usar AAAA-MM-DD.") from None
    if fecha_valida.isoformat() != fecha:
        raise ValueError("La fecha debe usar el formato AAAA-MM-DD.")

    reservas_turno = consultar_reservas(reservas, fecha, turno)
    if any(reserva["estudiante"] == estudiante for reserva in reservas_turno):
        raise ValueError("El estudiante ya tiene una reserva para esa fecha y turno.")
    if cupos_disponibles(reservas, fecha, turno) == 0:
        raise ValueError("Aforo máximo alcanzado: no quedan cupos disponibles.")

    reserva = {"estudiante": estudiante, "fecha": fecha, "turno": turno}
    reservas.append(reserva)
    return reserva.copy()


def demostracion():
    """Carga ejemplos y muestra consultas y rechazo por aforo completo."""
    reservas = []
    fecha = "2026-11-16"
    turno = "almuerzo"
    print(f"{NOMBRE_COMEDOR} - v3.0")
    print(f"Ración: S/ {PRECIO_RACION:.2f} | Almuerzo: {HORARIO_ALMUERZO}")
    print(f"Aforo máximo por fecha y turno: {AFORO_MAXIMO}")

    for estudiante in ("2026001", "2026002", "2026003"):
        registrar_reserva(reservas, estudiante, fecha, turno)
    print(f"\nReservas para {fecha}, {turno}:")
    for reserva in consultar_reservas(reservas, fecha, turno):
        print(f"  {reserva['estudiante']} | {reserva['fecha']} | {reserva['turno']}")
    print(f"Cupos disponibles: {cupos_disponibles(reservas, fecha, turno)}")

    try:
        registrar_reserva(reservas, "2026001", fecha, turno)
    except ValueError as error:
        print(f"Reserva duplicada rechazada: {error}")

    for numero in range(4, AFORO_MAXIMO + 1):
        registrar_reserva(reservas, f"2026{numero:03d}", fecha, turno)
    print(f"\nCupos después de completar el aforo: {cupos_disponibles(reservas, fecha, turno)}")
    try:
        registrar_reserva(reservas, "2026999", fecha, turno)
    except ValueError as error:
        print(f"Reserva adicional rechazada: {error}")
    print(f"Total registrado: {len(consultar_reservas(reservas))}")
    print(f"Cupos para el día siguiente: {cupos_disponibles(reservas, '2026-11-17', turno)}")
    print(f"Cupos para otro turno: {cupos_disponibles(reservas, fecha, 'cena')}")


if __name__ == "__main__":
    demostracion()
