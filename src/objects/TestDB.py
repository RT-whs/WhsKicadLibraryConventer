import pyodbc
import os


class TestDB:
    _instance = None  # Statická proměnná pro uchování instance

    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super(TestDB, cls).__new__(cls)            
        return cls._instance
     
    def __init__(self):
        
        self._app_login =  'sa'
        self._ip_address = '127.0.0.1'
        self._db_catalog = 'heliosTestDb'
        self._password = 'Whs63306330'
        self._port      = '14333'
        self._workstation = os.environ.get("COMPUTERNAME", "Unknown")
        self.connection = None
        self._connected = False

   


    @property
    def connected(self):
        return self._connected

    def __del__(self):
        try:
            if self.connection and self._connected:
                self.connection.close()
        except Exception as ex:
            print(f"Error closing connection in testDB destructor: {ex}")

    def get_connection(self):
        return self.connection

    def close(self):
        try:
            if self.connection and self._connected:
                self.connection.close()
            self._connected = False
        except Exception as ex:
            print(f"Error closing connection: {ex}")


    def send_query(self, sql_query, values=None):
        try:
            cursor = self.connection.cursor()
            if (values == None):
                cursor.execute(sql_query)
            else:
                cursor.execute(sql_query, values) 
            #rows = cursor.fetchall()

            columns = [column[0] for column in cursor.description]

            # Získání první řádky dat
            row = cursor.fetchone()

            # Sloučení názvů sloupců s daty
            #result = dict(zip(columns, row))


            print(columns)  # Výstup: {'column1': value1, 'column2': value2, ...}
            print(row)
            cursor.close()

            return row

        except Exception as e:
            print("Error connection to database: ", e)


            
    
    def create_table(self, table_name, column_defs):
        #try:
            cursor = self.connection.cursor()

            # Oprava: Použití sys.tables k ověření existence
            check_table_exists = "SELECT COUNT(*) FROM sys.tables WHERE name = ?"
            cursor.execute(check_table_exists, (table_name,))
            table_exists = cursor.fetchone()[0]

            # Pokud tabulka neexistuje, vytvoříme ji
            if not table_exists:
                # Oprava: Použití hranatých závorek pro bezpečnost názvů
                create_table_sql = f"CREATE TABLE [{table_name}] ({column_defs})"
                print(f"Executing: {create_table_sql}")  # Debug výstup
                cursor.execute(create_table_sql)
                self.connection.commit()  # Potvrzení změn

        #except Exception as e:
            #print("Error create table: ", e)
         
  
    def connect(self):
        connection_string = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={self._ip_address},{self._port};'
            f'DATABASE={self._db_catalog};'
            f'UID={self._app_login};'
            f'PWD={self._password};'
            f'Workstation ID={self._workstation};'
           
        )
        
        try:
            
            self.connection = pyodbc.connect(connection_string)
            self._connected = True
            print(f"Connected\n")
            return True
        
        except Exception as ex:
            print(f"Connection string: " + connection_string)
            print(f"Function Helios::Connect error: {ex}")
            if self.connection:
                self.connection.close()
            return False
        

