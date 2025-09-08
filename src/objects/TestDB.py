import pyodbc
import os
from src.objects.HeliosDB import DataBaseConnector


class TestDB(DataBaseConnector):
    _instance = None  # Statická proměnná pro uchování instance


    def get_connection_info(self):
        return {
            "login": "sa",
            "ip": "127.0.0.1,14333",
            "db": "heliosTestDb",
            "password": "Whs63306330",
            
            "workstation": os.environ.get("COMPUTERNAME", "Unknown")
        }

   
     
    def __init__(self):
        
        
        self.connection = None
        self._connected = False

   


#    @property
#    def connected(self):
#        return self._connected
#
#    def __del__(self):
#        try:
#            if self.connection and self._connected:
#                self.connection.close()
#        except Exception as ex:
#            print(f"Error closing connection in testDB destructor: {ex}")
#
#    def get_connection(self):
#        return self.connection
#
#    def close(self):
#        try:
#            if self.connection and self._connected:
#                self.connection.close()
#            self._connected = False
#        except Exception as ex:
#            print(f"Error closing connection: {ex}")
#
#
#    def send_query(self, sql_query, values=None):
#        try:
#            cursor = self.connection.cursor()
#            if (values == None):
#                cursor.execute(sql_query)
#            else:
#                cursor.execute(sql_query, values) 
#            #rows = cursor.fetchall()
#
#            columns = [column[0] for column in cursor.description]
#
#            # Získání první řádky dat
#            row = cursor.fetchone()
#
#            # Sloučení názvů sloupců s daty
#            #result = dict(zip(columns, row))
#
#
#            print(columns)  # Výstup: {'column1': value1, 'column2': value2, ...}
#            print(row)
#            cursor.close()
#
#            return row
#
#        except Exception as e:
#            print("Error connection to database: ", e)
#
#
#            
#    
#    def create_table(self, table_name, column_defs):
#        #try:
#            cursor = self.connection.cursor()
#
#            # Oprava: Použití sys.tables k ověření existence
#            check_table_exists = "SELECT COUNT(*) FROM sys.tables WHERE name = ?"
#            cursor.execute(check_table_exists, (table_name,))
#            table_exists = cursor.fetchone()[0]
#
#            # Pokud tabulka neexistuje, vytvoříme ji
#            if not table_exists:
#                # Oprava: Použití hranatých závorek pro bezpečnost názvů
#                create_table_sql = f"CREATE TABLE [{table_name}] ({column_defs})"
#                print(f"Executing: {create_table_sql}")  # Debug výstup
#                cursor.execute(create_table_sql)
#                self.connection.commit()  # Potvrzení změn

        #except Exception as e:
            #print("Error create table: ", e)
         
  
    
        

