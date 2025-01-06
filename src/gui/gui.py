import tkinter as tk
from tkinter import ttk
from src.dataextractor.datatypes import PropertyDictWHS

def show_in_gui(property_dict):

    def on_double_click(event):
        button_clicked = False
        """Zahájí editaci hodnoty při dvojkliku."""
        selected_item = tree.selection()
        if not selected_item:
            return
        item_id = selected_item[0]
        column_index = tree.identify_column(event.x)

        # Ověření, zda se kliklo do sloupce 'Value'
        if column_index == "#2":  # #2 odpovídá sloupci "Value"
            x, y, width, height = tree.bbox(item_id, column="#2")
            value = tree.item(item_id, "values")[1]
            name = tree.item(item_id, "values")[0]

            
           
            # Standardní vstupní pole pro jiné položky
            entry = tk.Entry(tree)
            entry.place(x=x, y=y, width=width, height=height)
            entry.insert(0, value)
            entry.focus()

            def on_focus_out(event=None):
                """Uloží hodnotu a zničí vstupní pole a tlačítko."""
                if button_clicked:  # Pokud bylo kliknuto na tlačítko, nepokračujeme
                    entry.focus_set()  # Znovu nastavíme fokus na vstupní pole
                    return
                    
                """Uloží hodnotu a zničí vstupní pole."""
                new_value = entry.get()
                tree.item(item_id, values=(tree.item(item_id, "values")[0], new_value))
                entry.destroy()

            def on_return(event=None):
                """Uloží hodnotu při stisknutí Enter."""
                on_focus_out()

                entry.bind("<FocusOut>", on_focus_out)
                entry.bind("<Return>", on_return)

            if name in {"Footprint", "ERP"}:
                def on_button_click():
                    nonlocal button_clicked
                    button_clicked = True
                    print(f"Footprint button clicked! Current value: {entry.get()}")
                    # Zde můžete přidat vlastní logiku, např. otevření dialogu


                # Pokud je položka footprint nebo ERP, zobraz tlačítko
                button = tk.Button(frame_tree, text="...", command=lambda: handle_button_click(name))
                button.place(x=x + width - 25, y=y, width=25, height=height)
                
                def on_focus_out(event=None):
                    """Skryje tlačítko při ztrátě fokusu."""
                    #button.destroy()

                root.bind("<Button-1>", on_focus_out, add="+")

    def save_changes():
        """Uloží změny zpět do property_dict."""
        for item_id in tree.get_children():
            name, value = tree.item(item_id, "values")
            for key, prop in property_dict.items():
                if prop["name"] == name:
                    prop["value"] = value

    root = tk.Tk()
    root.title("Editable Properties Viewer")

    frame_tree = ttk.Frame(root)
    frame_tree.grid(row=1, column=0, columnspan=3, padx=10, pady=20, sticky="nsew") 

    # Vytvoření stromového widgetu (Treeview) jako tabulky
    tree = ttk.Treeview(frame_tree, columns=("name", "value"), show="headings", height=15)
    tree.heading("name", text="Name")
    tree.heading("value", text="Value")
    tree.column("name", width=200)
    tree.column("value", width=600)

    # Naplnění tabulky daty
    for key, value in property_dict.items():
        tree.insert("", tk.END, values=(value["name"], value["value"]))

    tree.grid(row=1, column=0, columnspan=3, padx=10, pady=20, sticky="nsew")  # Proveďte roztažení



    # Přidání scrollbarů
     # Přidání vertikálního scrollbaru
    scrollbar_y = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.grid(row=1, column=3, sticky='ns')  # Vertikální scrollbar napravo

    # Přidání horizontálního scrollbaru
    scrollbar_x = ttk.Scrollbar(frame_tree, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=scrollbar_x.set)
    scrollbar_x.grid(row=2, column=0, columnspan=3, sticky='ew')  # Horizontální scrollbar pod tree view


    # Událost dvojkliku
    tree.bind("<Double-1>", on_double_click)

    

    #Create library selector
    DestinationLibName = "Choose library"
    label1 = ttk.Label(root,text="Choose/add library")
    label1.grid(row=0,column=0,pady=5, padx=5, sticky='w')
    entryDestLibname = tk.Entry(root)
    entryDestLibname.grid(row=0,column=0,pady=5, padx=150, sticky='w')
    buttonSelectlibrary = tk.Button(root, text="Select existing",  command=lambda: handle_button_selectLibrary_click(entryDestLibname.get()))
    buttonSelectlibrary.grid(row=0,column=0 ,pady=5, padx=280, sticky='w')


    # Přidání tlačítka pro uložení změn
    save_button = tk.Button(root, text="Save Changes", command=save_changes)
    save_button.grid(row=2,column=1,pady=10)

    # Zajištění, že sloupce se roztáhnou, pokud je to potřeba
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_columnconfigure(3, weight=0)  # Sloupec pro scrollbar y, nemusí se roztahovat

    # Zajištění, že řádky se roztáhnou, pokud je to potřeba
    root.grid_rowconfigure(1, weight=1)  # Prostor pro Treeview se roztáhne
    root.grid_rowconfigure(2, weight=0)  # Horizontální scrollbar by neměl zabírat moc místa
    root.grid_rowconfigure(3, weight=0)  # Pro tlačítko uložení

    # Aby se frame_tree roztáhl, nastavíme váhu pro tento rámec a pro řádky
    frame_tree.grid_rowconfigure(0, weight=1)  # Aby se Treeview roztáhlo
    frame_tree.grid_columnconfigure(0, weight=1)  # Aby se Treeview roztáhlo na šířku
    frame_tree.grid_columnconfigure(1, weight=0)  # Sloupec pro scrollbar y, nemusí se roztahovat

    root.mainloop()