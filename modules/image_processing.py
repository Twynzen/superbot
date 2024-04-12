import pyautogui as pg
from PIL import Image, ImageChops
import pytesseract
from config import SCREENSHOTS_DIR, TESSERACT_CMD_PATH

# Configura la ubicación de Tesseract en tu sistema
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD_PATH

def capture_screenshot(region, filename):
    """Toma una captura de pantalla de la región especificada y guarda la imagen."""
    screenshot = pg.screenshot(region=region)
    screenshot_path = f"{SCREENSHOTS_DIR}/{filename}"
    screenshot.save(screenshot_path)
    return screenshot_path

def compare_screenshots(screenshot1_path, screenshot2_path):
    """Compara dos capturas de pantalla para ver si son idénticas."""
    img1 = Image.open(screenshot1_path)
    img2 = Image.open(screenshot2_path)
    return ImageChops.difference(img1, img2).getbbox() is None

def process_image_for_text(image_path):
    """Utiliza OCR para extraer texto de una imagen."""
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

def capture_and_process_image(region):
    """Combina la captura de pantalla y el procesamiento de OCR."""
    screenshot_path = capture_screenshot(region, 'temp.png')
    text = process_image_for_text(screenshot_path)
    return text

def get_image_difference(image1_path, image2_path):
    """Obtiene la diferencia entre dos imágenes."""
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)
    return ImageChops.difference(img1, img2)
