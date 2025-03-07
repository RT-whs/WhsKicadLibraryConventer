import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, simpledialog
from src.util.json_util import ConfigSingleton
from src.objects.symbol import kicad_symbol
from blinker import Signal
from src.events.eventReceiver import EventReceiver
from src.objects.filehandler import FileHandlerKicad


def show_in_gui(symbol_object: kicad_symbol):

    def on_double_click(event):
        button_clicked = False
        button = None

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
                """Handles focus out events, ensuring entry and button are cleaned up."""
                try:
                    if entry.winfo_ismapped():  # Check if the entry widget is still valid
                        new_value = entry.get()
                        tree.item(item_id, values=(tree.item(item_id, "values")[0], new_value))
                    entry.destroy()  # Destroy the entry widget
                    if button:
                        button.destroy()  # Destroy the button if it exists
                except tk.TclError:
                    pass  # Handle the case where the widget is already destroyed

            def on_return(event=None):
                """Uloží hodnotu při stisknutí Enter."""
                on_focus_out()

            entry.bind("<FocusOut>", on_focus_out)
            entry.bind("<Return>", on_return)

            if name in {"Footprint", "ERP"}:
                
                def on_button_click():
                    nonlocal button_clicked
                    button_clicked = True
                    #print(f"Footprint button clicked! Current value: {entry.get()}") vrací hodnotu text boxu
                    # Zde můžete přidat vlastní logiku, např. otevření dialogu


                # Pokud je položka Footprint nebo ERP, zobraz tlačítko
                button = tk.Button(tree, text="...", command=lambda: on_button_click())
                button.place(x=x + width - 25, y=y, width=25, height=height)

                # Skrytí tlačítka při ztrátě fokusu (kliknutí mimo)
                def on_click_outside(event):
                    """Handles clicks outside the entry widget."""
                    nonlocal button_clicked
                    try:
                        if entry.winfo_ismapped():  # Safely check if the widget is still there
                            widget = root.winfo_containing(event.x_root, event.y_root)  # Detekuje, na co bylo kliknuto
                            if widget == button:  # Pokud bylo kliknuto na tlačítko, ignoruj událost
                                return
                            if not button_clicked:
                                on_focus_out()  # Clean up
                            else:
                                button_clicked = False
                    except tk.TclError:
                        pass  # The widget might already be destroyed

                root.bind("<Button-1>", on_click_outside, add="+")

    def save_changes():
        """Uloží změny zpět do property_dict."""
        #update dictionary
        for item_id in tree.get_children():
            name, value = tree.item(item_id, "values")
            for key, prop in symbol_object.propertiesFinal.items():
                if prop["name"] == name:
                    prop["value"] = value
        
        #check if library selected
        if cbDestLibname.getvar('InternalSelected') == 'false':
            print ("Selected destination symbol library!")
            return
        
        #save to kicad.sym
        buttonSignal_SaveSymbol.send("ButtonSaveSymbol", action="clicked")
        print("Saved")
        #close this window
        root.destroy()
    
    libraries_whs_kicad = FileHandlerKicad.Static.get_existing_libs()
    
    root = tk.Tk()
    root.title("Editable Properties Viewer")

    frame_tree = ttk.Frame(root)
    frame_tree.grid(row=1, column=0, columnspan=3, padx=10, pady=0, sticky="nsew") 

    # Vytvoření stromového widgetu (Treeview) jako tabulky
    tree = ttk.Treeview(frame_tree, columns=("name", "value"), show="headings", height=25)
    tree.heading("name", text="Name")
    tree.heading("value", text="Value")
    tree.column("name", width=200)
    tree.column("value", width=600)

    # Naplnění tabulky daty
    def update_tree(): 
        tree.delete       
        for key, value in symbol_object.propertiesFinal.items():
            tree.insert("", tk.END, values=(value["name"], value["value"]))

    update_tree()
    tree.grid(row=1, column=0, columnspan=3, padx=10, pady=20, sticky="nsew")  # Proveďte roztažení

    # Přidání scrollbarů
    scrollbar_y = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.grid(row=1, column=3, sticky='ns')  # Vertikální scrollbar napravo

    scrollbar_x = ttk.Scrollbar(frame_tree, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=scrollbar_x.set)
    scrollbar_x.grid(row=2, column=0, columnspan=3, sticky='ew')  # Horizontální scrollbar pod tree view

    # Událost dvojkliku
    tree.bind("<Double-1>", on_double_click)

    
    signal_gui_lib_create_button_pressed = Signal()     
    fileHandler = FileHandlerKicad()   
    fileHandler.registerEventReceiverCreateLibrary(signal_gui_lib_create_button_pressed)
   
   
    def on_click_CreateLib():        
        library_path, library_name = select_library_path_and_name()
        kwargs = {"library_path": library_path, "library_name": library_name}
        print(type(kwargs))
        results = signal_gui_lib_create_button_pressed.send("GUI", **kwargs)
        print("All handlers finished:", results)

        nonlocal libraries_whs_kicad
        libraries_whs_kicad = results[0][1] 
        cbDestLibname['values'] = libraries_whs_kicad
        
    """def registerEventLibCreated(self, signal_lib_created):
        self.receiverLibCreated = EventReceiver(signal_lib_created, self.EventLibCreated)
    
    def unregisterEventLibCreated(self):
        self.receiverLibCreated.disconnect()

    def EventLibCreated(self, sender, **kwargs):
        nonlocal libraries_whs_kicad
        libraries_whs_kicad = kwargs['libraries_whs_kicad_collection'] #load_existing_lib_patches()
        cbDestLibname['values'] = libraries_whs_kicad
    """


    def select_library_path_and_name():
        root = tk.Tk()
        root.withdraw()  # Skryje hlavní okno aplikace

        # Dialog pro výběr cesty ke knihovně
        library_path = filedialog.askdirectory(title="Select Library Path",initialdir = symbol_object.config_json.config['library_final_folder'] )
        if not library_path:  # Pokud uživatel zruší dialog
            print("Library path selection cancelled.")
            return None, None

        # Dialog pro zadání názvu knihovny
        library_name = simpledialog.askstring("Library Name", "Enter the name of the library: whs_yyy")
        if not library_name:  # Pokud uživatel zruší dialog nebo nezadá nic
            print("Library name input cancelled.")
            return None, None

        return library_path, library_name
    
    # Create library selector
    def on_combobox_select(event):   
        cbDestLibname.setvar('InternalSelected','true')             
        symbol_object.set_destination_library(cbDestLibname.get())

    label1 = ttk.Label(root,text="Choose/add library")
    label1.grid(row=0,column=0,pady=5, padx=5, sticky='w')
    cbDestLibname = ttk.Combobox(root, values=libraries_whs_kicad, state="readonly", width=100)  # "readonly" zabraňuje přímému zápisu uživatelem
    cbDestLibname.grid(row=0, column=0, pady=5, padx=150, sticky='w')
    cbDestLibname.set("Select a library")  # Výchozí hodnota ComboBoxu
    cbDestLibname.setvar('InternalSelected','false')
    cbDestLibname.bind("<<ComboboxSelected>>", on_combobox_select)
    
    

    buttonSelectlibrary = tk.Button(root, text="Create new library",  command=lambda: on_click_CreateLib(), width=20 )
    buttonSelectlibrary.grid(row=0,column=2 ,pady=5, padx=100, sticky='w')

    # Přidání tlačítka pro uložení změn
    buttonSignal_SaveSymbol = Signal()
    symbol_object.registerEventReceiverSaveCmd(buttonSignal_SaveSymbol)
    save_button = tk.Button(root, text="Save Changes", command=save_changes)
    save_button.grid(row=2,column=1,pady=10)

    # Zajištění, že sloupce se roztáhnou, pokud je to potřeba
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_columnconfigure(3, weight=0)  # Sloupec pro scrollbar y, nemusí se roztahovat

    root.grid_rowconfigure(1, weight=1)  # Prostor pro Treeview se roztáhne
    root.grid_rowconfigure(2, weight=0)  # Horizontální scrollbar by neměl zabírat moc místa
    root.grid_rowconfigure(3, weight=0)  # Pro tlačítko uložení

    frame_tree.grid_rowconfigure(0, weight=0)  # Aby se Treeview roztáhlo
    frame_tree.grid_columnconfigure(0, weight=1)  # Aby se Treeview roztáhlo na šířku
    frame_tree.grid_columnconfigure(1, weight=0)  # Sloupec pro scrollbar y, nemusí se roztahovat

    root.mainloop()



