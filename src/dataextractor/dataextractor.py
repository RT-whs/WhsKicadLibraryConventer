import regex as re
from src.gui.gui import show_in_gui
from src.objects.symbol import kicad_symbol


def extract_data(file_path):

    #try:
        # ----------SETTINGS
        #"""Loads from json all properties to container"""

        #config_data = ConfigSingleton()
        #except Exception as e:
    #    print(f"Error loading data from temporary library defined in json.config like {file_path}: {e}") 
    #    sym_properties_mandatory_dict = get_mandatory_dict_properties(config_data)

  
    # -------------------------------------------------------
    # ----------TEMPORARY LIBRARY----------------------------
    # -------------------------------------------------------
    """Loads from all properties from temporary library"""
    with open(file_path, "r", encoding="utf-8") as file:
        temp_library_data = file.read() 
        symbols = kicad_symbol.TextParsing.get_matching_key(temp_library_data,"(symbol ")
        for symbol in symbols: #handling symbol by symbol
            obj_symbol = kicad_symbol (symbol)
            #property_temp_dict: PropertyDictWHS = get_WhsDict_properties(sym_properties_temp)
            
            #merge_properties(property_temp_dict, sym_properties_mandatory_dict)            
            
            #Show in gui
            show_in_gui(obj_symbol)
            #keys_list = list(property_temp_dict.keys())
            #print(property_temp_dict[keys_list[0]] ['value'])
            #merge mandatory properties with         
    
    """najdi symbol 
    propočítej závorky 
    vyjmutou část ulož
    načti jednotlivé properties
    dopln o nové vytvoř symbol znova.
    ulož do nové knihovny
    
    
    
    """ 

























