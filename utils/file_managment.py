import os
from config import MAP_LOCATION_DIR

def save_data_to_file(data, filename):
    """Guarda datos en un archivo específico."""
    with open(os.path.join(MAP_LOCATION_DIR, filename), 'w') as file:
        # Aquí iría la lógica para escribir datos en el archivo.
        pass

def read_data_from_file(filename):
    """Lee datos de un archivo."""
    with open(os.path.join(MAP_LOCATION_DIR, filename), 'r') as file:
        # Aquí iría la lógica para leer datos del archivo.
        pass
