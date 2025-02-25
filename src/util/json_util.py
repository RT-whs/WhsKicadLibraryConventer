import json

class ConfigSingleton:
    _instance = None  # Statická proměnná pro uchování instance

    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super(ConfigSingleton, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Load json config from file"""
        try:
            with open("config.json", "r", encoding="utf-8") as file:
                self.config = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error when loading configuration config.json: {e}")
            self.config = {}  # Pokud soubor neexistuje nebo je špatně formátovaný, nastavíme prázdný dict

    def get(self, key, default=None, raise_error=False):
        """Return key or throw exception"""
        if key in self.config:
            return self.config[key]
        if raise_error:
            raise KeyError(f"Key '{key}' does not exist in configuration?")
        return default  # Return default value when not raise_error=True
    
    def get_print_content(self, max_length=40):
        """Print config content with keys and values limited to max_length chars"""
        def truncate(value, max_length=40):
            """Omezí délku na max_length znaků tak, že vezme první třetinu a poslední dvě třetiny, mezi ně vloží '...'."""
            value_str = str(value)
    
            if len(value_str) <= max_length:
                return value_str
    
            part1 = max_length // 3  # První třetina
            part2 = max_length - part1 - 3  # Poslední část, mínus tři znaky na '...'

            return value_str[:part1] + "..." + value_str[-part2:]
        
        truncated_config = {truncate(k,max_length): truncate(v,max_length) for k, v in self.config.items()}
        
        # Vytiskne JSON s oříznutými hodnotami
        return(json.dumps(truncated_config, indent=2, ensure_ascii=False))
