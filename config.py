import pytesseract
import os

GAME_SCREEN_REGION = {"top": 0, "left": 0, "width": 1920, "height": 580}

# Configuración de la ruta de Tesseract-OCR
TESSERACT_CMD_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD_PATH

# Directorios para el manejo de recursos e imágenes
MAP_LOCATION_DIR = "mapLocation"
SCREENSHOTS_DIR = "ojoIA"
RESOURCES_DIR = "resources"
ZAAP_IMAGES_DIR = os.path.join(SCREENSHOTS_DIR, 'zaaps')
# Nivel de confianza para la detección de imágenes
CONFIDENCE_LEVEL = 0.7

# Configuraciones de imágenes y navegación
IMAGE_OFFSET = 25
WAIT_TIME = 4
SCREENSHOT_SIZE = 100




MOVEMENTS_TO_PHOENIX_SKELETON = ["right", "right", "right", "right", "up", "up", "up", "up", "left"]

MOVEMENTS_TO_PHOENIX_STROPAJO = ["right", "right", "right", "right", "up",  "right"]
PHOENIX_ROUTES = {
    "9,16": {
        "movements": MOVEMENTS_TO_PHOENIX_SKELETON,  # Ejemplo de movimientos
        "phoenix_button_x": 620,
        "phoenix_button_y": 250
    },
    "-3,-13": {
        "movements": MOVEMENTS_TO_PHOENIX_STROPAJO,
        "phoenix_button_x": 820,
        "phoenix_button_y": 550
    }
}
# Rutas de Zaaps
ZAAPS = [
    "25,-4", "27,-14", "1,-32", "10,22", "13,26", "-31,-56", "-26,37", "-78,-41",
    "35,12", "-46,18", "-1,13", "-1,24", "7,-4", "5,-18", "-27,-36", "3,-5", "-5,-8",
    "-2,0", "39,-82", "20,29", "-25,12", "-20,-20", "-3,-42", "-5,-23", "-17,-47",
    "-34,8", "0,-56", "-13,28", "-16,1"
]
# Tipos de recursos y sus categorías
RESOURCES_TYPE = {
    "trigo": "cereals",
    "cebada": "cereals",
    "avena": "cereals",
    "castano": "wood",
    "roble": "wood",
    "fresno": "wood",
    "nogal": "wood",
    "hierro": "minerals",
    "ortiga": "herbage",
    "salvia": "herbage",
    "trebol": "herbage"
}

# Rutas a imágenes específicas de recursos
RESOURCE_PATHS = {
    "cereals": {
        "trigo": [
            "ojoIA/resources/cereals/trigo1.PNG",
            "ojoIA/resources/cereals/trigo2.PNG",
            "ojoIA/resources/cereals/trigo3.PNG",
            "ojoIA/resources/cereals/trigo4.PNG",
            "ojoIA/resources/cereals/trigo5.PNG"
        ],
        "cebada": [
            "ojoIA/resources/cereals/cebada1.PNG",
            "ojoIA/resources/cereals/cebada2.PNG"
        ],
        "avena": [
            "ojoIA/resources/cereals/avena1.PNG"
        ]
    },
       #"minerals": {
    #    "hierro": [
    #        "ojoIA/resources/minerals/hierro1.PNG",
    #        "ojoIA/resources/minerals/hierro2.PNG",
    #        "ojoIA/resources/minerals/hierro3.PNG",
    #        "ojoIA/resources/minerals/hierro4.PNG",
    #        "ojoIA/resources/minerals/hierro5.PNG"
    #    ]
    # }
    
    "wood": {
        "castano": [
            "ojoIA/resources/wood/casta1.PNG",
            "ojoIA/resources/wood/casta2.PNG",
            "ojoIA/resources/wood/casta3.PNG",
            "ojoIA/resources/wood/casta4.PNG"
        ],
        "fresno": [
            "ojoIA/resources/wood/fresno1.PNG",
            "ojoIA/resources/wood/fresno2.PNG",
            "ojoIA/resources/wood/fresno3.PNG"
        ],
        "nogal": [
            "ojoIA/resources/wood/nogal1.PNG",
            "ojoIA/resources/wood/nogal2.PNG",
            "ojoIA/resources/wood/nogal3.PNG"
        ],
        "roble": [
            "ojoIA/resources/wood/roble1.PNG",
            "ojoIA/resources/wood/roble2.PNG"
        ]
    },
    "herbage": {
        "ortiga": [
            "ojoIA/resources/herbage/ortiga1.PNG",
            "ojoIA/resources/herbage/ortiga2.PNG",
            "ojoIA/resources/herbage/ortiga3.PNG",
            "ojoIA/resources/herbage/ortiga4.PNG",
            "ojoIA/resources/herbage/ortiga5.PNG"
        ],
        "salvia": [
            "ojoIA/resources/herbage/salvia1.PNG",
            "ojoIA/resources/herbage/salvia2.PNG"
        ],
        "trebol": [
            "ojoIA/resources/herbage/trebol1.PNG",
            "ojoIA/resources/herbage/trebol2.PNG"
        ]
    }
}

# Regiones de captura de pantalla para detectar tooltips y otros indicadores
TOOLTIP_REGIONS = {
    'up': (960 - 50, 0, 100, 50),
    'left': (0 + 300, 540 - 25, 100, 50),
    'right': (1920 - 400, 540 - 25, 100, 50),
    'down': (960 - 50, 1080 - 200, 100, 50)
}

# Configuraciones de combate
COMBAT_MODE_REGION = (1610, 95, 155, 875)  # Conserva para operaciones de hover
BOARD_REGION = (300, 25, 1300, 900)

# Datos del personaje
PLAYER_NAME = 'Twenzen'
PLAYER_DATA_REGION = (715, 900, 120, 140)

# Directorio para guardar capturas de pantalla
SCREENSHOT_DIR = os.path.join("ojoIA", "screenshots")

# Nivel de confianza para la detección de imágenes
CONFIDENCE_LEVEL = 0.7

# Definición de las rutas para direcciones específicas
DIRECTION_PATH_ABSTRUB_ZAAP = [
    'left', 'left', 'down', 'right', 'right', 'right', 'up', 'up', 'left', 'left',
    'left', 'down', 'left', 'left', 'down', 'right', 'down', 'left', 'right', 'right',
    'up', 'right', 'down', 'right', 'up', 'right', 'down', 'right', 'up', 'up', 'up', 'up', 'up',
    'left', 'down', 'left', 'up', 'left', 'down', 'left', 'up', 'left', 'left', 'down', 'right', 'down', 'left', 'down'
]
DIRECTION_PATH_ESCARAHOJA_ZAAP = [
    'right', 'right', 'up', 'up', 'right', 'up', 'up', 'right', 'down', 'down',
    'down', 'up', 'up', 'right', 'right', 'up', 'right', 'up', 'up', 'left',
    'up', 'right', 'up', 'left', 'up', 'up', 'right', 'right', 'down', 'left', 'left', 'left', 'left'
]
DIRECTION_PATH_ROBLE = [
    'right', 'up', 'right', 'down', 'right', 'up',
    'up', 'up', 'up', 'up', 'right', 'up', 'left', 'up',
    'right', 'up', 'left', 'up', 'left', 'left',
    'left', 'left', 'left', 'left', 'left', 'down', 'down', 'left',
    'down', 'right', 'down', 'down', 'down', 'right', 'right', 'down', 'down', 'down', 'right'
]
DIRECTION_PATH_TREBOL = [
    'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down', 'down',
    'right', 'right', 'right', 'right', 'up', 'right', 'right'
]

# Región de detección de zaaps (toda la pantalla)
ZAAP_DETECTION_REGION = (0, 0, 1920, 1080)

# Región de la interfaz de zaaps y botón de teletransportarse
ZAAP_INTERFACE_REGION = (600, 200, 700, 600)  # Ajusta según sea necesario
TELEPORT_BUTTON_REGION = (860, 750, 200, 50)  # Ajusta según sea necesario

ZAAP_LOCATIONS = [
    {"nombre": "Isla Zanahowia", "coordenadas": "25,-4", "región": "Archipiélago Wabbit"},
    {"nombre": "Laboratorios abandonados", "coordenadas": "27,-14", "región": "Archipiélago Wabbit"},
    {"nombre": "Tainela", "coordenadas": "1,-32", "región": "Astrub"},
    {"nombre": "Ribera del golfo sufokeño", "coordenadas": "10,22", "región": "Bahía de Sufokia"},
    {"nombre": "Sufokia", "coordenadas": "13,26", "región": "Bahía de Sufokia"},
    {"nombre": "Corazón Inmaculado", "coordenadas": "-31,-56", "región": "Bonta"},
    {"nombre": "Coraza", "coordenadas": "-26,37", "región": "Brakmar"},
    {"nombre": "Burgo", "coordenadas": "-78,-41", "región": "Isla de Frigost"},
    {"nombre": "Playa Tortuga", "coordenadas": "35,12", "región": "Isla de Moon"},
    {"nombre": "Pueblo costero", "coordenadas": "-46,18", "región": "Isla de Otomai"},
    {"nombre": "Linde del Bosque Maléfico", "coordenadas": "-1,13", "región": "Amakna"},
    {"nombre": "Llanura de los escarahojas", "coordenadas": "-1,24", "región": "Amakna"},
    {"nombre": "Puerto de Madrestam", "coordenadas": "7,-4", "región": "Amakna"},
    {"nombre": "Ciudad de Astrub", "coordenadas": "5,-18", "región": "Astrub"},
    {"nombre": "Campos de Cania", "coordenadas": "-27,-36", "región": "Llanuras de Cania"},
    {"nombre": "Castillo de Amakna", "coordenadas": "3,-5", "región": "Amakna"},
    {"nombre": "La montaña de los crujidores", "coordenadas": "-5,-8", "región": "Amakna"},
    {"nombre": "Pueblo de Amakna", "coordenadas": "-2,0", "región": "Amakna"},
    {"nombre": "Arboleda nevada", "coordenadas": "39,-82", "región": "Archipiélago de Valonia"},
    {"nombre": "Pueblo de Pandala", "coordenadas": "20,29", "región": "Isla de Pandala"},
    {"nombre": "Camino de las caravanas", "coordenadas": "-25,12", "región": "Landas de Sidimote"},
    {"nombre": "Caminos rocosos", "coordenadas": "-20,-20", "región": "Llanuras de Cania"},
    {"nombre": "Lago de Cania", "coordenadas": "-3,-42", "región": "Llanuras de Cania"},
    {"nombre": "Llanura de los puerkazos", "coordenadas": "-5,-23", "región": "Llanuras de Cania"},
    {"nombre": "Llanuras Rocosas", "coordenadas": "-17,-47", "región": "Llanuras de Cania"},
    {"nombre": "Pueblo de los dopeuls", "coordenadas": "-34,8", "región": "Llanuras de Cania"},
    {"nombre": "Pueblo de los kanigs", "coordenadas": "0,-56", "región": "Llanuras de Cania"},
    {"nombre": "Sierra de Cania", "coordenadas": "-13,28", "región": "Llanuras de Cania"},
    {"nombre": "Pueblo de los ganaderos", "coordenadas": "-16,1", "región": "Montaña de los Koalaks"}
]

PREDEFINED_POSITIONS = {
    "5,-18": DIRECTION_PATH_ABSTRUB_ZAAP,
    "-1,24": DIRECTION_PATH_ESCARAHOJA_ZAAP,
    "-11,-8": DIRECTION_PATH_ROBLE,
    "3,21": DIRECTION_PATH_TREBOL
}
