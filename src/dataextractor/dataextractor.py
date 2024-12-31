def extract_data(file_path):
    """Načte data ze souboru a vypíše je."""
    try:
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
            print(f"Data loaded from {file_path}:\n{data[:100]}...")  # Vytiskneme pouze prvních 100 znaků
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
