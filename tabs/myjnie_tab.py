from tkinter import ttk

class CarWashTab(ttk.Frame):
    def __init__(self, parent, _map):
        super().__init__(parent)
        ttk.Label(self, text="Myjnie – w budowie").pack(padx=10, pady=10)
