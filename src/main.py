import json
import os
from monitor.monitor import start_monitoring
from dataextractor.dataextractor import extract_data  # Importujeme novou funkci

def load_config():
    """Načte konfiguraci ze souboru config.json."""
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config

import time

# Uchováme čas poslední změny souboru
last_modified_time = {}

def file_changed(file_path):
    """Callback funkce pro zpracování změn souborů."""
    global last_modified_time
    
    # Získáme aktuální čas změny
    current_time = time.time()
    
    # Zkontrolujeme, zda uplynul dostatečný čas od poslední změny
    if file_path in last_modified_time:
        time_diff = current_time - last_modified_time[file_path]
        if time_diff < 1:  # Pokud uplynulo méně než 1 sekunda od poslední změny, ignorujeme
            print(f"Skipping file {file_path} due to rapid changes.")
            return  # Přeskočíme další zpracování

    # Zpracujeme soubor
    print(f"Processing file: {file_path}")
    extract_data(file_path)

    # Uložíme čas poslední změny
    last_modified_time[file_path] = current_time

if __name__ == "__main__":
    # Načte nastavení z config.json
    config = load_config()
    directory_to_watch = config.get('watched_folder', './watched_folder')  # Výchozí hodnota pokud není uvedeno

    # Kontrola, zda složka existuje
    if not os.path.exists(directory_to_watch):
        print(f"Error: The watched folder '{directory_to_watch}' does not exist!")
    else:
        print(f"Monitoring changes in {directory_to_watch}...")
        start_monitoring(directory_to_watch, file_changed)
