import tkinter as tk
from tkinter import ttk, messagebox

from models.car_wash import CarWash, CAR_WASH_TYPES
from services.map_service import MapService


class CarWashTab(ttk.Frame):
    def __init__(self, parent, map_widget):
        super().__init__(parent)
        self.map_service = MapService(map_widget)
        # lista zakładek, które trzeba odświeżać po zmianach
        self.dependents: list = []
        # indeks wybranego elementu w listboxie
        self.sel: int | None = None

        # ormularz górny
        frm = ttk.Frame(self)
        frm.pack(fill="x", padx=4, pady=4)

        ttk.Label(frm, text="Nazwa").grid(row=0, column=0, sticky="e")
        ttk.Label(frm, text="Miasto").grid(row=0, column=2, sticky="e")
        ttk.Label(frm, text="Typ").grid(row=0, column=4, sticky="e")

        self.e_name = ttk.Entry(frm, width=15); self.e_name.grid(row=0, column=1)
        self.e_city = ttk.Entry(frm, width=15); self.e_city.grid(row=0, column=3)
        self.cb_type = ttk.Combobox(frm, values=CAR_WASH_TYPES,
                                    state="readonly", width=27)
        self.cb_type.grid(row=0, column=5)

        self.btn = ttk.Button(frm, text="Dodaj", command=self._save)
        self.btn.grid(row=0, column=6, padx=4)

        #lista
        self.lb = tk.Listbox(self, height=10)
        self.lb.pack(fill="both", expand=True, padx=4)
        self.lb.bind("<<ListboxSelect>>", self._pick)

        bar = ttk.Frame(self); bar.pack(fill="x", padx=4, pady=3)
        ttk.Button(bar, text="Usuń",    command=self._delete).pack(side="left")
        ttk.Button(bar, text="Wyczyść", command=self._clear).pack(side="right")

        self.refresh()

    # odświeża listę myjni i powiadamia zależne zakładki
    def refresh(self):
        self.lb.delete(0, tk.END)
        for w in CarWash.all():
            self.lb.insert(tk.END, f"{w.name} ({w.city}) – {w.wash_type}")
        for dep in self.dependents:
            if hasattr(dep, "refresh"):
                dep.refresh()

    # dodawanie lub zapisywanie zmian
    def _save(self):
        name, city, wtype = (self.e_name.get().strip(),
                             self.e_city.get().strip(),
                             self.cb_type.get().strip())
        if not (name and city and wtype):
            messagebox.showwarning("Błąd", "Wszystkie pola są wymagane")
            return

        if self.sel is None:                  # dodawanie
            wash = CarWash(name, city, wtype)
        else:                                 # edycja
            wash = CarWash.all()[self.sel]
            if wash.marker:
                self.map_service.remove_marker(wash.marker)
            wash.update(name, city, wtype)

        # marker w domyślnym kolorze
        wash.marker = self.map_service.add_marker(*wash.coordinates, label=wash.name)
        self.refresh(); self._clear()

    # wybór elementu z listy
    def _pick(self, _):
        sel = self.lb.curselection()
        if not sel: return
        self.sel = sel[0]
        w = CarWash.all()[self.sel]
        self.e_name.delete(0, tk.END); self.e_name.insert(0, w.name)
        self.e_city.delete(0, tk.END); self.e_city.insert(0, w.city)
        self.cb_type.set(w.wash_type)
        self.btn.config(text="Zapisz")

    # usunięcie
    def _delete(self):
        sel = self.lb.curselection()
        if not sel: return
        w = CarWash.all().pop(sel[0])
        if w.marker:
            self.map_service.remove_marker(w.marker)
        self.refresh(); self._clear()

    # wyczyszczenie formularza
    def _clear(self):
        self.e_name.delete(0, tk.END)
        self.e_city.delete(0, tk.END)
        self.cb_type.set("")
        self.btn.config(text="Dodaj")
        self.sel = None
