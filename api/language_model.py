from openai import OpenAI  # Asegúrate de que estás importando OpenAI correctamente
import env  # Asumiendo que tienes un archivo env con tu clave API

# Inicializa el cliente con la clave API
client = OpenAI(api_key=env.API_KEY)

def get_gpt_response(prompt):
    # Usa el cliente para crear una respuesta de chat con el modelo GPT-4 Turbo
    completion = client.completions.create(
        model='gpt-4-turbo',
        prompt=[
            {"role": "system", "content": "You are a character in a role-playing game."},
            {"role": "user", "content": prompt}
        ]
    )
    # Retorna solo el contenido del mensaje de la respuesta
    return completion.choices[0].message.content.strip()

