import sys
import os


# Nastavení cesty k projektovému kořenu
def add_project_root_to_sys_path():
    """Přidá kořenovou složku projektu do sys.path, pokud tam ještě není."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))

    if project_root not in sys.path:
        sys.path.append(project_root)


add_project_root_to_sys_path()
# Import modulu pro monitoring
from monitor.monitor import start_monitoring
# Hlavní program
from src.util.json_util import ConfigSingleton


def main():
    """Spustí monitoring, pokud je v konfiguraci zadána sledovaná složka."""
    config = ConfigSingleton()
    try:
        watched_folder = config.get("watched_folder", raise_error=True)
    except KeyError as e:
        print(f"Chyba: {e}")

    if watched_folder:
        start_monitoring(watched_folder)
    else:
        print("Nebyla zadána žádná sledovaná složka v konfiguraci.")


if __name__ == "__main__":
    main()
