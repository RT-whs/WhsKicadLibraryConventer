import os
from src.events.eventReceiver import EventReceiver
from src.util.json_util import ConfigSingleton

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
        self.Static.make_lib_base_structure(library_path, library_name)
        #add library to kicad definition
        self.Static.save_new_lib_to_kicad_settings(library_path, library_name)
        #update structure
        return self.Static.get_existing_libs()

    class Static:
        @staticmethod
        def get_existing_libs():
            config = ConfigSingleton()
            #get library
            whs_lib_path = config.get('library_final_folder')  # return value from json

            kicad_files = []

            # Walking throw dir tree
            for root, dirs, files in os.walk(whs_lib_path):
                # Omit base path
                if root == whs_lib_path:
                    continue
                
                # Each file check extension
                for file in files:
                    if file.endswith(".kicad_sym"):
                        # add full path to list                 
                        relative_path = os.path.relpath(os.path.join(root, file), start=whs_lib_path)
                        kicad_files.append(os.path.normpath(relative_path))


            return kicad_files
        
        
        @staticmethod
        def make_lib_base_structure(path,lib_name):   
            full_path = os.path.join(path,  lib_name+'.pretty')
            os.makedirs(full_path)
            full_path = os.path.join(path,  lib_name+'.3dshapes')
            os.makedirs(full_path)
            file_path = os.path.join(path, lib_name + '.kicad_sym')
            source_file_path = os.path.join(ConfigSingleton._instance.get('library_root_folder'), 'template', 'template_symbol_emtpy_lib.kicad_sym' )
            with open(file_path, 'w') as destinationFile, open( source_file_path , 'r') as sourceFile:
                destinationFile.write(sourceFile.read())
        

        @staticmethod
        def save_new_lib_to_kicad_settings(library_path, library_name):
            config = ConfigSingleton()
            library_desc_file = config.get('symbol_lib_file')
            with open(library_desc_file, "r", encoding="utf-8") as file:
                sym_lib_table = file.read() 

            #find last )
            last_index = sym_lib_table.rfind(')')
            last_index = sym_lib_table.rfind('\n', 0, last_index)
            #put newline before
            if last_index != -1:
                # Rozdělení obsahu na dvě části
                before = sym_lib_table[:last_index]
                after = sym_lib_table[last_index:]

                # Vlož novou řádku před poslední ')'
                lib_path = os.path.join(library_path,library_name)
                updated_content = before + f'  (lib (name \"{library_name}\")(type \"KiCad\")(uri \"{lib_path}")(options \"\")(descr \"Whs lib for {library_name}\"))' +'\n' + after
                #insert (lib (name "_libname_")(type "KiCad")(uri "_path/to/*.kicad_sym")(options "")(descr "Whs lib for _libname_"))

                #file save
                with open(library_desc_file, "w", encoding="utf-8") as file:
                    file.write(updated_content)
            else:
                raise Exception("Corrupted sym_lib_table, cannot write there")

