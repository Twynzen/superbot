from api.language_model import get_gpt_response
from modules.resource_management import search_resources
from modules.combat import searchMob
from modules.characters_tracking import click_on_character

def execute_action(action):
    if action == 'collect_resources':
        search_resources()
    elif action == 'search_mob':
        searchMob()
    elif action == 'track_character':
        click_on_character()
    else:
        print("Acción no reconocida.")

def interpret_and_execute_gpt_response(gpt_response):
    action = parse_gpt_response_to_action(gpt_response)
    execute_action(action)

def parse_gpt_response_to_action(gpt_response):
    if 'recoge recursos' in gpt_response:
        return 'collect_resources'
    elif 'busca mobs' in gpt_response:
        return 'search_mob'
    elif 'rastrea personaje' in gpt_response:
        return 'track_character'
    else:
        return 'unknown_action'
