import os
from pathlib import Path
from pathlib import PurePath
from src.events.eventReceiver import EventReceiver
from src.util.json_util import ConfigSingleton
import shutil


class FileHandlerKicad:
    _instance = None  # Static variable

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
        #add sym library to kicad definition
        self.Static.save_new_lib_to_kicad_settings(library_path, library_name)
        #add footprint library to kicad definition
        self.Static.save_new_footprint_lib_folder_to_kicad_settings(library_path, library_name)
        #update structure
        return self.Static.get_existing_libs()

    
    class Static:
        @staticmethod
        def get_footprint_file_content_from_watched_folder(file_name_without_suffix:str):
            watched_folder_filepath = Path( ConfigSingleton._instance.get( 'watched_folder'), 'SamacSys_Parts.pretty', file_name_without_suffix + ".kicad_mod")
            with open(watched_folder_filepath, "r", encoding="utf-8") as file:
                footprint_file = file.read() 
                return footprint_file, watched_folder_filepath

        
        @staticmethod
        def move_file(source: str, destination: str):
            """
            Move file from 'source' to 'destination'.
            If destination path missing create it
            """
            try:
                shutil.move(source, destination)
                #print(f"Soubor přesunut z {source} do {destination}")
            except Exception as e:
                raise MemoryError(f"Error move file: {e}")

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
            source_file_path = os.path.join(ConfigSingleton._instance.get('library_root_folder'), 'template', 'template_symbol_empty_lib.kicad_sym' )
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
                # Split content
                before = sym_lib_table[:last_index]
                after = sym_lib_table[last_index:]

                # Add new line before last ')'
                lib_path = os.path.join(library_path,library_name+".kicad_sym")
                #rename absolute path to defined symbol name
                lib_path = FileHandlerKicad.Static.get_lib_path_with_symbol_variable(lib_path)
                updated_content = before + f'  (lib (name \"{library_name}\")(type \"KiCad\")(uri \"{lib_path}")(options \"\")(descr \"Whs lib for {library_name}\"))' +'\n' + after
               

                #file save
                with open(library_desc_file, "w", encoding="utf-8") as file:
                    file.write(updated_content)
            else:
                raise Exception("Corrupted sym_lib_table, cannot write there")


        @staticmethod
        def save_new_footprint_lib_folder_to_kicad_settings(library_path, library_name,configFile="default"):
            #  (lib (name Varistor)(type KiCad)(uri ${KICAD9_FOOTPRINT_DIR}/Varistor.pretty)(options "")(descr "Varistor"))

            config = ConfigSingleton()
                     
            library_desc_file = config.get('footprint_lib_file') if configFile=="default" else configFile            
            with open( Path( library_desc_file), "r", encoding="utf-8") as file:
                sym_lib_table = file.read() 

            #find last )
            last_index = sym_lib_table.rfind(')')
            last_index = sym_lib_table.rfind('\n', 0, last_index)
            #put newline before
            if last_index != -1:
                # Split content
                before = sym_lib_table[:last_index]
                after = sym_lib_table[last_index:]

                # Add new line before last ')'
                lib_path = os.path.join(library_path,library_name+".pretty")
                #rename absolute path to defined symbol name
                lib_path = FileHandlerKicad.Static.get_lib_path_with_symbol_variable(lib_path)
                updated_content = before +'\n' + f'  (lib (name \"{library_name}\")(type \"KiCad\")(uri \"{lib_path}")(options \"\")(descr \"Whs footprint lib for {library_name}\"))'  + after
                #insert (lib (name "_libname_")(type "KiCad")(uri "_path/to/*.kicad_sym")(options "")(descr "Whs lib for _libname_"))

                #file save
                with open(library_desc_file, "w", encoding="utf-8") as file:
                    file.write(updated_content)
            else:
                raise Exception("Corrupted sym_lib_table, cannot write there")

        @staticmethod
        def get_lib_path_with_symbol_variable(library_path):
            config = ConfigSingleton()
            _lib_final_folder = PurePath(os.path.normpath(config.get('library_final_folder')))
            _lib_final_folder_symbol = PurePath(os.path.normpath(config.get('library_final_folder_path_symbol_name')))
            _parameter = PurePath(library_path.encode('unicode_escape').decode())                      
            _result =  str( _parameter).replace( str( _lib_final_folder), str( _lib_final_folder_symbol)) 
            _result = str( _result).replace('\\','/')             
            return _result


        @staticmethod
        def fix_path(path_str: str) -> str:
            """ Repair special characters and normalize it. """
            return path_str.encode("unicode_escape").decode("utf-8")
          
