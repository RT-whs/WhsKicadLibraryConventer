import time
import threading
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.dataextractor.dataextractor import extract_data  # Importujeme extract_data správně z modulu dataextractor

# Načteme čas poslední změny pro každý soubor
last_modified_time = {}
lock = threading.Lock()

# Funkce pro zpracování souboru po uplynutí 5 sekund
def process_file(file_path):
    """Zpracuje soubor po uplynutí 5 sekund od poslední změny."""
    print(f"Processing file: {file_path}")
    extract_data(file_path)

# Funkce pro zpracování změn souborů
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        """Tato funkce se spustí při změně souboru."""
        if event.is_directory:
            return  # Ignorujeme změny adresářů

        file_path = event.src_path
        # Získání přípony
        extension = os.path.splitext(file_path)[1]
        if extension == ".kicad_sym":
            print(f"File modified: {file_path}")
            handle_file_change(file_path)
        else:
            print(f"File modified: {file_path} skipped") 

# Funkce pro zpracování změn souboru
def handle_file_change(file_path):
    """Zpracuje změnu souboru, pokud uplynulo 5 sekund od poslední změny."""
    global last_modified_time
    
    # Získáme aktuální čas změny
    current_time = time.time()

    with lock:
        # Pokud uplynulo méně než 5 sekund od poslední změny, neprovádíme akce
        if file_path in last_modified_time:
            time_diff = current_time - last_modified_time[file_path]
            if time_diff < 5:
                print(f"Waiting for 5 seconds before processing {file_path}")
                last_modified_time[file_path] = current_time
                return  # Nezpracováváme, čekáme na 5 sekund
        # Aktualizujeme čas poslední změny
        last_modified_time[file_path] = current_time

    # Spustíme odpočet a zpracování souboru
    threading.Thread(target=start_countdown_and_process, args=[file_path]).start()

# Funkce pro odpočet a následné zpracování souboru
def start_countdown_and_process(file_path):
    """Provádí odpočet 2 sekund a následně zpracuje soubor."""
    for i in range(2, 0, -1):
        print(f"Waiting {i} seconds before processing {file_path}...", end="\r")
        time.sleep(1)

    # Po odpočtu zpracujeme soubor
    print(f"\nProcessing file after 2 seconds: {file_path}")
    process_file(file_path)

# Funkce pro spuštění monitorování změn v adresáři
def start_monitoring(watched_folder):
    """Spustí sledování změn v adresáři pomocí watchdog."""
    print(f"Monitoring changes in {watched_folder}...")
    
    # Vytvoření obsluhy událostí pro sledování změn souborů
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=watched_folder, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)  # Udržuje program aktivní pro monitorování
    except KeyboardInterrupt:
        observer.stop()  # Pokud uživatel přeruší program, zastavíme observer
    observer.join()
