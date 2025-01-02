import json

def extract_data(file_path):
    
    try:
        #----------SETTINGS
        """Loads from json all properties to container"""
        with open("config.json", "r", encoding="utf-8") as file:
            config_data = json.load(file)            
            sym_properties = config_data.get("sym_property_mandatory", [])

        #-------------------------------------------------------
        #----------TEMPORARY LIBRARY----------------------------
        """Loads from all properties from temporary library"""
        with open(file_path, "r", encoding="utf-8") as file:
            config_data = json.load(file)            
            sym_properties = config_data.get("sym_property_mandatory", [])

        najdi symbol 
        propočítej závorky 
        vyjmutou část ulož
        načti jednotlivé properties
        dopln o nové vytvoř symbol znova.
        ulož do nové knihovny



        

    except Exception as e:
        print(f"Error loading data from temporary library defined in json.config like {file_path}: {e}")


def load_sym_properties(config_data): # delete use now for example
    # Extrahování pole sym_property_mandatory

        

        # Iterace přes vlastnosti a jejich výpis
        for prop in sym_properties:
            name = prop.get("name")
            format_value = prop.get("format_value")
            snippet = prop.get("snippet")
            print(f"Name: {name}, Format: {format_value}, Snippet:\n{snippet}\n")
