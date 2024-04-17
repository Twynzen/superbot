import pyautogui as pg
import time
from modules.navigation import change_map
from modules.image_processing import capture_screenshot, image_difference
from config import COMBAT_MODE_REGION, DIRECTION_PATH_ABSTRUB_ZAAP,  MAP_LOCATION_DIR, WAIT_TIME
from modules.image_processing import capture_map_coordinates


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
        
def searchMob():
     print("Comenzando ruta de abstrub para ardilla.")
            # Aquí iría la lógica para buscar mobs en la zona.
     coordinates_before_change = capture_map_coordinates()
     print(f"Coordenadas antes de cambiar de mapa: {coordinates_before_change}")

     change_map(DIRECTION_PATH_ABSTRUB_ZAAP)
     time.sleep(WAIT_TIME)  # Espera después de intentar cambiar de mapa.

     coordinates_after_change = capture_map_coordinates()
     print(f"Coordenadas después de intentar cambiar de mapa: {coordinates_after_change}")

     if coordinates_before_change == coordinates_after_change:
         print("No se detectaron cambios en la posición del mapa. Verificando modo de combate...")
         check_combat_status()  # Verifica continuamente si está en combate
     else:
         print("El cambio de mapa fue exitoso.")
            # Ejemplo: find_mobs()