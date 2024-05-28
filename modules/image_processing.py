import time
import pytesseract
import os
import numpy as np
import cv2
import pyautogui as pg
from config import SCREENSHOTS_DIR, TESSERACT_CMD_PATH, MAP_LOCATION_DIR, CONFIDENCE_LEVEL, ZAAP_IMAGES_DIR,WAIT_TIME
from PIL import Image, ImageChops, UnidentifiedImageError
import config_shared 



# Configura la ubicación de Tesseract en tu sistema
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD_PATH





def capture_screenshot(region=None, filename="screenshot.png", directory=SCREENSHOTS_DIR):
    """Toma una captura de pantalla de la región especificada y guarda la imagen en el directorio dado."""
    try:
        # Crea el directorio si no existe
        if not os.path.exists(directory):
            os.makedirs(directory)

        screenshot = pg.screenshot(region=region)
        screenshot_path = f"{directory}/{filename}"
        screenshot.save(screenshot_path)
        return screenshot_path
    except Exception as e:
        print(f"Error al capturar la pantalla: {e}")
        return None


def capture_map_coordinates():
    """Captura las coordenadas del mapa usando OCR."""
    try:
        region_to_capture = (0, 65, 100, 40)
        filename = "map_coordinates.png"
        screenshot_path = capture_screenshot(region_to_capture, filename, MAP_LOCATION_DIR)
        if screenshot_path:
            coordinates = process_image_for_text(screenshot_path)
            if coordinates.strip() == "":  # Verifica si Tesseract devolvió una cadena vacía.
                print("Tesseract no pudo detectar coordenadas en la imagen.")
                return "Unknown"  # Puedes devolver un valor que denote desconocido o error.
            return coordinates
        else:
            print("Fallo al capturar la imagen para OCR.")
            return "Capture Failed"
    except Exception as e:
        print(f"Error al capturar las coordenadas del mapa: {e}")
        return "Error"

def process_image_for_text(image_path):
    """Utiliza OCR para extraer texto de una imagen con configuraciones optimizadas."""
    try:
        image = Image.open(image_path)
        # Preprocesamiento de la imagen (opcional): puedes aplicar filtros para mejorar el contraste, convertir a escala de grises, etc.
        # ...
        # Configuraciones de Tesseract
        custom_config = r'--oem 3 --psm 6'
        return pytesseract.image_to_string(image, config=custom_config)
    except UnidentifiedImageError as e:
        print(f"No se pudo abrir la imagen: {e}")
        return None
    except Exception as e:
        print(f"Error al procesar la imagen para obtener texto: {e}")
        return None

def capture_and_process_image(region, image_name, output_folder):
    """Captura una imagen de una región específica, la guarda y la procesa con OCR para extraer texto."""
    # Comprueba y crea la carpeta de salida si no existe
    output_path = f"{MAP_LOCATION_DIR}/{output_folder}"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Captura y guarda la imagen
    image_path = f"{output_path}/{image_name}.png"
    image = pg.screenshot(region=region)
    image.save(image_path)

    # Procesar la imagen con OCR
    text = pytesseract.image_to_string(cv2.imread(image_path))
    return text, image_path

def get_image_difference(image1_path, image2_path):
    """Obtiene la diferencia entre dos imágenes."""
    try:
        img1 = Image.open(image1_path)
        img2 = Image.open(image2_path)
        return ImageChops.difference(img1, img2)
    except Exception as e:
        print(f"Error al obtener la diferencia entre imágenes: {e}")
        return None
    
def image_difference(image1_path, image2_path, save_debug=True):
    """Calcula la diferencia entre dos imágenes usando OpenCV y devuelve si son significativamente diferentes.
    Opcionalmente guarda las imágenes comparadas para depuración."""
    debug_dir = f"{MAP_LOCATION_DIR}/combat_check_images"  # Directorio para guardar imágenes de depuración
    if save_debug and not os.path.exists(debug_dir):
        os.makedirs(debug_dir)
    
    try:
        # Cargar imágenes y convertirlas a escala de grises
        img1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

        # Calcular la diferencia entre las imágenes
        diff = cv2.absdiff(img1, img2)
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

        # Guardar imágenes para depuración
        if save_debug:
            cv2.imwrite(os.path.join(debug_dir, 'last_reference_image.png'), img1)
            cv2.imwrite(os.path.join(debug_dir, 'last_debug_image.png'), img2)
            cv2.imwrite(os.path.join(debug_dir, 'diff_image.png'), thresh)  # Guardar imagen de diferencia para revisión

        # Comprobar si hay diferencias significativas
        if np.sum(thresh) > 0:  # Si hay píxeles blancos en la imagen umbralizada, hay diferencias
            print("Differences detected. Combat has ended or the scene has changed.")
            return True
        else:
            print("No differences found. Combat is still active.")
            return False
    except Exception as e:
        print(f"Error processing image difference using OpenCV: {e}")
        return True  # Si hay un error, suponer que el combate ha terminado por precaución

def capture_current_game_frame():
    """
    Captura la pantalla actual del juego y devuelve una imagen.
    La región capturada puede ser ajustada según la resolución y la ventana del juego.
    """
    game_region = (0, 0, 1920, 1080)  # Ajusta esta tupla a la región exacta del juego
    frame = pg.screenshot(region=game_region)
    frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    return frame

def detect_map_edges(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    return edges

def capture_combat_map_frame():
    # Definir la región específica donde se espera que esté el mapa de combate.
    # Ajusta los valores de la tupla según la posición y tamaño del mapa en tu juego.
    combat_map_region = (100, 200, 800, 600)
    frame = pg.screenshot(region=combat_map_region)
    frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    return frame


def pause_and_validate_mouse_position():
    """Pausa la ejecución y muestra la posición actual del mouse para validación."""
    mouse_x, mouse_y = pg.position()
    print(f"Mouse position: ({mouse_x}, {mouse_y})")
    #input("Press Enter to continue...")

def detect_and_click_exit_combat():
    try:
        exit_button_x = 1440  # Ajustar según sea necesario
        exit_button_y = 1010  # Ajustar según sea necesario

        pg.click(exit_button_x, exit_button_y)
        print(f"Click en botón de rendirse en las coordenadas ({exit_button_x}, {exit_button_y}).")
        pause_and_validate_mouse_position()

        time.sleep(2)  # Espera un momento para que aparezca el cuadro de confirmación

        confirm_button_x = 940  # Ajustar según sea necesario
        confirm_button_y = 580  # Ajustar según sea necesario

        pg.click(confirm_button_x, confirm_button_y)
        print(f"Click en botón 'Ok' en las coordenadas ({confirm_button_x}, {confirm_button_y}).")
        pause_and_validate_mouse_position()

        time.sleep(2)

        # Verificar si aparece el cuadro de diálogo de muerte en toda la pantalla
        death_dialog_location = pg.locateCenterOnScreen('ojoIA/death_dialog.png', confidence=0.3)
        if death_dialog_location:
            revive_button_x = 940 # Ajustar según sea necesario
            revive_button_y = 615  # Ajustar según sea necesario

            pg.click(revive_button_x, revive_button_y)
            print(f"Click en botón 'Sí' en las coordenadas ({revive_button_x}, {revive_button_y}).")
            config_shared.is_dead = True
            print("Personaje está muerto. Actualizando config_shared.is_dead a True.")
        else:
            print("No se detectó el cuadro de diálogo de muerte, siguiendo flujo de derrota normal.")
        
        
        time.sleep(2)

        close_button_x = 950  # Ajustar según sea necesario
        close_button_y = 630  # Ajustar según sea necesario

        pg.click(close_button_x, close_button_y)
        pause_and_validate_mouse_position()
        
        print(f"Click en botón 'Cerrar' en las coordenadas ({close_button_x}, {close_button_y}).")
        time.sleep(3)
        
        return True

    except Exception as e:
        screenshot_path = capture_screenshot(region=None, filename="exit_combat_detection_error.png", directory="ojoIA/errors")
        print(f"Error al intentar clickear el botón de rendirse: {e}. Captura guardada en {screenshot_path}")
    return False

def ocr_read_text(image_path, lang='eng'):
    """Utiliza OCR para leer el texto de una imagen."""
    try:
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, lang=lang)  # Especificar el idioma si es necesario
        return text
    except Exception as e:
        print(f"Error al leer texto de la imagen con OCR: {e}")
        return ""