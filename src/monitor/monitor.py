import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
    def __init__(self, directory_to_watch, callback):
        self.directory_to_watch = directory_to_watch
        self.callback = callback
        self.event_handler = FileSystemEventHandler()
        self.event_handler.on_modified = self.on_modified

    def on_modified(self, event):
        """Akce, která se vykoná, když je soubor změněn."""
        if event.is_directory:
            return
        print(f"File modified: {event.src_path}")
        self.callback(event.src_path)  # Zavolání callbacku pro zpracování změny

    def start(self):
        """Spustí sledování složky."""
        observer = Observer()
        observer.schedule(self.event_handler, self.directory_to_watch, recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)  # Udržuje program běžící
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

def start_monitoring(directory_to_watch, callback):
    watcher = Watcher(directory_to_watch, callback)
    watcher.start()
