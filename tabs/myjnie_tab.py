import tkinter as tk
from tkinter import ttk

class CarWashTab(ttk.Frame):
    def __init__(self, parent, _map):
        super().__init__(parent)

        frm = ttk.Frame(self); frm.pack(fill="x", padx=4, pady=4)
        for col, text in enumerate(("Nazwa", "Miasto", "Typ")):
            ttk.Label(frm, text=text).grid(row=0, column=col*2, sticky="e")

        self.e_name = ttk.Entry(frm, width=16); self.e_name.grid(row=0, column=1)
        self.e_city = ttk.Entry(frm, width=16); self.e_city.grid(row=0, column=3)
        self.e_type = ttk.Entry(frm, width=16); self.e_type.grid(row=0, column=5)

        ttk.Button(frm, text="Dodaj").grid(row=0, column=6, padx=2)

        self.lb = tk.Listbox(self, height=10)
        self.lb.pack(fill="both", expand=True, padx=4, pady=4)
