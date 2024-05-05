import pytesseract
import os
import numpy as np
import cv2
import pyautogui as pg
from config import SCREENSHOTS_DIR, TESSERACT_CMD_PATH, MAP_LOCATION_DIR
from PIL import Image, ImageChops, UnidentifiedImageError



# Configura la ubicación de Tesseract en tu sistema
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD_PATH


def capture_screenshot(region, filename, directory=SCREENSHOTS_DIR):
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
