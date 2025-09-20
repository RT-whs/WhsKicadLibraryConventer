#Main test
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),  "..")))

from src.objects.filehandler import FileHandlerKicad
from src.objects.filehandler import FileHandlerKicad
from src.objects.HeliosDB import HeliosDB
from src.objects.TestDB import TestDB

import re
from pathlib import Path


# add root project folder to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

import unittest
from typing import TypedDict


#should use absolute linking so needed to set the env var by this: 
#$env:PYTHONPATH="F:\WHS\Projects\Company\WhsKicadLibraryConverter"
from src.gui.gui import show_in_gui
from src.objects.symbol import kicad_symbol


class TestData(unittest.TestCase):
    

    def setUp(self):
        with open("tests/testing.kicad_sym", "r", encoding="utf-8") as file:
            temp_library_data = file.read()      
            self.text = temp_library_data
            
    @unittest.skip("Not call on the production DB")
    def test_helios(self):
        self.db = HeliosDB()
        self.assertTrue(self.db.connect() )

        ### Get index from helios        
        # self.db.send_query( r"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
        result = self.db.send_query( r"SELECT MAX(RegCis) AS MaxRegCis FROM TabKmenZbozi WHERE SkupZbo = 320")

        number = int(result[0])
        print(number)
        print(number + 1)
       

        result = self.db.send_query( r"SELECT * FROM TabKmenZbozi WHERE SkupZbo = 320 AND RegCis = ?", number )
        #zjistí že ID v této tabulce je autoincrement - potvrdí že je autoincrement id
        result_row = self.db.send_query( r"SELECT name, is_identity FROM sys.columns WHERE object_id = OBJECT_ID('TabKmenZbozi')")         
        self.db.close()    

    

        
  
    @unittest.skip("Skipped empty")
    def test_wsl_testDB(self):
        """ 
        WSL2
        Ubuntu 22.04

        in wsl2 is docker 

        docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=Whs63306330" 
            -e "MSSQL_PID=Developer" -e "MSSQL_AGENT_ENABLED=true" 
            -p 14333:1433 --name sqlcontainerwsl --hostname sqlcontainerwsl 
            -d mcr.microsoft.com/mssql/server:2022-latest

        docker cmds in wsl
        docker ps - show info about docker image
        docker exec -it sqlcontainerwsl /bin/bash  - příkazový řádek přímo v image
        docker inspect sqlcontainerwsl

        Další kontejner sqlcmd který se po ukončení smaže .. obsahuje nástroj pro editaci sql serveru
        docker run --rm -it mcr.microsoft.com/mssql-tools /opt/mssql-tools/bin/sqlcmd -S 172.17.0.2 -U sa -P "Whs63306330"

        Připojení přes SSMS (ve Windows)
            Server name: localhost,14333
            Authentication: SQL Server Authentication
            Login: sa
            Password: heslo (to, co jsi nastavil v proměnné MSSQL_SA_PASSWORD) 

            Databáze: heliosTestDb

        Připojení přímo z wsl 
        docker exec -it sqlcontainerwsl /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "heslo"
        SELECT @@VERSION;

        Připojení z windows
        sqlcmd -S 127.0.0.1,14333 -U sa -P "Whs63306330"

        show databases
        SELECT name
        FROM sys.databases;

        show tables;
        SELECT * FROM information_schema.tables;

        delete table
        DROP TABLE tablename;
        """
        #self.dbTest = TestDB()
        #self.assertTrue(self.dbTest.connect() )
        #self.dbTest.close()


  
    @unittest.skip("Skipped data already prepared")
    def test_copy_table(self):
        
        
        def create_table_like(src_cursor, dst_cursor, table_name: str):
            # 1. Zjistit definici sloupců ze zdrojové tabulky
            src_cursor.execute(f"SELECT * FROM {table_name} WHERE 1=0")
            cols = src_cursor.description

            # 2. Mapování Python/ODBC typů -> SQL Server typy
            type_map = {
                int: "INT",
                str: "NVARCHAR(MAX)",
                float: "FLOAT",
                bytes: "VARBINARY(MAX)",
            }

            col_defs = []
            for col in cols:
                name = col[0]
                pytype = col[1]
                sqltype = type_map.get(pytype, "NVARCHAR(MAX)")  # fallback
                col_defs.append(f"[{name}] {sqltype}")

            ddl = f"CREATE TABLE dbo.{table_name} ({', '.join(col_defs)})"

            # 3. Dropnout tabulku pokud existuje
            drop_sql = f"IF OBJECT_ID('dbo.{table_name}', 'U') IS NOT NULL DROP TABLE dbo.{table_name};"
            dst_cursor.execute(drop_sql)

            # 4. Vytvořit tabulku
            dst_cursor.execute(ddl)
            dst_cursor.connection.commit()
            print(f"Tabulka dbo.{table_name} byla znovu vytvořena.")




        print("*     Test_copy_table     *")
        self.db = HeliosDB()
        ConnectedHelios, CursorHelios =  self.db.connect()
        
        self.dbTest = TestDB()
        ConnectedTestDB, CursorTestDb, ConnectionTestDb = self.dbTest.connect()
        result = self.db.send_query( r"SELECT MAX(RegCis) AS MaxRegCis FROM TabKmenZbozi WHERE SkupZbo = 320")
        number = int(result[0])
        kmenova_karta = self.db.send_query( r"SELECT * FROM TabKmenZbozi WHERE SkupZbo = 320 AND RegCis = ?", number )
        print(kmenova_karta[0])
        #Copy table structure - uncoment when necessary
        #col_defs = self.db.get_table_defs('TabKmenZbozi')        
        #self.dbTest.create_table('TabKmenZbozi', col_defs)


        if (True):
            # Načti všechna data a názvy sloupců
            #create_table_like(CursorHelios, CursorTestDb, "TabKmenZbozi")

            CursorHelios.execute("SELECT * FROM TabKmenZbozi WHERE SkupZbo = 320")
            rows = [tuple(r) for r in CursorHelios.fetchall()]
            columns = [desc[0] for desc in CursorHelios.description]

            # Připrav INSERT
            placeholders = ", ".join(["?"] * len(columns))
            columns_str = ", ".join(columns)
            sql = f"INSERT INTO TabKmenZbozi ({columns_str}) VALUES ({placeholders})"

            # Vlož data do cílové DB
            CursorTestDb.executemany(sql, rows)
            ConnectionTestDb.commit()

            print(f"Zkopírováno {len(rows)} řádků.")

        #Save kmenova karta to new db
        print("*     Copy tab Kmen Zbozi Finished    *")
        #Copy table
        



        self.dbTest.close()
        self.db.close()


    def test_localDB(self):
        self.dbTest = TestDB()
        #Connection
        ConnectedTestDB, CursorTestDb, ConnectionTestDb = self.dbTest.connect()
        self.assertTrue(ConnectedTestDB)
        result = self.dbTest.send_query(r"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'TabKmenZbozi';")
        print (result)
        #New item 
            #Check if already exist
                # When exist show the message
        result = self.dbTest.send_query(r"SELECT MAX(RegCis) AS MaxRegCis FROM TabKmenZbozi WHERE SkupZbo = 320")
        maxregcis = result[0][0]
        print (maxregcis)
        number = int(maxregcis)
        number = number +1 
        print(number)
                
                # When not exist create new item in db
        symbol_collection = kicad_symbol.TextParsing.get_matching_key(self.text, "(symbol ")
        obj_test_symbol = kicad_symbol(symbol_collection[0])  
        self.dbTest.copy_last_record('TabKmenZbozi',maxregcis)

        #Update record by symbol
        symbol_collection = kicad_symbol.TextParsing.get_matching_key(self.text, "(symbol ")        
        obj_test_symbol = kicad_symbol(symbol_collection[0])  
        self.dbTest.update_record_by_kicad_symbol('TabKmenZbozi', number, obj_test_symbol)


        self.dbTest.close()
    


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
        #                           Get symbol name
        #----------------------------------------------------------------------------------------     
        self.assertEqual( "KY_DDLN31.23-5G8H-36-J3T3-200-R18", obj_test_symbol.propertiesInternalDict['Value']['value'] )
        self.assertEqual( "KY_DDLN31.23-5G8H-36-J3T3-200-R18", obj_test_symbol.get_symbol_name() )
       
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

        
        #show_in_gui(obj_test_symbol)
        """Temporary code end""" 
        
        #----------------------------------------------------------------------------------------
        #                           SAVE PROPERTIES TO SYM
        #----------------------------------------------------------------------------------------       

        
        
        obj_test_symbol.set_destination_library(r"F:\WHS\Projects\Company\WhsKicadLibraryConventer\tests\whs_test_destinationLib.kicad_sym")
        self.assertEqual( r"F:\WHS\Projects\Company\WhsKicadLibraryConventer\tests\whs_test_destinationLib.kicad_sym", str(obj_test_symbol.selected_destination_lib) )

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
        replaced_text = kicad_symbol.TextParsing.place_keys_over_placeholder("This is a testing string with \"{placeholder}\"","new text","{placeholder}")
        self.assertEqual("This is a testing string with \"new text\"",replaced_text)

        replaced_text = kicad_symbol.TextParsing.place_keys_over_placeholder("This is a testing string with Placeholder","new text","placeholder")
        self.assertNotEqual("This is a testing string with new text",replaced_text)
        #test to remove also empty lines
        replaced_text = kicad_symbol.TextParsing.place_keys_over_placeholder("This is a testing string with placeholder,\nplaceholder\nplaceholder\n\n\n","new text","placeholder")
        self.assertEqual("This is a testing string with new text,",replaced_text)


        #project testing 
        #update symbol text
        obj_test_symbol.propertiesFinal.clear()
        obj_test_symbol.propertiesFinal[0] = PropertyDictWHS = {
            "name": "propnameexample",
            "value": "123",
            "format_value": "formatted_example",
            "snippet": "(property \"{PLACEHOLDER_NAME}\" \"{PLACEHOLDER_VALUE}\"\n    (at 0 0 0)\n    (effects\n        (font\n            (size 1.27 1.27)\n        )\n    )\n)"
            }
        
        obj_test_symbol.symbolText = "This is a testing string with (property  \"{placeholder}\"  \"{placeholder}\" and more) and symbol continue";   
        obj_test_symbol.ActualizeSymbolTextFinal()
        self.assertEqual("This is a testing string with (property \"propnameexample\" \"123\"\n    (at 0 0 0)\n    (effects\n        (font\n            (size 1.27 1.27)\n        )\n    )\n) and symbol continue",obj_test_symbol.symbolTextFinal)


       
        #print(obj_test_symbol.symbolTextFinal)
        
        #----------------------------------------------------------------------------------------
        #                           LOAD 3D AND OTHER DATA
        #----------------------------------------------------------------------------------------   
        obj_test_symbol.footprintFileSource = """(model "C:\\WHS_Kicad_Temp\\SamacSys_Parts.3dshapes\\KY_DDLN31.23-5G8H-36-J3T3-200-R18.stp"
		    (offset
			    (xyz 0 0 0)
		    )
		    (scale
			    (xyz 1 1 1)
		    )
		    (rotate
			    (xyz 0 0 0)
		    )
	        )"""
        
        obj_test_symbol.set_model_value(r"C:\testfolder\test.stp")
        self.assertEqual( """(model "C:/testfolder/test.stp"
		    (offset
			    (xyz 0 0 0)
		    )
		    (scale
			    (xyz 1 1 1)
		    )
		    (rotate
			    (xyz 0 0 0)
		    )
	        )""", obj_test_symbol.footprintFileDestination)
        

        #----------------------------------------------------------------------------------------
        #                           CHECK FILES PRESENCE
        #----------------------------------------------------------------------------------------           


    def test_libraries(self):
        whs_lib_list = FileHandlerKicad.Static.get_existing_libs()
        #print("Finded libraries in libraries folder: " +str(whs_lib_list))


    def test_FileHandler(self):
        path = FileHandlerKicad.Static.get_lib_path_with_symbol_variable("C:\WHS_Kicad_Libraries\parts\passive\resistors\whs_resistors_test.kicad_sym") 
        self.assertEqual( "${WHS_MAIN_LIB}/passive/resistors/whs_resistors_test.kicad_sym", path)
        print("Path from file handler: " + path)

        #Update footprint library definition file
        #Check here in test folder manually
        destFile = os.path.join( str(Path(__file__).parent), "fp-lib-table" )
        FileHandlerKicad.Static.save_new_footprint_lib_folder_to_kicad_settings("","test_library",destFile)


if __name__ == '__main__':
    unittest.main()