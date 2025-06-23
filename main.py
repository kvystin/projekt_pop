import tkinter as tk
from tkinter import ttk
import tkintermapview

from tabs.myjnie_tab     import CarWashTab
from tabs.klienci_tab    import ClientTab
from tabs.pracownicy_tab import EmployeeTab
from tabs.overview_tab   import OverviewTab


def main() -> None:
    root = tk.Tk()
    root.title("System zarządzania myjniami")
    root.geometry("1400x850")
    root.minsize(1100, 700)

    map_widget = tkintermapview.TkinterMapView(root, width=1400, height=500)
    map_widget.pack(fill="x")
    map_widget.set_position(52.2297, 21.0122)
    map_widget.set_zoom(6)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    tab_over = OverviewTab(notebook, map_widget)
    tab_wash = CarWashTab(notebook, map_widget)
    tab_cli  = ClientTab(notebook,  map_widget, tab_over)
    tab_emp  = EmployeeTab(notebook, map_widget, tab_over)

    tab_wash.dependents = [tab_cli, tab_emp, tab_over]

    notebook.add(tab_wash, text="Myjnie")
    notebook.add(tab_cli,  text="Klienci")
    notebook.add(tab_emp,  text="Pracownicy")
    notebook.add(tab_over, text="Przegląd")

    root.mainloop()


if __name__ == "__main__":
    main()
