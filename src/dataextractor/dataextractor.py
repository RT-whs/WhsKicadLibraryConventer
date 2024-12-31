import os

def extract_data(file_path):
    """Funkce pro načítání a zpracování dat ze souboru."""
    print(f"Loading data from {file_path}")
    # Zde bys mohl provést nějaké operace s daty, např. otevření souboru nebo jeho zpracování.
    with open(file_path, 'r') as file:
        data = file.read()
        print(f"Data loaded: {data[:100]}...")  # Ukázka prvních 100 znaků
