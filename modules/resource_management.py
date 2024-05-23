import pyautogui as pg
from modules.combat import check_combat_status
from modules.navigation import change_map, move_to_position
from modules.image_processing import capture_map_coordinates
import time
from config import RESOURCE_PATHS, CONFIDENCE_LEVEL, WAIT_TIME, RESOURCES_TYPE,DIRECTION_PATH_ESCARAHOJA_ZAAP,DIRECTION_PATH_ROBLE, DIRECTION_PATH_ABSTRUB_ZAAP, ZAAPS, DIRECTION_PATH_TREBOL


PREDEFINED_POSITIONS = {
    "5,-8": DIRECTION_PATH_ABSTRUB_ZAAP,
    "-1,24": DIRECTION_PATH_ESCARAHOJA_ZAAP,
    "-11,-8": DIRECTION_PATH_ROBLE,
    "3,21": DIRECTION_PATH_TREBOL
}

EXCEPTIONS = {
        'fresno': {
            'ignored_positions': [(1465, 862)],  # Lista de posiciones a ignorar
        },
        'trigo': {
            'special_click_offsets': [(907, 588, 4, 0)],  # (x, y, offset_x, offset_y) donde x, y es la posición a buscar y (offset_x, offset_y) es cuánto mover el mouse antes de clickear
        }
    }

def clean_coordinates(coord):
    """
    Limpia y convierte las coordenadas capturadas en un formato adecuado.
    """
    coord = coord.strip().split(',')
    x = ''.join(filter(str.isdigit, coord[0])) if '-' not in coord[0] else '-' + ''.join(filter(str.isdigit, coord[0]))
    y = ''.join(filter(str.isdigit, coord[1])) if '-' not in coord[1] else '-' + ''.join(filter(str.isdigit, coord[1]))
    return f"{x},{y}"

def find_resource_on_screen(resource_type, category):
    """Busca los recursos en pantalla por tipo y categoría y devuelve la ubicación si los encuentra."""
    category_dict = RESOURCE_PATHS.get(category, {})
    paths = category_dict.get(resource_type, [])
    for path in paths:
        try:
            location = pg.locateCenterOnScreen(path, confidence=CONFIDENCE_LEVEL)
            if location:
                print(f"Recurso de tipo {resource_type} en categoría {category} encontrado en {path}.")
                return location
        except pg.ImageNotFoundException:
            continue  # Simplemente continúa con la siguiente imagen
        except Exception as e:
            print(f"Error al buscar el recurso de tipo {resource_type} en categoría {category} en {path}: {e}")
    # Si termina el bucle y no encuentra nada, imprime un mensaje general.
    print(f"Recurso de tipo {resource_type} en categoría {category} no encontrado.")
    return None



def apply_exceptions(resource_type, location):
    """Aplica las excepciones de clic especificadas en el diccionario EXCEPTIONS."""
    if resource_type in EXCEPTIONS:
        resource_exceptions = EXCEPTIONS[resource_type]
        print(f"Aplicando excepciones para {resource_type}, posición encontrada: {location}")

        # Para el caso de trigo que necesita un clic especial
        if 'special_click_offsets' in resource_exceptions:
            for (x, y, offset_x, offset_y) in resource_exceptions['special_click_offsets']:
                if (location.x, location.y) == (x, y):
                    new_location = (location.x + offset_x, location.y + offset_y)
                    print(f"Aplicando offset especial a {resource_type}: {new_location}")
                    return new_location

        # Para el caso de fresno ignorado
        if 'ignored_positions' in resource_exceptions:
            for ignored_pos in resource_exceptions['ignored_positions']:
                if (location.x, location.y) == ignored_pos:
                    print(f"Ignorando posición de {resource_type} en {ignored_pos}")
                    return None

        # Para el caso de salvia que necesita ajustar el clic
        if 'click_adjustments' in resource_exceptions:
            for (offset_x, offset_y) in resource_exceptions['click_adjustments']:
                new_location = (location.x + offset_x, location.y + offset_y)
                print(f"Aplicando ajuste de clic a {resource_type}: {new_location}")
                return new_location

    return (location.x, location.y)


 
def collect_resource(resource_type):
    """Intenta recolectar un recurso dado si se encuentra en pantalla."""
    category = RESOURCES_TYPE.get(resource_type, None)
    if category is None:
        print(f"Categoría no definida para el recurso {resource_type}.")
        return False  # Salir si no hay categoría definida.

    location = find_resource_on_screen(resource_type, category)
    if location:
        # Aplica las excepciones antes de hacer clic.
        new_location = apply_exceptions(resource_type, location)
        if new_location:
            pg.click(new_location)
            time.sleep(WAIT_TIME)
            print(f"Recolectado {resource_type}.")
            return True
        else:
            print(f"Recurso {resource_type} ignorado debido a una excepción.")
    return False

def search_and_collect_resources():
    """Bucle principal para buscar y recolectar recursos repetidamente hasta que no encuentre más."""
    resources_found = False
    for resource_type in RESOURCES_TYPE:  # Solo iterar sobre los tipos definidos con categoría
        while collect_resource(resource_type):  # Continúa intentando recolectar mientras haya recursos.
            resources_found = True
            print(f"Recolectado {resource_type}. Volviendo a buscar {resource_type}...")
    
    if not resources_found:
        print("No se encontraron más recursos. Intentando cambiar de mapa...")
        return False
    return True

def search_resources():
    initial_position = capture_map_coordinates()
    print(f"Coordenadas iniciales: {initial_position}")

    # Preguntar al usuario cuál es la posición predefinida principal
    main_position = choose_predefined_position()

    # Moverse a la posición predefinida principal si no coincide
    move_to_predefined_position(initial_position, main_position)
    resources_collected = search_and_collect_resources()
    if not resources_collected:
        print("No se encontraron más recursos en la zona.")
    time.sleep(2) 

    # Ejecutar la ruta de la posición predefinida principal
    path = PREDEFINED_POSITIONS[main_position]
    for direction in path:
        change_map(direction)
        time.sleep(WAIT_TIME)  # Pausa entre cambios de mapa

        # Capturar y mostrar la posición del mapa actual y anterior
        current_position = capture_map_coordinates()
        print(f"Coordenadas después de cambiar de mapa: {current_position}")

        # Buscar recursos en la zona antes de cambiar de mapa
        while True:
            resources_collected = search_and_collect_resources()
            if not resources_collected:
                print("No se encontraron más recursos en la zona.")
                break
            time.sleep(2)  # Pequeña pausa antes de buscar de nuevo

    # Solicitar segunda y tercera posición predefinida opcional
    while True:
        second_position_choice = input("¿Desea definir una segunda posición predefinida? (y/n): ")
        if second_position_choice.lower() == 'y':
            second_position = choose_predefined_position()
            move_to_predefined_position(current_position, second_position)

            path = PREDEFINED_POSITIONS[second_position]
            for direction in path:
                change_map(direction)
                time.sleep(WAIT_TIME)  # Pausa entre cambios de mapa

                # Capturar y mostrar la posición del mapa actual y anterior
                current_position = capture_map_coordinates()
                print(f"Coordenadas después de cambiar de mapa: {current_position}")

                # Buscar recursos en la zona antes de cambiar de mapa
                while True:
                    resources_collected = search_and_collect_resources()
                    if not resources_collected:
                        print("No se encontraron más recursos en la zona.")
                        break
                    time.sleep(2)  # Pequeña pausa antes de buscar de nuevo

            third_position_choice = input("¿Desea definir una tercera posición predefinida? (y/n): ")
            if third_position_choice.lower() == 'y':
                third_position = choose_predefined_position()
                move_to_predefined_position(current_position, third_position)

                path = PREDEFINED_POSITIONS[third_position]
                for direction in path:
                    change_map(direction)
                    time.sleep(WAIT_TIME)  # Pausa entre cambios de mapa

                    # Capturar y mostrar la posición del mapa actual y anterior
                    current_position = capture_map_coordinates()
                    print(f"Coordenadas después de cambiar de mapa: {current_position}")

                    # Buscar recursos en la zona antes de cambiar de mapa
                    while True:
                        resources_collected = search_and_collect_resources()
                        if not resources_collected:
                            print("No se encontraron más recursos en la zona.")
                            break
                        time.sleep(2)  # Pequeña pausa antes de buscar de nuevo
            else:
                print("No se definió una tercera posición.")
                break
        else:
            break
def calculate_distance(pos1, pos2):
    x1, y1 = map(int, clean_coordinates(pos1).split(','))
    x2, y2 = map(int, clean_coordinates(pos2).split(','))
    return abs(x1 - x2) + abs(y1 - y2)

def get_closest_zaap(current_position, target_position):
    min_distance = float('inf')
    closest_zaap = None
    for zaap in ZAAPS:
        distance = calculate_distance(current_position, zaap) + calculate_distance(zaap, target_position)
        if distance < min_distance:
            min_distance = distance
            closest_zaap = zaap
    return closest_zaap

def move_to_predefined_position(initial_position, target_position):
    initial_position = clean_coordinates(initial_position)
    target_position = clean_coordinates(target_position)
    if initial_position != target_position:
        print(f"Posición inicial no coincide con la posición predefinida. Moviéndose a la posición predefinida {target_position}.")
        closest_zaap = get_closest_zaap(initial_position, target_position)
        print(f"Moverse al Zaap más cercano: {closest_zaap}")
        move_to_position(closest_zaap)
        move_to_position(target_position)
    else:
        print(f"Posición inicial coincide con la posición predefinida: {initial_position}. Usando ruta correspondiente.")


def choose_predefined_position():
    print("Seleccione una posición predefinida:")
    positions = list(PREDEFINED_POSITIONS.keys())
    for index, position in enumerate(positions, start=1):
        print(f"{index}. {position}")
    choice = int(input("Ingrese el número de la posición deseada: "))
    if 1 <= choice <= len(positions):
        return positions[choice - 1]
    else:
        print("Selección inválida. Por favor, intente de nuevo.")
        return choose_predefined_position()