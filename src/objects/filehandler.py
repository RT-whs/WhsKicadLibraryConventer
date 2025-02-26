from src.events.eventReceiver import EventReceiver
from blinker import Signal
from src.util.lib_util import load_existing_lib_patches, make_lib_base_structure,save_new_lib_to_kicad_settings

class FileHandlerKicad:
    _instance = None  # Statická proměnná pro uchování instance

    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super(FileHandlerKicad, cls).__new__(cls)            
        return cls._instance

    def registerEventReceiverCreateLibrary(self, signal_lib_create):
        self.receiver_lib_create = EventReceiver(signal_lib_create, self.event_lib_create)
    
    def unregisterEventSaveCmd(self):
        self.receiver_lib_create.disconnect()

    def event_lib_create(self, sender, **kwargs):
        library_path = kwargs.get("library_path", "N/A")
        library_name = kwargs.get("library_name", "N/A")

        print(f"EventReceiver: Received event from {sender}")
        print(f"Library Path: {library_path}")
        print(f"Library Name: {library_name}")
         
         #create folders
        #make_lib_base_structure(library_path, library_name)
        #add library to kicad definition
        #save_new_lib_to_kicad_settings(library_path, library_name)
        #update structure
