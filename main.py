from modules.combat import searchMob, initiate_combat_sequence
from modules.resource_management import search_resources
from modules.image_processing import capture_map_coordinates, capture_current_game_frame
from modules.characters_tracking import load_character_templates, detect_character, click_on_character, track_and_click_character
from api.bot_controller import interpret_and_execute_gpt_response
from api.language_model import get_gpt_response
import inspect
import modules

def list_module_functions(module):
    functions_list = []
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj):
            functions_list.append(name)
    return functions_list

def explore_project():
    modules_list = [modules.combat, modules.resource_management, modules.characters_tracking]
    all_functions = {}
    for module in modules_list:
        module_name = module.__name__.split('.')[-1]
        all_functions[module_name] = list_module_functions(module)
    return all_functions

def main_menu():
    print("Seleccione una opción:")
    print("1. Recolectar recursos")
    print("2. Buscar mobs en la zona")
    print("3. Leer chat del juego (Funcionalidad en desarrollo)")
    print("4. Combate automático")
    print("5. Observa el entorno y obtiene datos")
    print("6. Interactuar con GPT-4")
    print("7. Explorar funciones del proyecto con GPT-4")
    
    choice = input("Introduce el número de la opción deseada: ")
    return choice

def interact_with_gpt4():
    user_prompt = input("Describe la misión o consulta para el personaje: ")
    gpt_response = get_gpt_response(user_prompt)
    print(f"GPT-4: {gpt_response}")
    interpret_and_execute_gpt_response(gpt_response)

def explore_with_gpt4():
    all_functions = explore_project()
    prompt = f"Estas son las funciones disponibles en el proyecto: {all_functions}. Sugiere acciones creativas que el bot pueda realizar utilizando estas funciones."
    gpt_response = get_gpt_response(prompt)
    print(f"GPT-4: {gpt_response}")
    interpret_and_execute_gpt_response(gpt_response)

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
        elif user_choice == '4':
            initiate_combat_sequence()
        elif user_choice == '5':
            track_and_click_character()
        elif user_choice == '6':
            interact_with_gpt4()
        elif user_choice == '7':
            explore_with_gpt4()
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    main()
