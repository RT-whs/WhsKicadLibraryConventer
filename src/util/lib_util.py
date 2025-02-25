from src.util.json_util import ConfigSingleton
import os

def load_existing_lib_patches():
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

def make_lib_base_structure(path,lib_name):
    
   
    full_path = os.path.join(path,  lib_name+'.pretty')
    os.makedirs(full_path)
    full_path = os.path.join(path,  lib_name+'.3dshapes')
    os.makedirs(full_path)

    file_path = os.path.join(path, lib_name + '.kicad_sym')
    with open(file_path, 'w') as file:
        pass  # no operation leave empty file

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
    
