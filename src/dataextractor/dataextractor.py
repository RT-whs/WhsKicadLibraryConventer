import regex as re
from src.gui.gui import show_in_gui
from src.objects.symbol import kicad_symbol


def extract_data(file_path):


    # -------------------------------------------------------
    # ----------TEMPORARY LIBRARY----------------------------
    # -------------------------------------------------------
    """Loads from all properties from temporary library"""
    with open(file_path, "r", encoding="utf-8") as file:
        temp_library_data = file.read() 
        symbols = kicad_symbol.TextParsing.get_matching_key(temp_library_data,"(symbol ")
        for symbol in symbols: #handling symbol by symbol
            obj_symbol = kicad_symbol (symbol)           

            #Show in gui
            show_in_gui(obj_symbol)

            #next save by save button




















