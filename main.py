from modules.combat import  searchMob
from modules.resource_management import search_resources
from modules.image_processing import capture_map_coordinates

def main_menu():
    print("Seleccione una opción:")
    print("1. Recolectar recursos")
    print("2. Buscar mobs en la zona (Funcionalidad en desarrollo)")
    print("3. Leer chat del juego (Funcionalidad en desarrollo)")
    print("3. Combate automatico (Funcionalidad en desarrollo)")
    
    choice = input("Introduce el número de la opción deseada: ")
    return choice


        

def main():
    print("Iniciando el bot...")
    initial_coordinates = capture_map_coordinates()
    if initial_coordinates:
        print(f"Coordenadas iniciales del mapa al iniciar: {initial_coordinates}")
    else:
        print("No se pudieron capturar las coordenadas iniciales del mapa.")
    
    while True:
        user_choice = main_menu()
        
        if user_choice == '1':
            while True:
                search_resources()
            

        elif user_choice == '2':
           while True:
               searchMob()
        
        elif user_choice == '3':
            print("Esta funcionalidad aún está en desarrollo.")
            # Aquí iría la lógica para leer el chat del juego.
            # Ejemplo: read_game_chat()
        
        elif user_choice == '4':
            print("Esta funcionalidad aún está en desarrollo.")
            # Aquí iría la lógica para combate
            # Ejemplo: read_game_chat() IR AL BANCO

        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    main()
