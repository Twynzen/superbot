# navigation.py

import pyautogui as pg
import time
from config import TOOLTIP_REGIONS, WAIT_TIME
from modules.image_processing import capture_map_coordinates


CURRENT_DIRECTION_INDEX = 0

def clean_coordinates(coord):
    """
    Limpia y convierte las coordenadas capturadas en un formato adecuado.
    """
    coord = coord.strip().split(',')
    x = ''.join(filter(lambda c: c.isdigit() or c == '-', coord[0]))
    y = ''.join(filter(lambda c: c.isdigit() or c == '-', coord[1]))
    return f"{x},{y}"

def change_map(direction):
    """
    Cambia el mapa en la dirección especificada.
    """
    if direction not in TOOLTIP_REGIONS:
        raise ValueError(f"Dirección inválida: {direction}. Las direcciones válidas son: {list(TOOLTIP_REGIONS.keys())}")
    
    pg.click(TOOLTIP_REGIONS[direction])
    time.sleep(WAIT_TIME) 

def move_to_position(target_position):
    """
    Mueve al bot a una posición específica en el mapa.
    """
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