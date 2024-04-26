import pyautogui as pg
import time
import cv2
import pytesseract
import numpy as np
from modules.navigation import change_map
from modules.image_processing import capture_screenshot, image_difference
from config import COMBAT_MODE_REGION, DIRECTION_PATH_ABSTRUB_ZAAP,  MAP_LOCATION_DIR, WAIT_TIME, PLAYER_NAME
from modules.image_processing import capture_map_coordinates, capture_combat_map_frame, detect_map_edges

def check_combat_status():
    """Revisa si el bot está en combate, basado en la presencia de la barra de estado."""
    while True:
        status_bar_image_path = capture_status_bar()
        
        # Aquí podrías realizar un procesamiento de imagen adicional si es necesario
        # Por ejemplo, aplicar filtros, detección de bordes, etc.

        if is_status_bar_detected(status_bar_image_path):
            print("Combat is still active...")
            hover_and_detect_player_name(PLAYER_NAME)
            
            # Aquí podrías agregar lógica adicional basada en la información de la barra de estado
        else:
            print("Combat status check indicates combat has ended.")
            break

        time.sleep(3) 
        
def is_status_bar_detected(image_path):
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Rangos HSV para colores específicos
    # Estos valores son solo ejemplos, debes ajustarlos según los colores exactos de tu juego
    red_lower = np.array([0, 70, 50])
    red_upper = np.array([10, 255, 255])
    blue_lower = np.array([110, 50, 50])
    blue_upper = np.array([130, 255, 255])
    
    # Crear máscaras para los colores
    mask_red = cv2.inRange(hsv, red_lower, red_upper)
    mask_blue = cv2.inRange(hsv, blue_lower, blue_upper)
    
    # Buscar contornos en las máscaras
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Dibujar contornos sobre la imagen original para la visualización
    cv2.drawContours(image, contours_red, -1, (0, 255, 0), 3)  # Dibuja contornos rojos en verde
    cv2.drawContours(image, contours_blue, -1, (255, 0, 0), 3)  # Dibuja contornos azules en azul

    # TESTEO :Mostrar las máscaras y la imagen original con contornos QUITAR!
    # cv2.imshow('Red Mask', mask_red)
    # cv2.imshow('Blue Mask', mask_blue)
    # cv2.imshow('Detected Contours', image)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Verifica si hay contornos significativos de los colores rojo y azul
    red_detected = any(cv2.contourArea(contour) > 100 for contour in contours_red)
    blue_detected = any(cv2.contourArea(contour) > 100 for contour in contours_blue)
    
    # Aquí podría ir la lógica adicional para el reconocimiento de patrones y formas

    return red_detected and blue_detected    

def hover_and_detect_player_name(player_name):
    """Mueve el cursor sobre los personajes en la barra y espera a que aparezcan los nombres en toda la pantalla."""
    print("Buscando Personaje")
    # Calcular las posiciones de hover basadas en COMBAT_MODE_REGION
    start_x, start_y, width, height = COMBAT_MODE_REGION
    num_steps = 15  # Cantidad de pasos para moverse a lo largo de la barra
    step_size = height // num_steps  # Divide la altura en 3 partes para las 3 barras

    for step in range(num_steps):
        hover_position = (start_x + width // 2, start_y + step * step_size)
        pg.moveTo(hover_position)
        time.sleep(0.01)  # Un retardo más corto para el hover

        # Toma una captura de pantalla de toda la pantalla
        full_screen_screenshot = pg.screenshot()
        full_screen_screenshot_path = f"{MAP_LOCATION_DIR}/full_screen_with_name.png"
        full_screen_screenshot.save(full_screen_screenshot_path)

        # Leer el nombre resaltado usando OCR
        text = pytesseract.image_to_string(cv2.imread(full_screen_screenshot_path))
        
        if player_name in text:
            print(f"{player_name} encontrado en la pantalla!")
            # Aquí podrías añadir lógica adicional para determinar la posición del personaje.
            break
        else:
            # Si no se encuentra el nombre, continúa con el siguiente paso.
            continue
 
def capture_status_bar():
    # Define la región donde se espera que esté la barra de estado de los personajes.
    # Estas coordenadas son hipotéticas y deben ser ajustadas según tu juego.
    status_bar_region = COMBAT_MODE_REGION
    status_bar_image = pg.screenshot(region=status_bar_region)
    status_bar_image_path = f"{MAP_LOCATION_DIR}/current_status_bar.png"
    status_bar_image.save(status_bar_image_path)
    return status_bar_image_path
        
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


def initiate_combat_sequence():
    # Asegúrate de que estás en combate
    if check_combat_status():
        
        
        # Captura el marco del mapa de combate y detecta los bordes
        combat_map_frame = capture_combat_map_frame()
        combat_map_edges = detect_map_edges(combat_map_frame)
        
        cv2.imshow('Combat Map Edges', combat_map_edges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # Con base en los bordes, determina la posición del personaje y enemigos
        # ... (lógica para determinar posiciones)
        # Realiza el siguiente movimiento o ataque
        # ... (lógica para realizar acciones)

# Puedes llamar a initiate_combat_sequence en el lugar apropiado donde manejas el combate en main.py o combat.py