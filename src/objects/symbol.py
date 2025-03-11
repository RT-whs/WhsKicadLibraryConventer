from src.util.json_util import ConfigSingleton
from enum import Enum
from pathlib import Path
from typing import TypedDict
import regex as re
from blinker import Signal
import os
from src.events.eventReceiver import EventReceiver
from typing import Final
from src.objects.filehandler import FileHandlerKicad


class PropertyDictWHS(TypedDict):
    name: str
    value: str
    format_value: str
    snippet: str

class kicad_symbol_print_depth(Enum):
    VERBOSE = 1
    SETTINGS = 2


class kicad_symbol:
    #Constants
    PLACEHOLDER_NAME: Final[str] = "{PLACEHOLDER_NAME}"
    PLACEHOLDER_VALUE: Final[str] = "{PLACEHOLDER_VALUE}"
    PLACEHOLDER_DELETED_KEY: Final[str] = "{PLACEHOLDER_DELETED_KEY}"

    def __init__(self, one_symbol_string):
        self.symbolText = one_symbol_string
        self.propertiesTextCollection = self.TextParsing.get_matching_key(self.symbolText,  "(property ")
        self.propertiesInternalDict: PropertyDictWHS = self.TextParsing.get_WhsDict_properties(self.propertiesTextCollection) 
        self.config_json = ConfigSingleton()
        self.propertiesMandatory = self.TextParsing.get_mandatory_dict_properties(self.config_json.config.get('sym_property_mandatory'))        
        self.propertiesFinal:PropertyDictWHS = self.TextParsing.merge_properties(self.propertiesInternalDict, self.propertiesMandatory )
        self.symbolTextFinal = self.symbolText
        self.footprintFileSource, self.footprintSourcePath = FileHandlerKicad.Static.get_footprint_file_content_from_watched_folder(str(self.get_footprint_name()))

        self.filePathStp3DSource = self.get_model_value()
        self.filePathStp3DDest   = ""
        self.selected_destination_lib ="" #setter = set_destination_library 


    """Set destination lib file"""
    def set_destination_library(self, library_file):
        
        encoded_lib_file = FileHandlerKicad.Static.fix_path(library_file)
        #Example C:\WHS_Kicad_Libraries\parts\passive\resitors\whs_resistors_highPower.kicad_sym
        self.selected_destination_lib = Path(self.config_json.config["library_final_folder"]) / encoded_lib_file
        self.update_properties_by_library_name(self.selected_destination_lib)

        #Footprint original file 
        """Loaded during init to memory self.footprintFile"""

        #3d data destination
        #Example C:\WHS_Kicad_Libraries\parts\passive\resitors\whs_resistors_highPower.3dshapes\KY_DDLN31.23-5G8H-36-J3T3-200-R18.stp
        #where file name is taken from basename 3d source
        #3dSource is taken from from kicad_mod file directly readed on init
        library_path = str(self.selected_destination_lib).replace( 'kicad_sym', '3dshapes') 
        self.filePathStp3DDest = Path(library_path).joinpath(os.path.basename(self.filePathStp3DSource))

        #Footprint new file
        """Get path from selected library"""
        #Example C:\WHS_Kicad_Libraries\parts\passive\resitors\whs_resistors_highPower.pretty\KYDDLN31235G8H36J3T3200R18.kicad_mod
        footprint_path = str(self.selected_destination_lib).replace( 'kicad_sym', 'pretty') 
        self.footprintDestionationPath = Path(footprint_path).joinpath(os.path.basename(self.footprintSourcePath))
        
        """Adjust the file content ... model link"""
        self.set_model_value(str(self.filePathStp3DDest)) #write link to footprint file


        


    """
    For automatic update some properties when destination library
    is setted or changed
    """
    def update_properties_by_library_name(self, selected_library_name):
        footprint = self.propertiesFinal['Footprint'] 
        footList=str(footprint['value']).split(':')
        footList[0] = Path(selected_library_name).stem #filename without suffix
        self.propertiesFinal['Footprint']['value'] = footList[0] + ':' + footList[1]

    """Can be used like file name"""
    def get_footprint_name(self):
        _fpComplete = self.propertiesInternalDict['Footprint']['value']
        if ':' not in _fpComplete:
            raise ValueError("Footprint name is missing ':' separator or value after it.")
        _fpName = str(_fpComplete).split(':',1) #get part after :
        if len(_fpName) < 2 or not _fpName[1].strip():
            raise ValueError("Footprint name is empty after ':' separator.")
        return _fpName[1]


    def get_model_value(self):        
        match = re.search(r'\(\s*model\s+"([^"]+)"', self.footprintFileSource)
        return match.group(1) if match else None
    

    def set_model_value(self, new_value):
        self.footprintFileDestination = self.footprintFileSource
        fixed_new_value = FileHandlerKicad.Static.fix_path(new_value)
        self.footprintFileDestination = re.sub(
            r'(\(\s*model\s+")([^"]+)(")', 
            rf'\1{fixed_new_value}\3', 
            #rf'\1{re.escape(new_value)}\3', 
            self.footprintFileDestination
        )


    def get_symbol_name(self):
        return  self.propertiesInternalDict['Value']['value']

    def registerEventReceiverSaveCmd(self, signal_save):
        self.receiverSave = EventReceiver(signal_save, self.saveCmd)
    
    def unregisterEventSaveCmd(self):
        self.receiverSave.disconnect()

    """Function called from gui to saving symbol to final library."""

    def saveCmd(self, sender, **kwargs):
        """kwargs {'action': 'clicked'}"""
        print(f"Custom Handler saveCmd: {sender} sent {kwargs}")
        print("Checking ERP number at helios, check collisions -- not implemented now")

        print("Copy  footprint symbolname.kicad_mod from temp library to selected final library")

        print("Kicad.mod delete original")

        print("Update kicad mode in temp folder for proper 3dshape step file. ")    
        

        print("Move symbol 3dshape file symbolname.stp from temp library to selected final library")
        FileHandlerKicad.Static.move_file( self.filePathStp3DSource, self.filePathStp3DDest)

        



        

        

    def __str__(self):
        keys_list = list(self.propertiesTextCollection.keys())
        printResult = "\nPrint of instance of class:\"kicad_symbol\"\n" 

        for property in keys_list:            
            prop_data = self.propertiesTextCollection[property]
            printResult += f""" Key: {property}\n"""            
        return printResult
            
    def to_string(self, print_depth, detail=True):
        

        keys_list = list(self.propertiesTextCollection.keys())
        printResult = "\nPrint of instance of class:\"kicad_symbol\"\n" 

        if print_depth==kicad_symbol_print_depth.VERBOSE:
            printResult += "VERBOSE\n"
            for property in keys_list:            
                prop_data = self.propertiesTextCollection[property]
                printResult += f""" Key: {property}\n
                \t Name:   {prop_data['name']}
                \t Value:  {prop_data['value']}
                \t Format: {prop_data['format_value']}
                """
            return printResult
        
        if print_depth==kicad_symbol_print_depth.SETTINGS:
            printResult += "CONFIG json:\n"
            printResult += self.config_json.get_print_content(60)               
            return printResult
        
    ##Subroutines
    def ActualizeSymbolTextFinal(self, symbolTextWithoutProperties):
        #update snippets
        for key, value in self.propertiesFinal.items():            
            value["snippet"] = str(value["snippet"]).replace(self.PLACEHOLDER_NAME,value['name'])
            value["snippet"] = str(value["snippet"]).replace(self.PLACEHOLDER_VALUE,value['value'])

        #serialize snippets
        keys_listPropertiesFinal = list(self.propertiesFinal.keys())
        snippet = "\n".join(
            str(self.propertiesFinal[key]['snippet'])
            for key in keys_listPropertiesFinal
            )
        #print("Variable snippet type is:" +str(type(snippet)))
        self.symbolTextFinal = self.TextParsing.place_keys_over_placeholder(symbolTextWithoutProperties , snippet , self.PLACEHOLDER_DELETED_KEY)


    class TextParsing:
        @staticmethod
        def get_matching_key(symbol_properties, search_pattern):
            matches = []
            start_pos = 0
            text_length = len(symbol_properties)

            #find symbols
            while start_pos < text_length:
            # Find `search_pattern` from actual pos
                start_pos = symbol_properties.find(search_pattern, start_pos)
                if start_pos == -1:
                    break  # End when no next occur

                bracket_counter = 1
                end_pos = start_pos + 1
                # Iterate and find matching brackets
                while bracket_counter > 0 and end_pos < text_length:
                    if symbol_properties[end_pos] == '(':
                        bracket_counter += 1
                    elif symbol_properties[end_pos] == ')':
                        bracket_counter -= 1
                    end_pos += 1

                    # When reach bracket pairs continue by next block
                    if bracket_counter == 0:
                        matches.append(symbol_properties[start_pos:end_pos])
                        start_pos = end_pos+1  # Continue after this block
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
                        "snippet": property
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
                if key not in properties_merged:  # Add missing items
                    properties_merged[key] = value

            return properties_merged
        
        
        @staticmethod
        def delete_matching_key(symbol_properties, search_pattern, replacement):
            start_pos = 0
            text_length = len(symbol_properties)
            if symbol_properties.find('(',0) == -1:
                return symbol_properties
            while start_pos < text_length:
                 start_pos = symbol_properties.find(search_pattern, start_pos)
                 if start_pos == -1:
                     break
                 
                 bracket_counter = 1
                 end_pos = start_pos + 1

                 while bracket_counter > 0 and end_pos < text_length:
                     if symbol_properties[end_pos] == '(':
                         bracket_counter += 1
                     elif symbol_properties[end_pos] == ')':
                         bracket_counter -= 1
                     end_pos += 1

                     if bracket_counter == 0:
                         symbol_properties = symbol_properties[:start_pos]+ replacement + symbol_properties[end_pos:]  # Remove block 
                         text_length = len(symbol_properties)  # Actualize text len
                         start_pos = start_pos  # Continue from same pos
                         break
                     
            return symbol_properties
        

        @staticmethod
        def place_keys_over_placeholder(sourceDocument : str, keys, placeholder):
            resultDoc = sourceDocument.replace(placeholder,keys,1)
            resultDoc = resultDoc.replace(placeholder,"")
            # Remove empty lines
            resultDoc = "\n".join(line for line in resultDoc.splitlines() if line.strip())
            return resultDoc
            
            
            
            

   
