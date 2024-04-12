# Configuración de la ruta de Tesseract-OCR
TESSERACT_CMD_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Directorios para el manejo de recursos e imágenes
MAP_LOCATION_DIR = "mapLocation"
SCREENSHOTS_DIR = "ojoIA"
RESOURCES_DIR = "resources"

# Configuraciones de imágenes y navegación
IMAGE_OFFSET = 25
WAIT_TIME = 8
SCREENSHOT_SIZE = 100
DIRECTIONS = [
    'right', 'right', 'up', 'up', 'right', 'up', 'up', 'right', 'down', 'down',
    'down', 'up', 'up', 'right', 'right', 'up', 'right', 'up', 'up', 'left',
    'up', 'right', 'up', 'left'
]

# Rutas a imágenes específicas de recursos
RESOURCE_PATHS = {
    "trigo": ["ojoIA/trigo1.PNG", "ojoIA/trigo2.PNG", "ojoIA/trigo3.PNG", "ojoIA/trigo4.PNG", "ojoIA/trigo5.PNG"],
    "ojoIA/fresno": ["ojoIA/fresno1.PNG", "ojoIA/fresno2.PNG", "ojoIA/fresno3.PNG"],
    "ojoIA/castano": ["ojoIA/casta1.PNG", "ojoIA/casta2.PNG", "ojoIA/casta3.PNG", "ojoIA/casta4.PNG"],
    "ojoIA/ortiga": ["ojoIA/ortiga1.PNG", "ojoIA/ortiga2.PNG", "ojoIA/ortiga3.PNG", "ojoIA/ortiga4.PNG", "ojoIA/ortiga5.PNG"],
    "ojoIA/salvia": ["ojoIA/salvia1.PNG", "ojoIA/salvia2.PNG"],
    "ojoIA/nogal": ["ojoIA/nogal1.PNG", "ojoIA/nogal2.PNG", "ojoIA/nogal3.PNG"],
    "ojoIA/hierro": ["ojoIA/hierro1.PNG", "ojoIA/hierro2.PNG", "ojoIA/hierro3.PNG", "ojoIA/hierro4.PNG", "ojoIA/hierro5.PNG"]   
}

# Regiones de captura de pantalla para detectar tooltips y otros indicadores
TOOLTIP_REGIONS = {
    'up': (960 - 50, 0, 100, 50),
    'left': (0 + 300, 540 - 25, 100, 50),
    'right': (1920 - 400, 540 - 25, 100, 50),
    'down': (960 - 50, 1080 - 200, 100, 50),
}
#Combat 
COMBAT_MODE_REGION = (1310, 930, 165, 75) 


CONFIDENCE_LEVEL = 0.7
