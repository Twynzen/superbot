# navigation.py
import pytesseract
import pyperclip

import pygetwindow as gw
import pyautogui as pg
import os
import time
from config import TOOLTIP_REGIONS, WAIT_TIME, ZAAP_IMAGES_DIR, TELEPORT_BUTTON_REGION, ZAAPS, ZAAP_INTERFACE_REGION, ZAAP_LOCATIONS
from modules.image_processing import capture_map_coordinates

TESSERACT_CMD_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD_PATH
from collections import defaultdict

# Estructura para registrar intentos fallidos
failed_moves_registry = defaultdict(set)
previous_position = None


def clean_coordinates(coord):
    coord = coord.strip().split(',')
    x = ''.join(filter(lambda c: c.isdigit() or c == '-', coord[0]))
    y = ''.join(filter(lambda c: c.isdigit() or c == '-', coord[1]))
    return f"{x},{y}"

def calculate_distance(pos1, pos2):
    x1, y1 = map(int, clean_coordinates(pos1).split(','))
    x2, y2 = map(int, clean_coordinates(pos2).split(','))
    return abs(x1 - x2) + abs(y1 - y2)


def get_closest_zaap(position):
    min_distance = float('inf')
    closest_zaap = None
    for zaap in ZAAPS:
        distance = calculate_distance(position, zaap)
        if distance < min_distance:
            min_distance = distance
            closest_zaap = zaap
    return closest_zaap


def get_zaap_name_by_coordinates(coordinates):
    coordinates = clean_coordinates(coordinates) 
    for zaap in ZAAP_LOCATIONS:
        if clean_coordinates(zaap["coordenadas"]) == coordinates:
            return zaap["nombre"]
    print(f"No se encontró un Zaap con las coordenadas {coordinates}")
    return None

def detect_and_click_zaap():
    for zaap_image in os.listdir(ZAAP_IMAGES_DIR):
        zaap_image_path = os.path.join(ZAAP_IMAGES_DIR, zaap_image)
        try:
            location = pg.locateCenterOnScreen(zaap_image_path, confidence=0.8)
            if location:
                pg.click(location)
                time.sleep(WAIT_TIME)
                return True
        except pg.ImageNotFoundException:
            continue  # Si no se encuentra la imagen, pasa a la siguiente
        except Exception as e:
            print(f"Error al buscar el zaap en {zaap_image_path}: {e}")
    return False


def search_zaap_in_interface(zaap_name):
    print(zaap_name, "ZAAP BUSCADO EN LA INTERFAZ")
    search_input_region = (1300, 220, 1200, 140)  # Ajusta esta región según la posición del campo de búsqueda en la interfaz
    pg.click(search_input_region[0], search_input_region[1])
    pyperclip.copy(zaap_name)  # Copia el nombre del Zaap al portapapeles
    pg.hotkey('ctrl', 'v')  # Pega el nombre del Zaap desde el portapapeles
    time.sleep(2)  # Espera un momento para que los resultados se actualicen

def get_sorted_zaaps_by_distance(position):
    """
    Devuelve una lista de Zaaps ordenados por distancia desde la posición dada.
    """
    distances = []
    for zaap in ZAAPS:
        distance = calculate_distance(position, zaap)
        distances.append((zaap, distance))
    distances.sort(key=lambda x: x[1])
    return distances



def check_zaap_route_exceptions(current_position, target_zaap):
    if current_position == '12,12' and target_zaap == '10,22':
        print("Excepción de Zaap detectada: Ignorando Zaap 10,22 desde la posición 12,12.")
        return True  # Indica que esta excepción aplica y debe ser ignorada
    return False

def teleport_to_closest_zaap(current_position, target_position):
    # Listar Zaaps en orden de cercanía desde la posición actual
    sorted_zaaps_to_current = get_sorted_zaaps_by_distance(current_position)
    print("Zaaps ordenados por cercanía desde la posición actual:")
    for zaap, distance in sorted_zaaps_to_current:
        zaap_name = get_zaap_name_by_coordinates(zaap)
        # print(f"{zaap} ({zaap_name}) - Distancia: {distance}")

    # Verificar excepciones de ruta de Zaap y filtrar Zaap 10,22 si estamos en 12,12
    if current_position == '12,12':
        sorted_zaaps_to_current = [zaap for zaap in sorted_zaaps_to_current if clean_coordinates(zaap[0]) != '10,22']
        print("Excepción de Zaap detectada: Ignorando Zaap 10,22 desde la posición 12,12.")

    if not sorted_zaaps_to_current:
        print("No se encontraron Zaaps adecuados después de aplicar las excepciones. Moviéndose normalmente.")
        move_to_position(target_position)
        return

    closest_zaap_to_current = sorted_zaaps_to_current[0][0]  # El más cercano filtrado

    # Listar Zaaps en orden de cercanía desde la posición de destino
    sorted_zaaps_to_target = get_sorted_zaaps_by_distance(target_position)
    print("Zaaps ordenados por cercanía desde la posición de destino:")
    for zaap, distance in sorted_zaaps_to_target:
        zaap_name = get_zaap_name_by_coordinates(zaap)
        print(f"{zaap} ({zaap_name}) - Distancia: {distance}")

    closest_zaap_to_target = sorted_zaaps_to_target[0][0]  # El más cercano

    # Verificar si el zaap más cercano desde la posición actual es el mismo que nos acercaría a la posición de destino
    if closest_zaap_to_current == closest_zaap_to_target:
        print("El zaap más cercano desde la posición actual es el mismo que nos acercaría a la posición de destino. Evitando teleportarse.")
        move_to_position(target_position)
        return

    if closest_zaap_to_current and closest_zaap_to_target:
        closest_zaap_name_to_current = get_zaap_name_by_coordinates(closest_zaap_to_current)
        closest_zaap_name_to_target = get_zaap_name_by_coordinates(closest_zaap_to_target)

        if not closest_zaap_name_to_current or not closest_zaap_name_to_target:
            print("No se encontró el nombre del Zaap más cercano.")
            return

        print(f"Zaap más cercano a la posición actual ({current_position}): {closest_zaap_to_current} ({closest_zaap_name_to_current})")
        print(f"Zaap más cercano a la posición de destino ({target_position}): {closest_zaap_to_target} ({closest_zaap_name_to_target})")

        print(f"Teleporting to closest Zaap from {closest_zaap_to_current} ({closest_zaap_name_to_current}) to {closest_zaap_to_target} ({closest_zaap_name_to_target})")

        move_to_position(closest_zaap_to_current)
        if detect_and_click_zaap():
            search_zaap_in_interface(closest_zaap_name_to_target)
            pg.click(TELEPORT_BUTTON_REGION)
            time.sleep(WAIT_TIME)
        else:
            print("No Zaap detected at current position. Moving normally.")
    else:
        print("No close Zaap found for teleportation. Moving normally.")
        
def change_map(direction):
    if direction not in TOOLTIP_REGIONS:
        raise ValueError(f"Dirección inválida: {direction}. Las direcciones válidas son: {list(TOOLTIP_REGIONS.keys())}")
    
    pg.click(TOOLTIP_REGIONS[direction])
    time.sleep(WAIT_TIME)
    
def try_alternate_directions(current_x, current_y, target_x, target_y):
    primary_direction = None
    secondary_direction = None

    # Determinar la dirección primaria y secundaria basada en la dirección fallida
    if current_x != target_x:
        # Si hay diferencia en x (fallo izquierda/derecha), intentar mover hacia arriba
        primary_direction = 'up'
    elif current_y != target_y:
        # Si hay diferencia en y (fallo arriba/abajo), intentar mover hacia la derecha
        primary_direction = 'right'

    for direction in [primary_direction]:
        if (current_x, current_y, direction) not in failed_moves_registry[(current_x, current_y)]:
            print(f"Intentando ruta alternativa de ({current_x}, {current_y}) a ({current_x + (direction == 'right') - (direction == 'left')}, {current_y + (direction == 'down') - (direction == 'up')}) dirección {direction}")
            change_map(direction)
            time.sleep(WAIT_TIME)
            new_position = capture_map_coordinates()
            new_x, new_y = map(int, clean_coordinates(new_position).split(','))
            if (new_x, new_y) != previous_position:  # Evitar retrocesos
                if new_position != "Capture Failed" and new_position != "Error":
                    if new_x != current_x or new_y != current_y:
                        return new_position

    return f"{current_x},{current_y}"  # Retorna la misma posición si no se logró mover


def move_to_position(target_position):
    global previous_position
    target_x, target_y = map(int, clean_coordinates(target_position).split(','))
    failed_attempts = 0
    previous_position = None  # Inicializar la posición anterior

    while True:
        current_position = capture_map_coordinates()
        if current_position == "Capture Failed" or current_position == "Error":
            print("Error capturando coordenadas actuales. Reintentando...")
            continue

        current_x, current_y = map(int, clean_coordinates(current_position).split(','))
        
        # Comprobar excepciones de ruta
        new_x, new_y, exception_applied = check_route_exceptions(f"{current_x},{current_y}", target_position)
        if exception_applied:
            previous_position = (current_x, current_y)
            current_x, current_y = new_x, new_y
            print(f"Posición actualizada a ({current_x}, {current_y}) por excepción de ruta.")
            continue

        if current_x == target_x and current_y == target_y:
            print(f"Posición objetivo {target_position} alcanzada.")
            break

        move_direction = None
        is_backtracking = False

        if current_x < target_x and (current_x, current_y, 'right') not in failed_moves_registry[(current_x, current_y)]:
            move_direction = 'right'
        elif current_x > target_x and (current_x, current_y, 'left') not in failed_moves_registry[(current_x, current_y)]:
            move_direction = 'left'
        elif current_y < target_y and (current_x, current_y, 'down') not in failed_moves_registry[(current_x, current_y)]:
            move_direction = 'down'
        elif current_y > target_y and (current_x, current_y, 'up') not in failed_moves_registry[(current_x, current_y)]:
            move_direction = 'up'

        if move_direction:
            print(f"Intentando mover de ({current_x}, {current_y}) a ({current_x + (move_direction == 'right') - (move_direction == 'left')}, {current_y + (move_direction == 'down') - (move_direction == 'up')}) dirección {move_direction}")
            change_map(move_direction)
            time.sleep(WAIT_TIME)
            new_position = capture_map_coordinates()
            new_x, new_y = map(int, clean_coordinates(new_position).split(','))
            if previous_position and (new_x, new_y) == previous_position:
                print(f"Retroceso detectado de {new_position} a {current_position}. Intentando rutas alternativas...")
                is_backtracking = True
        else:
            print("Todos los movimientos en esta dirección han fallado previamente. Intentando rutas alternativas...")
            new_position = try_alternate_directions(current_x, current_y, target_x, target_y)

        new_x, new_y = map(int, clean_coordinates(new_position).split(','))

        if new_x == current_x and new_y == current_y:
            failed_attempts += 1
            if move_direction:
                print(f"Movimiento fallido registrado: ({current_x}, {current_y}) dirección {move_direction}")
                failed_moves_registry[(current_x, current_y)].add((current_x, current_y, move_direction))
            if failed_attempts >= 2:
                print("Intentos fallidos repetidos. Intentando rutas alternativas...")
                new_position = try_alternate_directions(current_x, current_y, target_x, target_y)
                new_x, new_y = map(int, clean_coordinates(new_position).split(','))
                if new_x == current_x and new_y == current_y:
                    print("No se pudo mover después de intentar rutas alternativas. Reintentando...")
                    failed_attempts = 0  # Resetear los intentos fallidos pa

def check_route_exceptions(current_position, target_position):
    if current_position == '-6,-9' and target_position == '-11,-8':
        print("Excepción de ruta detectada: de -6,-9 a -11,-8, moviéndose hacia arriba.")
        change_map('up')
        time.sleep(WAIT_TIME)
        new_position = capture_map_coordinates()
        new_x, new_y = map(int, clean_coordinates(new_position).split(','))
        return new_x, new_y, True  # Retornar la nueva posición y un indicador de que se aplicó una excepción

    if current_position == '-6,-10' and target_position == '-5,-8':
        print("Excepción de ruta detectada: de -6,-10 a -5,-8, moviéndose hacia abajo.")
        change_map('down')
        time.sleep(WAIT_TIME)
        new_position = capture_map_coordinates()
        new_x, new_y = map(int, clean_coordinates(new_position).split(','))
        return new_x, new_y, True  # Retornar la nueva posición y un indicador de que se aplicó una excepción
    
    if current_position == '-8,-10' and target_position == '-11,-8':
        print("Excepción de ruta detectada: de -8,-10 a -11,-8, moviéndose hacia abajo.")
        change_map('down')
        time.sleep(WAIT_TIME)
        new_position = capture_map_coordinates()
        new_x, new_y = map(int, clean_coordinates(new_position).split(','))
        return new_x, new_y, True  # Retornar la nueva posición y un indicador de que se aplicó una excepción
    
    if current_position == '-7,-9' and target_position == '-5,-8':
        print("Excepción de ruta detectada: de -7,-9 a -5,-8, moviéndose hacia arriba.")
        change_map('up')
        time.sleep(WAIT_TIME)
        new_position = capture_map_coordinates()
        new_x, new_y = map(int, clean_coordinates(new_position).split(','))
        return new_x, new_y, True  # Retornar la nueva posición y un indicador de que se aplicó una excepción  
    
    return None, None, False

# navigation.py

