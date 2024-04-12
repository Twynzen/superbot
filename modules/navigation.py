import pyautogui as pg
import time
from config import DIRECTIONS, TOOLTIP_REGIONS, WAIT_TIME

CURRENT_DIRECTION_INDEX = 0

def change_map():
    global CURRENT_DIRECTION_INDEX
    direction_to_move = DIRECTIONS[CURRENT_DIRECTION_INDEX]
    CURRENT_DIRECTION_INDEX = (CURRENT_DIRECTION_INDEX + 1) % len(DIRECTIONS)
    
    # Mueve el cursor al botón de la dirección deseada y hace clic.
    pg.click(TOOLTIP_REGIONS[direction_to_move])
    time.sleep(WAIT_TIME)  # Espera después de clickear para dar tiempo al juego de cambiar el mapa.
    
    # Aquí podrías implementar lógica adicional si es necesario, como verificaciones después de cambiar el mapa.
