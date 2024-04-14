import pyautogui as pg
import time
from modules.image_processing import capture_screenshot, image_difference
from config import COMBAT_MODE_REGION, CONFIDENCE_LEVEL,  MAP_LOCATION_DIR, WAIT_TIME


def check_combat_status():
    """Revisa de manera indefinida si el bot está en combate, comparando capturas de pantalla con una imagen de referencia."""
    reference_image_path = 'ojoIA/combat_indicator.PNG'
    debug_image_path = f"{MAP_LOCATION_DIR}/combat_debug.png"

    while True:
        capture_screenshot(COMBAT_MODE_REGION, 'combat_debug.png', MAP_LOCATION_DIR)
        # Compara la imagen de depuración con la imagen de referencia.
        if not image_difference(debug_image_path, reference_image_path):
            print("Combat is still active...")
            time.sleep(3)  # Revisa cada 3 segundos
        else:
            print("Combat status check indicates combat has ended.")
            break