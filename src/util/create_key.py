from cryptography.fernet import Fernet

# Vygenerování nového klíče
key = Fernet.generate_key()

# Uložení klíče do souboru
with open("crypto.key", "wb") as key_file:
    key_file.write(key)

print("Šifrovací klíč byl uložen do 'crypto.key'.")