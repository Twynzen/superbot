import pytesseract
import os
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

def capture_and_process_image(region):
    """Combina la captura de pantalla y el procesamiento de OCR."""
    try:
        screenshot_path = capture_screenshot(region, 'temp.png')
        if screenshot_path:
            text = process_image_for_text(screenshot_path)
            return text
        return None
    except Exception as e:
        print(f"Error al capturar y procesar la imagen: {e}")
        return None

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
    """Calcula la diferencia entre dos imágenes y devuelve si son significativamente diferentes.
    Opcionalmente guarda las imágenes comparadas para depuración."""
    debug_dir = f"{MAP_LOCATION_DIR}/combat_check_images"  # Directorio para guardar imágenes de depuración
    if save_debug and not os.path.exists(debug_dir):
        os.makedirs(debug_dir)
    
    try:
        image1 = Image.open(image1_path).convert('L')  # Convertir a escala de grises para uniformidad
        image2 = Image.open(image2_path).convert('L')

        # Guardar imágenes para depuración
        if save_debug:
            image1.save(os.path.join(debug_dir, 'last_reference_image.png'))
            image2.save(os.path.join(debug_dir, 'last_debug_image.png'))

        diff = ImageChops.difference(image1, image2)
        stat = diff.getbbox()  # Obtener el cuadro delimitador de las diferencias

        if stat is None:
            print("No differences found. Combat is still active.")
            return False  # No hay diferencias
        else:
            print("Differences detected. Combat has ended or the scene has changed.")
            return True  # Hay diferencias
    except Exception as e:
        print(f"Error processing image difference: {e}")
        return True  # Si hay un error, suponer que el combate ha terminado por precaución