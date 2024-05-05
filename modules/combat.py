import pyautogui as pg
import time
import cv2
import pytesseract
import numpy as np
from modules.navigation import change_map
from modules.image_processing import capture_screenshot, image_difference, capture_and_process_image
from config import COMBAT_MODE_REGION, DIRECTION_PATH_ABSTRUB_ZAAP,  MAP_LOCATION_DIR, WAIT_TIME, PLAYER_NAME, PLAYER_DATA_REGION
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
    """
    Mueve el cursor sobre los personajes en la barra y espera a que aparezcan los nombres en toda la pantalla.
    Mientras está en hover, recopila datos del jugador, del botón verde y del campo de texto general.
    """
    print("Buscando Personaje y recopilando datos...")
    combat_data = []

    # Calcular las posiciones de hover basadas en COMBAT_MODE_REGION
    start_x, start_y, width, height = COMBAT_MODE_REGION
    num_steps = 16  # Cantidad de pasos para moverse a lo largo de la barra

    for step in range(num_steps - 1, -1, -1):  # Invierte el orden del bucle
        hover_position = (start_x + width // 2, start_y + step * (height // num_steps))
        pg.moveTo(hover_position)
        time.sleep(0.2)  # Agregar un pequeño retardo para permitir que la UI del juego responda al hover

        # Toma una captura de pantalla de toda la pantalla
        full_screen_screenshot = pg.screenshot()
        
        # Verificar si el nombre del jugador está presente en la pantalla
        if player_name in pytesseract.image_to_string(np.array(full_screen_screenshot)):
            print(f"{player_name} encontrado en la pantalla!")
            
            # Recopilar datos del jugador
            player_data = extract_player_data(PLAYER_DATA_REGION)
            combat_data.append(player_data)

            # TODO: Implementar y llamar a la función para el botón verde
            # green_button_data = detect_green_button_text(GREEN_BUTTON_REGION)
            # combat_data.append(green_button_data)

            # TODO: Implementar y llamar a la función para el campo de texto general
            # general_text_data = extract_general_text_field(GENERAL_TEXT_FIELD_REGION)
            # combat_data.append(general_text_data)

            # Retornar los datos recopilados
            return combat_data
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

def gather_combat_data(player_name, player_data_region, green_button_region, general_text_field_region):
    """Recopila todos los datos necesarios durante el combate."""
    player_data = extract_player_data(player_data_region)
    green_button_data = detect_green_button_text(green_button_region)
    general_text_data = extract_general_text_field(general_text_field_region)
    
    # Retornar un diccionario con todos los datos recopilados
    return {
        "player_data": player_data,
        "green_button_data": green_button_data,
        "general_text_data": general_text_data
    }
    
def extract_player_data(player_data_region):
    """Extrae los datos del jugador de una región específica utilizando la función genérica."""
    player_data_text, player_data_image_path = capture_and_process_image(
        player_data_region, "player_data", "player_data_folder"
    )
    print("Datos del Jugador Extraídos:", player_data_text)
    return {"player_data": player_data_text, "image_path": player_data_image_path}

def detect_green_button_text(green_button_region):
    """Detecta el texto del botón verde en combate."""
    green_button_text, green_button_image_path = capture_and_process_image(
        green_button_region, "green_button", "green_button_folder"
    )
    return {"green_button_text": green_button_text, "image_path": green_button_image_path}

def extract_general_text_field(general_text_field_region):
    """Extrae el texto del campo general de texto en combate."""
    general_text, general_text_image_path = capture_and_process_image(
        general_text_field_region, "general_text", "general_text_folder"
    )
    return {"general_text": general_text, "image_path": general_text_image_path}