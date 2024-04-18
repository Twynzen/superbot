import os
import cv2
import pyautogui as pg

CHARACTER_IMAGES_DIR = os.path.join("ojoIA", "characters", "main_character", "Static")

def load_character_templates():
    templates = {}
    for filename in os.listdir(CHARACTER_IMAGES_DIR):
        path = os.path.join(CHARACTER_IMAGES_DIR, filename)
        template = cv2.imread(path, cv2.IMREAD_COLOR)
        direction = os.path.splitext(filename)[0]  # 'look_down', 'look_up', etc.
        templates[direction] = template
    return templates

def detect_character(frame, templates):
    match_threshold = 0.8  # Ejemplo de umbral, debería ser ajustado según las pruebas
    for direction, template in templates.items():
        result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > match_threshold:
            top_left = max_loc
            h, w = template.shape[:2]
            bottom_right = (top_left[0] + w, top_left[1] + h)
            center = (top_left[0] + w // 2, top_left[1] + h // 2)
            cv2.rectangle(frame, top_left, bottom_right, color=(0, 255, 0), thickness=2)
            return center  # Devuelve la posición central del personaje
    return None

def click_on_character(center):
    if center is not None:
        pg.click(center)
