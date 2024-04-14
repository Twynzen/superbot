from modules.combat import check_combat_status
from modules.navigation import change_map
from modules.resource_management import search_and_collect_resources
from modules.image_processing import capture_map_coordinates
from config import WAIT_TIME
import time

def main():
    print("Iniciando el bot...")
    initial_coordinates = capture_map_coordinates()
    if initial_coordinates:
        print(f"Coordenadas iniciales del mapa al iniciar: {initial_coordinates}")
    else:
        print("No se pudieron capturar las coordenadas iniciales del mapa.")

    while True:
        resources_collected = search_and_collect_resources()

        if not resources_collected:
            print("No se encontraron recursos. Intentando cambiar de mapa...")
            coordinates_before_change = capture_map_coordinates()
            print(f"Coordenadas antes de cambiar de mapa: {coordinates_before_change}")

            change_map()
            time.sleep(WAIT_TIME)  # Espera después de intentar cambiar de mapa.

            coordinates_after_change = capture_map_coordinates()
            print(f"Coordenadas después de intentar cambiar de mapa: {coordinates_after_change}")

            if coordinates_before_change == coordinates_after_change:
                print("No se detectaron cambios en la posición del mapa. Verificando modo de combate...")
                check_combat_status()  # Verifica continuamente si está en combate
            else:
                print("El cambio de mapa fue exitoso.")

        time.sleep(2)

if __name__ == "__main__":
    main()
