"""RF03: consulta y presentación del menú diario y semanal."""

from config import HORARIO_ALMUERZO, NOMBRE_COMEDOR, PRECIO_RACION


MENU_SEMANAL = {
    "lunes": {
        "plato": "Arroz con pollo",
        "bebida": "Refresco de cebada",
        "acompañamiento": "Ensalada de verduras",
    },
    "martes": {
        "plato": "Lentejas con bistec",
        "bebida": "Limonada",
        "acompañamiento": "Arroz blanco",
    },
    "miércoles": {
        "plato": "Ají de gallina",
        "bebida": "Chicha morada",
        "acompañamiento": "Papa sancochada y arroz",
    },
    "jueves": {
        "plato": "Estofado de res",
        "bebida": "Refresco de maracuyá",
        "acompañamiento": "Arroz y ensalada",
    },
    "viernes": {
        "plato": "Pescado frito",
        "bebida": "Refresco de piña",
        "acompañamiento": "Arroz y yuca sancochada",
    },
}


def consultar_menu_diario(dia):
    """Devuelve el menú del día o None si no está publicado."""
    dia = dia.strip().lower()
    if dia == "miercoles":
        dia = "miércoles"
    return MENU_SEMANAL.get(dia)


def consultar_menu_semanal():
    """Devuelve los menús publicados de lunes a viernes."""
    return MENU_SEMANAL


def mostrar_menu_diario(dia):
    """Imprime los platos del día solicitado."""
    menu = consultar_menu_diario(dia)
    print(f"\n{dia.strip().capitalize()}")
    print("-" * 40)
    if menu is None:
        print("No hay menú publicado para este día.")
        return
    print(f"Plato principal: {menu['plato']}")
    print(f"Bebida: {menu['bebida']}")
    print(f"Acompañamiento: {menu['acompañamiento']}")


def mostrar_menu_semanal():
    """Imprime el menú semanal en orden de lunes a viernes."""
    print(NOMBRE_COMEDOR)
    print("MENÚ SEMANAL - LUNES A VIERNES")
    print(f"Horario de almuerzo: {HORARIO_ALMUERZO}")
    print(f"Precio por ración: S/ {PRECIO_RACION:.2f}")
    for dia in consultar_menu_semanal():
        mostrar_menu_diario(dia)


if __name__ == "__main__":
    mostrar_menu_semanal()
