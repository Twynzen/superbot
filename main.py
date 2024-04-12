from modules.combat import is_in_combat_mode
from modules.navigation import change_map
from modules.resource_management import search_and_collect_resources
import logging
from config import WAIT_TIME
import time


def main():
    while True:  # Bucle principal del bot.
        if is_in_combat_mode():
            # Aquí podrías incluir acciones adicionales en caso de combate.
            print("Modo combate detectado. Esperando hasta que termine...")
            time.sleep(WAIT_TIME)  # Espera a que termine el combate.
            continue  # Continúa el bucle principal.

        # Intenta recolectar recursos.
        resources_collected = search_and_collect_resources()
        if resources_collected:
            print("Recolectando recursos...")
            continue  # Si se recolectaron recursos, vuelve a empezar el ciclo.

        # Si no se recolectaron recursos, intenta cambiar de mapa.
        print("Intentando cambiar de mapa para encontrar más recursos...")
        map_changed = change_map()
        if not map_changed:
            print("No se pudo cambiar de mapa. Reintentando...")
            continue  # Si falla el cambio de mapa, reintenta el ciclo.

        # Espera un momento antes de volver a empezar el ciclo.
        time.sleep(WAIT_TIME)

if __name__ == "__main__":
    print("Iniciando el bot...")
    main()
