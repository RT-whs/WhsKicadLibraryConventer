#Main test
import sys
import os
# Přidáme kořenovou složku projektu do sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

import unittest
from typing import TypedDict


#should use absolute linking so needed to set the env var by this: 
#$env:PYTHONPATH="F:\WHS\Projects\Company\WhsKicadLibraryConverter"
from src.gui.gui import show_in_gui
from src.util.lib_util import load_existing_lib_patches
from src.objects.symbol import kicad_symbol


class TestData(unittest.TestCase):
    

    def setUp(self):
        with open("tests/testing.kicad_sym", "r", encoding="utf-8") as file:
            temp_library_data = file.read()      
            self.text = temp_library_data
            

    def test_loading_symbol(self):
        matches = kicad_symbol.TextParsing.get_matching_key(self.text, "(symbol ")       
        self.assertEqual(2,len(matches))
    
    def test_properties(self):

        symbol_collection = kicad_symbol.TextParsing.get_matching_key(self.text, "(symbol ")
        
        obj_test_symbol = kicad_symbol(symbol_collection[0])  
        #----------------------------------------------------------------------------------------
        #                           Load mandatory properties
        #----------------------------------------------------------------------------------------   
        
        self.assertEqual( "ERP", obj_test_symbol.propertiesMandatory.get('ERP', {}).get('name') )
        self.assertEqual( "ERP_Title4_OrderNr", obj_test_symbol.propertiesMandatory.get('ERP_Title4_OrderNr', {}).get('name') )
        self.assertEqual( "^.*$", obj_test_symbol.propertiesMandatory.get('ERP_Title4_OrderNr', {}).get('format_value') )

        #----------------------------------------------------------------------------------------
        #                           Get all property 
        #----------------------------------------------------------------------------------------     
        #EASY ACESS TO KEYS BY INDEX
        keys_list = list(obj_test_symbol.propertiesInternalDict.keys())
        #print(property_temp_dict[keys_list[0]]) 
        self.assertEqual( "Reference", obj_test_symbol.propertiesInternalDict[keys_list[0]] ['name'] )

        #----------------------------------------------------------------------------------------
        #                           Check merge_properties
        #----------------------------------------------------------------------------------------
        #CORE
        #ADD to property_temp_dict the mandatory parts
        """now in property_temp_dict are all properties in standardized format: """
        """Merge required properties with properties which comes from generated library"""        

        #check if value in ERP_Summaries contain dictionary item with name also erp_summaries
        self.assertEqual("ERP_Summaries", obj_test_symbol.propertiesFinal["ERP_Summaries"]["name"])
        #check if also contain value in subdictionary "your summaries"
        self.assertEqual("your summaries", obj_test_symbol.propertiesFinal["ERP_Summaries"]["value"])
        #print(obj_test_symbol)
        #print(obj_test_symbol.to_string(print_depth=kicad_symbol_print_depth.SETTINGS, detail=True))

        """Show properties in window, usually should be commented"""
        #now the data are ready for show in editor and processing
        show_in_gui(obj_test_symbol)
        """Temporary code end""" 
        
        #----------------------------------------------------------------------------------------
        #                           SAVE PROPERTIES TO SYM
        #----------------------------------------------------------------------------------------       
        obj_test_symbol.set_destination_library("F:\WHS\Projects\Company\WhsKicadLibraryConventer\tests\whs_test_destinationLib.kicad_sym")
        self.assertEqual("F:\WHS\Projects\Company\WhsKicadLibraryConventer\tests\whs_test_destinationLib.kicad_sym", str(obj_test_symbol.selected_destination_lib) )

        #----------------------------------------------------------------------------------------
        #                           DELETE matched key
        #----------------------------------------------------------------------------------------   
        deleted_symbol = obj_test_symbol.TextParsing.delete_matching_key(obj_test_symbol.symbolText, "(property ","")
        self.maxDiff = None
        self.assertEqual("""(symbol "KY_DDLN31.23-5G8H-36-J3T3-200-R18"\n\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n\t\t(on_board yes)\n\t\t\n\t\t\n\t\t\n\t\t\n\t\t\n\t\t\n\t\t\n\t\t\n\t\t\n\t\t\n\t\t\n\t\t\n\t\t(symbol "KY_DDLN31.23-5G8H-36-J3T3-200-R18_1_1"\n\t\t\t(rectangle\n\t\t\t\t(start 5.08 2.54)\n\t\t\t\t(end 17.78 -10.16)\n\t\t\t\t(stroke\n\t\t\t\t\t(width 0.254)\n\t\t\t\t\t(type default)\n\t\t\t\t)\n\t\t\t\t(fill\n\t\t\t\t\t(type background)\n\t\t\t\t)\n\t\t\t)\n\t\t\t(pin passive line\n\t\t\t\t(at 0 -5.08 0)\n\t\t\t\t(length 5.08)\n\t\t\t\t(name "K_1"\n\t\t\t\t\t(effects\n\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t\t(number "1"\n\t\t\t\t\t(effects\n\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t)\n\t\t\t(pin passive line\n\t\t\t\t(at 0 -2.54 0)\n\t\t\t\t(length 5.08)\n\t\t\t\t(name "A_1"\n\t\t\t\t\t(effects\n\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t\t(number "2"\n\t\t\t\t\t(effects\n\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t)\n\t\t\t(pin passive line\n\t\t\t\t(at 0 -7.62 0)\n\t\t\t\t(length 5.08)\n\t\t\t\t(name "K_2"\n\t\t\t\t\t(effects\n\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t\t(number "3"\n\t\t\t\t\t(effects\n\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t)\n\t\t\t(pin passive line\n\t\t\t\t(at 0 0 0)\n\t\t\t\t(length 5.08)\n\t\t\t\t(name "A_2"\n\t\t\t\t\t(effects\n\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t\t(number "4"\n\t\t\t\t\t(effects\n\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)""",
                         deleted_symbol)
        
        deleted_symbol = obj_test_symbol.TextParsing.delete_matching_key("My text for testing to delete", "delete","DELETED_KEY")
        self.assertEqual("My text for testing to delete" , deleted_symbol)

        deleted_symbol = obj_test_symbol.TextParsing.delete_matching_key("My text for testing to (delete  nonsense)", "(delete","DELETED_KEY")
        self.assertEqual("My text for testing to DELETED_KEY" , deleted_symbol)


        #----------------------------------------------------------------------------------------
        #                           Replacing
        #----------------------------------------------------------------------------------------   
        replaced_text = kicad_symbol.TextParsing.place_keys_over_placeholder("This is a testing string with placeholder","new text","placeholder")
        self.assertEqual("This is a testing string with new text",replaced_text)

        replaced_text = kicad_symbol.TextParsing.place_keys_over_placeholder("This is a testing string with Placeholder","new text","placeholder")
        self.assertNotEqual("This is a testing string with new text",replaced_text)
        #test to remove also empty lines
        replaced_text = kicad_symbol.TextParsing.place_keys_over_placeholder("This is a testing string with placeholder,\nplaceholder\nplaceholder\n\n\n","new text","placeholder")
        self.assertEqual("This is a testing string with new text,",replaced_text)


        #project testing load merged data
        deleted_symbol = obj_test_symbol.TextParsing.delete_matching_key(obj_test_symbol.symbolText, "(property ",kicad_symbol.PLACEHOLDER_DELETED_KEY)
        obj_test_symbol.ActualizeSymbolTextFinal(deleted_symbol)


        print(obj_test_symbol.symbolTextFinal)
        
        #----------------------------------------------------------------------------------------
        #                           LOAD 3D AND OTHER DATA
        #----------------------------------------------------------------------------------------   


        

        #----------------------------------------------------------------------------------------
        #                           CHECK FILES PRESENCE
        #----------------------------------------------------------------------------------------           

    def test_libraries(self):
        whs_lib_list = load_existing_lib_patches()
        #self.assertIn(os.path.normpath('parts\\passive\\diodes\\whs_diode_Led.kicad_sym'),whs_lib_list)
        


if __name__ == '__main__':
    unittest.main()