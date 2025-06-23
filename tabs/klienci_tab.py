from tkinter import ttk
class ClientTab(ttk.Frame):
    def __init__(self, parent, *_):
        super().__init__(parent)
        ttk.Label(self, text="Klienci – w budowie").pack(padx=10, pady=10)
