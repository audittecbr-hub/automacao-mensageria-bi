from dotenv import load_dotenv
import os

load_dotenv('../agente/.env')
evo_url = os.getenv('EVOLUTION_API_URL')
evo_key = os.getenv('EVOLUTION_API_TOKEN')
evo_instance = os.getenv('EVOLUTION_INSTANCE_NAME')

with open('.env', 'a') as f:
    f.write(f'\nEVOLUTION_SERVER_URL={evo_url}\nEVOLUTION_API_KEY={evo_key}\nEVOLUTION_INSTANCE_NAME={evo_instance}\n')
