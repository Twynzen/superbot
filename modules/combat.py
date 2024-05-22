import pyautogui as pg
import time
import cv2
import pytesseract
import numpy as np
from modules.navigation import change_map
from modules.image_processing import capture_screenshot, image_difference, capture_and_process_image
from config import COMBAT_MODE_REGION, DIRECTION_PATH_ABSTRUB_ZAAP,  MAP_LOCATION_DIR, WAIT_TIME, PLAYER_NAME, PLAYER_DATA_REGION, BOARD_REGION, GAME_SCREEN_REGION
from modules.image_processing import capture_map_coordinates, capture_combat_map_frame, detect_map_edges
import torch
from ultralytics import YOLO
import mss
import random

class_colors = {}


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
    
    
           # TODO: Identificar enemigo y dibujar línea
            # TODO: Validar casillas verdes de movimiento
              # TODO: Implementar y llamar a la función para el botón verde
            # green_button_data = detect_green_button_text(GREEN_BUTTON_REGION)
            # combat_data.append(green_button_data)

            # TODO: Implementar y llamar a la función para el campo de texto general
            # general_text_data = extract_general_text_field(GENERAL_TEXT_FIELD_REGION)
            # combat_data.append(general_text_data)
    """
    Mueve el cursor sobre los personajes en la barra y espera a que aparezcan los nombres en toda la pantalla.
    Mientras está en hover, recopila datos del jugador, del botón verde y del campo de texto general.
    """
    print("Buscando personaje y recopilando datos...")
    combat_data = []
    start_x, start_y, width, height = COMBAT_MODE_REGION
    num_steps = 16

    for step in range(num_steps - 1, -1, -1):
        # Mover el cursor en la barra lateral de COMBAT_MODE_REGION para activar el nombre
        hover_position = (start_x + width // 2, start_y + step * (height // num_steps))
        pg.moveTo(hover_position)
        time.sleep(0.2)  # Tiempo para que el UI responda al hover

        # Captura de BOARD_REGION después de cada movimiento de hover para detectar nombres en el tablero
        board_screenshot = pg.screenshot(region=BOARD_REGION)
        current_frame = np.array(board_screenshot)

        # Utilizar pytesseract para realizar OCR en la imagen capturada de BOARD_REGION
        ocr_result = pytesseract.image_to_data(current_frame, output_type=pytesseract.Output.DICT)
        for i, text in enumerate(ocr_result['text']):
            if player_name in text:
                x, y, w, h = ocr_result['left'][i], ocr_result['top'][i], ocr_result['width'][i], ocr_result['height'][i]
                
                # Dibujar la línea vertical 100 píxeles abajo del texto detectado
                draw_vertical_line(current_frame, x + w // 2, y + h , 20)
                
                # Guardar la imagen con la línea para verificación
                verification_image_path = f"{MAP_LOCATION_DIR}/verification_image_with_line.png"
                cv2.imwrite(verification_image_path, current_frame)
                print(f"Imagen con línea guardada para verificación en {verification_image_path}")
                
                cv2.imshow("Verification Image with Line", current_frame)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                # Agregar los datos recopilados al conjunto de datos de combate
                player_data = extract_player_data(PLAYER_DATA_REGION)
                combat_data.append(player_data)
                return combat_data  # Retorna después de detectar el primer nombre coincidente

        time.sleep(0.5)  # Pequeña pausa para evitar sobrecargar el sistema
        
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


def draw_vertical_line(image, center_x, base_y, line_height):
    """Dibuja una línea vertical corta en la posición x del personaje detectado, empezando desde base_y hacia abajo."""
    adjusted_base_y = base_y  +70
    cv2.line(image, (center_x, adjusted_base_y), (center_x, adjusted_base_y - line_height), (0, 255, 0), 2)  
    return image


def get_color_for_class(class_name):
    if class_name not in class_colors:
        class_colors[class_name] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return class_colors[class_name]

def detect_objects_in_real_time():
    # Cargar el modelo entrenado
    model = YOLO("C:\\Users\\Daniel\\Desktop\\Daniel\\labellmg\\datasetCombat\\runs\\detect\\train2\\weights\\best.pt")

    # Inicializar el capturador de pantalla
    sct = mss.mss()
    last_detections = {}
    screenshot_taken = False  # Flag para verificar si el pantallazo ya fue tomado

    while True:
        # Capturar la pantalla
        screenshot = sct.grab(GAME_SCREEN_REGION)
        img = np.array(screenshot)

        # Convertir la imagen de BGR a RGB (mss devuelve una imagen en formato BGR)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # Hacer predicciones
        results = model(img)

        current_detections = {}
        log_entries = []

        # Dibujar las predicciones en la imagen
        for result in results[0].boxes.data:  # Acceder a los resultados como tensores
            x1, y1, x2, y2, conf, cls = result
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            class_name = model.names[int(cls)]
            color = get_color_for_class(class_name)
            x_center, y_center = (x1 + x2) // 2, (y1 + y2) // 2

            current_detections[class_name] = (x_center, y_center, conf)

            # Solo dibujar si la posición ha cambiado significativamente
            if class_name not in last_detections or (x_center, y_center) != last_detections[class_name][:2]:
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                cv2.putText(img, f'{class_name} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Preparar la entrada de log
            log_entries.append(f"- {class_name} at ({x_center}, {y_center}) with confidence {conf:.2f}")

        last_detections = current_detections

        # Imprimir los logs formateados
        if log_entries:
            print("\nDetected objects:")
            print("\n".join(log_entries))

        # Tomar y guardar el pantallazo solo una vez
        if not screenshot_taken and current_detections:
            cv2.imwrite("screenshot.png", img)
            screenshot_taken = True
            print("Pantallazo guardado como screenshot.png")

        # Pausa de 3 segundos
        time.sleep(3)