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

def clean_coordinates(coord):
    coord = coord.strip().split(',')
    x = ''.join(filter(lambda c: c.isdigit() or c == '-', coord[0]))
    y = ''.join(filter(lambda c: c.isdigit() or c == '-', coord[1]))
    return f"{x},{y}"

def calculate_distance(pos1, pos2):
    x1, y1 = map(int, clean_coordinates(pos1).split(','))
    x2, y2 = map(int, clean_coordinates(pos2).split(','))
    return abs(x1 - x2) + abs(y1 - y2)


#CUADRAR CLICK EN BUSCAR DESTINO
#VALIDAR BUSQUEDA DE OTROS ZAAPS NO SOLO DEL -1,13
#TELETRANSPORTAR CON EXTIO

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

def teleport_to_closest_zaap(current_position, target_position):
    # Listar Zaaps en orden de cercanía desde la posición actual
    sorted_zaaps_to_current = get_sorted_zaaps_by_distance(current_position)
    print("Zaaps ordenados por cercanía desde la posición actual:")
    for zaap, distance in sorted_zaaps_to_current:
        zaap_name = get_zaap_name_by_coordinates(zaap)
        print(f"{zaap} ({zaap_name}) - Distancia: {distance}")

    closest_zaap_to_current = sorted_zaaps_to_current[0][0]  # El más cercano

    # Listar Zaaps en orden de cercanía desde la posición de destino
    sorted_zaaps_to_target = get_sorted_zaaps_by_distance(target_position)
    print("Zaaps ordenados por cercanía desde la posición de destino:")
    for zaap, distance in sorted_zaaps_to_target:
        zaap_name = get_zaap_name_by_coordinates(zaap)
        print(f"{zaap} ({zaap_name}) - Distancia: {distance}")

    closest_zaap_to_target = sorted_zaaps_to_target[0][0]  # El más cercano

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

def move_to_position(target_position):
    target_x, target_y = map(int, clean_coordinates(target_position).split(','))
    while True:
        current_position = capture_map_coordinates()
        if current_position == "Capture Failed" or current_position == "Error":
            print("Error capturando coordenadas actuales. Reintentando...")
            continue

        current_x, current_y = map(int, clean_coordinates(current_position).split(','))
        print(f"Moviéndose de {current_position} a {target_position}")

        if current_x == target_x and current_y == target_y:
            print(f"Posición objetivo {target_position} alcanzada.")
            break

        if current_x < target_x:
            change_map('right')
        elif current_x > target_x:
            change_map('left')

        if current_y < target_y:
            change_map('down')
        elif current_y > target_y:
            change_map('up')