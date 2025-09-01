import json
from cryptography.fernet import Fernet

# Tvůj šifrovací klíč (nahraď vlastním uloženým klíčem)
with open("crypto.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

# Nové heslo k zašifrování
new_password = "Hesloveslo2023"
encrypted_password = cipher.encrypt(new_password.encode()).decode()

# Načtení existujícího JSON souboru
try:
    with open("config.json", "r", encoding="utf-8") as file:
        data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    data = {}  # Pokud soubor neexistuje nebo je poškozený, vytvoří se nový slovník

# Aktualizace hesla
data["helios_app_password"] = encrypted_password

# Uložení zpět do JSON
with open("config.json", "w") as file:
    json.dump(data, file, indent=4)

print("Šifrované heslo bylo aktualizováno v config.json")
