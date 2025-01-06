import json
import regex as re
from src.dataextractor.datatypes import PropertyDictWHS
from src.gui.gui import show_in_gui
from src.util.json_util import load_json_config



def extract_data(file_path):
    
    try:
        #----------SETTINGS
        """Loads from json all properties to container"""
        
        config_data = load_json_config()         
    except Exception as e:
        print(f"Error loading data from temporary library defined in json.config like {file_path}: {e}") 

        sym_properties_mandatory = get_mandatory_dict_properties(config_data)


  
    #-------------------------------------------------------
    #----------TEMPORARY LIBRARY----------------------------
    """Loads from all properties from temporary library"""
    with open(file_path, "r", encoding="utf-8") as file:
        temp_library_data = file.read() 
        symbols = get_matching_key(temp_library_data,"(symbol ")
        for symbol in symbols: #handling symbol by symbol
            sym_properties_temp = get_matching_key(symbol, "(property ")
            property_temp_dict: PropertyDictWHS = get_dict_properties(sym_properties_temp)
            
            merge with sym_properties_mandatory Todo 
            
            #Show in gui
            show_in_gui(property_temp_dict, config_data.get('library_final_folder'))
            keys_list = list(property_temp_dict.keys())
            print(property_temp_dict[keys_list[0]] ['value'])
            #merge mandatory properties with 

        
    
    """najdi symbol 
    propočítej závorky 
    vyjmutou část ulož
    načti jednotlivé properties
    dopln o nové vytvoř symbol znova.
    ulož do nové knihovny"""



        

    

         

def get_mandatory_dict_properties(config_data):
    sym_properties_dict: PropertyDictWHS = {
            item["name"]: item for item in config_data.get("sym_property_mandatory", [])
    }
    return sym_properties_dict

def get_dict_properties(properties):
    properties_dict = {}
    for property in properties:
        match = re.search(r'\(property\s+"(?P<name>[^"]+)"+\s+"(?P<value>[^"]+)"', property)  #https://regex101.com/
     
        if match:
            property_name = match.group("name")
            property_value = match.group("value")
            property_dict: PropertyDictWHS  = {
                "name": property_name,
                "value": property_value,
                "format_value": "",  # Default empty format_value, can be updated if necessary
                "snippet": {property}
            }
        properties_dict[property_name] = property_dict

    return properties_dict

def get_matching_key (symbol_properties, search_pattern):
    matches = []
    start_pos = 0
    text_length = len(symbol_properties)
    

     #find symbols
        
    while start_pos < text_length:
            # Najdi výskyt `search_pattern` od aktuální pozice
            start_pos = symbol_properties.find (search_pattern,start_pos)
            if start_pos == -1:         
                break  # Pokud není další výskyt, skonči
            
            bracket_counter = 1            
            end_pos = start_pos + 1 
            # Iteruj a hledej uzavírací závorky
            while bracket_counter > 0 and end_pos < text_length:
                if symbol_properties[end_pos] == '(':
                    bracket_counter += 1
                elif symbol_properties[end_pos] == ')':
                    bracket_counter -= 1
                end_pos += 1
            
                # Pokud jsme vyrovnali závorky, přidej výsledek
                if bracket_counter == 0:
                    matches.append(symbol_properties[start_pos:end_pos])
                    start_pos = end_pos+1  # Pokračuj za tímto blokem
                    break

    return matches

