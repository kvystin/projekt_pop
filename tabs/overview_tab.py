from tkinter import ttk

from models.car_wash import CarWash
from models.customer import Customer
from models.employee import Employee


class OverviewTab(ttk.Frame):
    def __init__(self, parent, map_widget):
        super().__init__(parent)
        self.map_widget = map_widget

        self.tree = ttk.Treeview(self, columns=("type", "name"), show="tree headings")
        self.tree.heading("#0",   text="Obiekt")
        self.tree.heading("type", text="Typ")
        self.tree.heading("name", text="Nazwa / Imię")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self._jump)

        ttk.Button(self, text="Odśwież", command=self.refresh).pack(pady=4)
        self.refresh()

    # ----------------------------------------------------------
    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for wash in CarWash.all():
            wid = self.tree.insert("", "end",
                                   text=f"{wash.name} ({wash.city})",
                                   values=("Myjnia", wash.name))

            cid = self.tree.insert(wid, "end", text="Klienci")
            for c in Customer.all():
                if c.assigned_car_wash == wash.name:
                    self.tree.insert(cid, "end", text="",
                                     values=("Klient", c.full_name()))

            eid = self.tree.insert(wid, "end", text="Pracownicy")
            for e in Employee.all():
                if e.assigned_car_wash == wash.name:
                    self.tree.insert(eid, "end", text="",
                                     values=("Pracownik", e.full_name()))

    # ----------------------------------------------------------
    def _jump(self, _evt):
        iid = self.tree.focus()
        if not iid: return
        typ, name = self.tree.item(iid, "values")

        if typ == "Myjnia":
            w = next(w for w in CarWash.all() if w.name == name)
            self._center(*w.coordinates, 10)
        elif typ == "Klient":
            c = next(c for c in Customer.all() if c.full_name() == name)
            self._center(*c.coordinates, 12)
        elif typ == "Pracownik":
            e = next(e for e in Employee.all() if e.full_name() == name)
            self._center(*e.coordinates, 12)

    def _center(self, lat, lon, zoom):
        self.map_widget.set_position(lat, lon)
        self.map_widget.set_zoom(zoom)
