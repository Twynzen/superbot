import pytesseract
# Configuración de la ruta de Tesseract-OCR
TESSERACT_CMD_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD_PATH

# Directorios para el manejo de recursos e imágenes
MAP_LOCATION_DIR = "mapLocation"
SCREENSHOTS_DIR = "ojoIA"
RESOURCES_DIR = "resources"
RESOURCES_TYPE =  {
    "trigo": "cereals",
    "castano": "wood",
    "fresno": "wood",
    "nogal": "wood",
    "hierro": "minerals",
    "ortiga": "herbage",
    "salvia": "herbage"
}
#region
REGION_TO_CAPTURE = (0, 65, 100 , 90-50) 



# Configuraciones de imágenes y navegación
IMAGE_OFFSET = 25
WAIT_TIME = 6
SCREENSHOT_SIZE = 100

DIRECTION_PATH_ABSTRUB_ZAAP = [
    'left', 'left', 'down', 'right', 'right', 'right', 'up', 'up', 'left', 'left',
    'left', 'down', 'left', 'left', 'down', 'right', 'down', 'left', 'right', 'right',
    'up', 'right', 'down', 'right', 'up','right','down','right','up','up', 'up','up', 'up',
    'left','down','left','up','left','down','left','up','left','left','down','right','down','left','down',
]

DIRECTION_PATH_ESCARAHOJA_ZAAP = [
    'right', 'right', 'up', 'up', 'right', 'up', 'up', 'right', 'down', 'down',
    'down', 'up', 'up', 'right', 'right', 'up', 'right', 'up', 'up', 'left',
    'up', 'right', 'up', 'left'
]

# Rutas a imágenes específicas de recursos
RESOURCE_PATHS = {
    "cereals": {
        "trigo": [
            "ojoIA/resources/cereals/trigo1.PNG",
            "ojoIA/resources/cereals/trigo2.PNG",
            "ojoIA/resources/cereals/trigo3.PNG",
            "ojoIA/resources/cereals/trigo4.PNG",
            "ojoIA/resources/cereals/trigo5.PNG"
        ]
    },
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
        ]
    },
    "minerals": {
        "hierro": [
            "ojoIA/resources/minerals/hierro1.PNG",
            "ojoIA/resources/minerals/hierro2.PNG",
            "ojoIA/resources/minerals/hierro3.PNG",
            "ojoIA/resources/minerals/hierro4.PNG",
            "ojoIA/resources/minerals/hierro5.PNG"
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
        ]
    }
}


# Regiones de captura de pantalla para detectar tooltips y otros indicadores
TOOLTIP_REGIONS = {
    'up': (960 - 50, 0, 100, 50),
    'left': (0 + 300, 540 - 25, 100, 50),
    'right': (1920 - 400, 540 - 25, 100, 50),
    'down': (960 - 50, 1080 - 200, 100, 50),
}
#Combat 
COMBAT_MODE_REGION = (1310, 995, 165, 45) 


CONFIDENCE_LEVEL = 0.7
