import json
import sys
import os

# Přidáme kořenovou složku projektu do sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from monitor.monitor import start_monitoring  
# Importujeme start_monitoring z modulu monitor

# Načteme cestu k adresáři z config.json
def load_config():
    """Načte konfiguraci z JSON souboru."""
    try:
        with open('config.json', 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
            return config.get("watched_folder", "")  # Vrátí cestu k adresáři nebo prázdný řetězec
    except Exception as e:
        print(f"Error loading config: {e}")
        return ""

# Hlavní program
if __name__ == "__main__":
    watched_folder = load_config()  # Načteme cestu z config.json
    if watched_folder:
        start_monitoring(watched_folder)
    else:
        print("No watched folder specified in config.")
