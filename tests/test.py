#Main test
import sys
import os
# Přidáme kořenovou složku projektu do sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

import unittest
import regex as re
from typing import TypedDict



#should use absolute linking so needed to set the env var by this: 
#$env:PYTHONPATH="F:\WHS\Projects\Company\WhsKicadLibraryConverter"
from src.dataextractor.dataextractor import get_matching_key, load_json_config, get_mandatory_dict_properties , get_dict_properties
from src.dataextractor.datatypes import PropertyDictWHS
from src.gui.gui import show_in_gui
from src.util.lib_util import load_existing_lib_patches


class TestData(unittest.TestCase):
    

    def setUp(self):
        with open("tests/testing.kicad_sym", "r", encoding="utf-8") as file:
            temp_library_data = file.read()      
            self.text = temp_library_data
            

    def test_loading_symbol(self):
        matches = get_matching_key(self.text, "(symbol ")       
        self.assertEqual(2,len(matches))
    
    def test_properties(self):
        config = load_json_config()
        property_mandatory = get_mandatory_dict_properties(config)
        self.assertEqual( "ERP", property_mandatory.get('ERP', {}).get('name') )
        self.assertEqual( "ERPTitle4_OrderNr", property_mandatory.get('ERPTitle4_OrderNr', {}).get('name') )
        self.assertEqual( "^.*$", property_mandatory.get('ERPTitle4_OrderNr', {}).get('format_value') )

        #load temp library
        matches = get_matching_key(self.text, "(symbol ")
           

        #for symbol in matches:
        property_temp_matches = get_matching_key(matches[0], "(property ")
        property_temp_dict: PropertyDictWHS = get_dict_properties(property_temp_matches)
        show_in_gui(property_temp_dict, config.get('library_final_folder'))
        self.assertEqual( "ERP", property_mandatory.get('ERP', {}).get('name') )
        
        keys_list = list(property_temp_dict.keys())
        #print(property_temp_dict[keys_list[0]]) 
        self.assertEqual( "Reference", property_temp_dict[keys_list[0]] ['name'] )
        """now in property_temp_dict are all properties in standardized format: """

        #CORE
        #ADD to property_temp_dict the mandatory parts



        #now the data are ready for show in editor and processing

    def test_libraries(self):
        whs_lib_list = load_existing_lib_patches()
        self.assertIn(os.path.normpath('parts\\passive\\diodes\\whs_diode_Led.kicad_sym'),whs_lib_list)
        


if __name__ == '__main__':
    unittest.main()