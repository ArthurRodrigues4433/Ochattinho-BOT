import json

PREFIXES = {}
LOG_CHANNELS = {}
MOD_ROLES = {}

def load_settings():
    global PREFIXES, LOG_CHANNELS, MOD_ROLES
    try:
        with open('settings.json', 'r') as f:
            data = json.load(f)
            PREFIXES = data.get('prefixes', {})
            LOG_CHANNELS = data.get('log_channels', {})
            MOD_ROLES = data.get('mod_roles', {})
        print("Settings carregados com sucesso.")
    except FileNotFoundError:
        print("Arquivo settings.json não encontrado, usando padrões.")
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar settings.json: {e}, usando padrões.")
        PREFIXES = {}
        LOG_CHANNELS = {}
        MOD_ROLES = {}

def save_settings():
    with open('settings.json', 'w') as f:
        json.dump({'prefixes': PREFIXES, 'log_channels': LOG_CHANNELS, 'mod_roles': MOD_ROLES}, f)

load_settings()