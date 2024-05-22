import pyautogui as pg
from modules.combat import check_combat_status
from modules.navigation import change_map
from modules.image_processing import capture_map_coordinates
import time
from config import RESOURCE_PATHS, CONFIDENCE_LEVEL, WAIT_TIME, RESOURCES_TYPE,DIRECTION_PATH_ESCARAHOJA_ZAAP,DIRECTION_PATH_ROBLE

EXCEPTIONS = {
        'fresno': {
            'ignored_positions': [(1465, 862)],  # Lista de posiciones a ignorar
        },
        'trigo': {
            'special_click_offsets': [(907, 588, 4, 0)],  # (x, y, offset_x, offset_y) donde x, y es la posición a buscar y (offset_x, offset_y) es cuánto mover el mouse antes de clickear
        }
    }


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

    """Intenta recolectar un recurso dado si se encuentra en pantalla."""
    location = find_resource_on_screen(resource_type)
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
        resources_collected = search_and_collect_resources()
        if not resources_collected:
            print("No se encontraron recursos. Intentando cambiar de mapa...")
            coordinates_before_change = capture_map_coordinates()
            print(f"Coordenadas antes de cambiar de mapa: {coordinates_before_change}")

            change_map(DIRECTION_PATH_ROBLE)
            time.sleep(WAIT_TIME)  # Espera después de intentar cambiar de mapa.

            coordinates_after_change = capture_map_coordinates()
            print(f"Coordenadas después de intentar cambiar de mapa: {coordinates_after_change}")

            if coordinates_before_change == coordinates_after_change:
                print("No se detectaron cambios en la posición del mapa. Verificando modo de combate...")
                check_combat_status()  # Verifica continuamente si está en combate
            else:
                print("El cambio de mapa fue exitoso.")
        time.sleep(2)  # Pequeña pausa antes de mostrar de nuevo el menú

