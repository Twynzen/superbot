import pyautogui as pg
from config import COMBAT_MODE_REGION, CONFIDENCE_LEVEL

def is_in_combat_mode():
    """Determina si el bot está en combate buscando una imagen específica en la pantalla."""
    try:
        # Ruta a la imagen que indica que estamos en combate.
        combat_indicator_image_path = 'ojoIA/combat_indicator.PNG'
        
        # Busca la imagen en la región especificada con un nivel de confianza establecido.
        combat_indicator = pg.locateOnScreen(combat_indicator_image_path, region=COMBAT_MODE_REGION, confidence=CONFIDENCE_LEVEL)
        
        # Si se encuentra la imagen, devuelve True, indicando que el bot está en combate.
        return combat_indicator is not None

    except pg.ImageNotFoundException:
        # Si no se encuentra la imagen, escribe en la consola y asume que no está en combate.
        print("Combat indicator not found. Assuming not in combat mode.")
        return False
