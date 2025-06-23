import tkinter as tk
from tkinter import ttk
import tkintermapview

from tabs.myjnie_tab import CarWashTab

def main() -> None:
    root = tk.Tk()
    root.title("System myjni")
    root.geometry("1200x700")

    # mapa
    map_widget = tkintermapview.TkinterMapView(root, width=1200, height=350)
    map_widget.pack(fill="x")

    # notebook
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)
    notebook.add(CarWashTab(notebook, map_widget), text="Myjnie")

    root.mainloop()
