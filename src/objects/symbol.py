from src.util.json_util import ConfigSingleton
from enum import Enum
from pathlib import Path
from typing import TypedDict
import regex as re
from blinker import Signal
from src.events.eventReciever import EventReceiver


class PropertyDictWHS(TypedDict):
    name: str
    value: str
    format_value: str
    snippet: str

class kicad_symbol_print_depth(Enum):
    VERBOSE = 1
    SETTINGS = 2


class kicad_symbol:
    def __init__(self, one_symbol_string):
        self.symbolText = one_symbol_string
        self.propertiesTextCollection = self.TextParsing.get_matching_key(self.symbolText,  "(property ")
        self.propertiesInternalDict: PropertyDictWHS = self.TextParsing.get_WhsDict_properties(self.propertiesTextCollection) 
        self.config_json = ConfigSingleton()
        self.propertiesMandatory = self.TextParsing.get_mandatory_dict_properties(self.config_json.config.get('sym_property_mandatory'))
        self.propertiesFinal = self.TextParsing.merge_properties(self.propertiesInternalDict, self.propertiesMandatory )


    def set_destination_library(self, library_file):
        self.selected_destination_lib = Path(self.config_json.config["library_final_folder"]) / library_file


    def registerEventReceiverSaveCmd(self, signal_save):
        self.receiverSave = EventReceiver(signal_save, self.saveCmd)
    
    def unregisterEventSaveCmd(self):
        self.receiverSave.disconnect()

    def saveCmd(self, sender, **kwargs):
        print(f"Custom Handler: {sender} sent {kwargs}")
        

    def __str__(self):
        keys_list = list(self.propertiesTextCollection.keys())
        printresult = "\nPrint of instance of class:\"kicad_symbol\"\n" 

        for property in keys_list:            
            prop_data = self.propertiesTextCollection[property]
            printresult += f""" Key: {property}\n"""            
        return printresult
            
    def to_string(self, print_depth, detail=True):
        

        keys_list = list(self.propertiesTextCollection.keys())
        printresult = "\nPrint of instance of class:\"kicad_symbol\"\n" 

        if print_depth==kicad_symbol_print_depth.VERBOSE:
            printresult += "VERBOSE\n"
            for property in keys_list:            
                prop_data = self.propertiesTextCollection[property]
                printresult += f""" Key: {property}\n
                \t Name:   {prop_data['name']}
                \t Value:  {prop_data['value']}
                \t Format: {prop_data['format_value']}
                """
            return printresult
        
        if print_depth==kicad_symbol_print_depth.SETTINGS:
            printresult += "CONFIG json:\n"
            printresult += self.config_json.get_print_content(60)               
            return printresult
        
    class TextParsing:
        @staticmethod
        def get_matching_key(symbol_properties, search_pattern):
            matches = []
            start_pos = 0
            text_length = len(symbol_properties)

            #find symbols
            while start_pos < text_length:
            # Najdi výskyt `search_pattern` od aktuální pozice
                start_pos = symbol_properties.find(search_pattern, start_pos)
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
        
            
        """Transform properties to WhsDictionary format"""
        @staticmethod
        def get_WhsDict_properties(properties):
            properties_dict = {}
            for property in properties:
                match = re.search(r'\(property\s+"(?P<name>[^"]+)"+\s+"(?P<value>[^"]+)"',
                                  property)
                # https://regex101.com/
                if match:
                    property_name = match.group("name")
                    property_value = match.group("value")
                    property_dict: PropertyDictWHS  = {
                        "name": property_name,
                        "value": property_value,
                        "format_value": "",
                        "snippet": {property}
                    }
                properties_dict[property_name] = property_dict
            return properties_dict
        

        @staticmethod
        def get_mandatory_dict_properties(sym_property_mandatory):   
            sym_properties_dict: PropertyDictWHS = {
                item["name"]: item for item in sym_property_mandatory
            }
            return sym_properties_dict
        
        @staticmethod
        def merge_properties(property_temp_dict, sym_properties_mandatory_dict):
            properties_merged: PropertyDictWHS    

            properties_merged = property_temp_dict.copy()

            for key, value in sym_properties_mandatory_dict.items():
                if key not in properties_merged:  # Přidání pouze chybějících položek
                    properties_merged[key] = value

              # Výpis všech 'name'
            """for value in properties_merged.values():
                print("name:", value["name"])  # Přístup k hodnotě 'name'"""   
            return properties_merged

   
