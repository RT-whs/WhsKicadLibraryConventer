import json

def load_json_config():
    with open("config.json", "r", encoding="utf-8") as file:
        return  json.load(file)   