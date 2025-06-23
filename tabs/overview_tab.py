from tkinter import ttk
class OverviewTab(ttk.Frame):
    def __init__(self, parent, _map_widget):
        super().__init__(parent)
        ttk.Label(self, text="Przegląd – jeszcze pusto").pack(padx=10, pady=10)

    def refresh(self):
        pass
