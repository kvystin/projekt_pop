import tkinter as tk
from tkinter import ttk

from models.car_wash import CarWash
from models.customer import Customer
from models.employee import Employee


class OverviewTab(ttk.Frame):
    def __init__(self, parent, map_widget):
        super().__init__(parent)
        self.map_widget = map_widget

        # TreeView z kolumnami: typ i nazwa/imię
        self.tree = ttk.Treeview(self, columns=("type", "name"), show="tree headings")
        self.tree.heading("#0",   text="Obiekt")
        self.tree.heading("type", text="Typ")
        self.tree.heading("name", text="Nazwa / Imię")
        self.tree.pack(fill="both", expand=True)
        # dwuklik → funkcja _jump centrowała mapę
        self.tree.bind("<Double-1>", self._jump)

        ttk.Button(self, text="Odśwież", command=self.refresh).pack(pady=4)

        self.refresh()

    # buduje drzewo od zera
    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for wash in CarWash.all():
            # główny węzeł – myjnia
            wid = self.tree.insert("", "end",
                                   text=f"{wash.name} ({wash.city})",
                                   values=("Myjnia", wash.name))

            # podwęzeł „Klienci”
            cid = self.tree.insert(wid, "end", text="Klienci")
            for cust in Customer.all():
                if cust.assigned_car_wash == wash.name:
                    self.tree.insert(cid, "end", text="",
                                     values=("Klient", cust.full_name()))

            # podwęzeł „Pracownicy”
            eid = self.tree.insert(wid, "end", text="Pracownicy")
            for emp in Employee.all():
                if emp.assigned_car_wash == wash.name:
                    self.tree.insert(eid, "end", text="",
                                     values=("Pracownik", emp.full_name()))

    # reakcja na dwuklik w TreeView – centrowanie mapy
    def _jump(self, _event):
        item_id = self.tree.focus()
        if not item_id:
            return
        obj_type, name = self.tree.item(item_id, "values")

        if obj_type == "Myjnia":
            wash = next(w for w in CarWash.all() if w.name == name)
            self._center_map(*wash.coordinates, zoom=10)
        elif obj_type == "Klient":
            cust = next(c for c in Customer.all() if c.full_name() == name)
            self._center_map(*cust.coordinates, zoom=12)
        elif obj_type == "Pracownik":
            emp = next(e for e in Employee.all() if e.full_name() == name)
            self._center_map(*emp.coordinates, zoom=12)

    # pomocnicza metoda do ustawiania widoku mapy
    def _center_map(self, lat: float, lon: float, zoom: int):
        self.map_widget.set_position(lat, lon)
        self.map_widget.set_zoom(zoom)
