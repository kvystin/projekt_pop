import tkinter as tk
from tkinter import ttk, messagebox

from models.car_wash import CarWash
from services.map_service import MapService
from services.geolocation import get_coordinates


class CarWashTab(ttk.Frame):
    def __init__(self, parent, map_widget):
        super().__init__(parent)

        self.map_service = MapService(map_widget)
        self.selected: int | None = None

        # ── formularz ────────────────────────────────────────────
        form = ttk.Frame(self); form.pack(fill="x", padx=4, pady=4)
        for col, txt in enumerate(("Nazwa", "Miasto", "Typ")):
            ttk.Label(form, text=txt).grid(row=0, column=col*2, sticky="e")

        self.e_name = ttk.Entry(form, width=18); self.e_name.grid(row=0, column=1)
        self.e_city = ttk.Entry(form, width=18); self.e_city.grid(row=0, column=3)
        self.e_type = ttk.Entry(form, width=18); self.e_type.grid(row=0, column=5)

        self.btn_save = ttk.Button(form, text="Dodaj", command=self._save)
        self.btn_save.grid(row=0, column=6, padx=3)

        # ── lista ────────────────────────────────────────────────
        self.lb = tk.Listbox(self, height=10)
        self.lb.pack(fill="both", expand=True, padx=4)
        self.lb.bind("<<ListboxSelect>>", self._pick)

        bar = ttk.Frame(self); bar.pack(fill="x", padx=4, pady=3)
        ttk.Button(bar, text="Usuń",    command=self._delete).pack(side="left")
        ttk.Button(bar, text="Wyczyść", command=self._clear).pack(side="right")

        self.refresh()

    # ------------------------------------------------------------
    def refresh(self):
        self.lb.delete(0, tk.END)
        for w in CarWash.all():
            self.lb.insert(tk.END, f"{w.name} ({w.city}) – {w.wash_type}")

    # ------------------------------------------------------------
    def _save(self):
        name, city, typ = (self.e_name.get().strip(),
                           self.e_city.get().strip(),
                           self.e_type.get().strip())
        if not (name and city and typ):
            messagebox.showwarning("Błąd", "Wszystkie pola są wymagane")
            return

        if self.selected is None:
            wash = CarWash(name, city, typ)
        else:
            wash = CarWash.all()[self.selected]
            if wash.marker:
                self.map_service.remove_marker(wash.marker)
            wash.update(name, city, typ)

        lat, lon = get_coordinates(wash.city)
        wash.coordinates = [lat, lon]
        wash.marker = self.map_service.add_marker(lat, lon, label=wash.name)

        self.refresh(); self._clear()

    # ------------------------------------------------------------
    def _pick(self, _):
        sel = self.lb.curselection()
        if not sel: return
        self.selected = sel[0]; w = CarWash.all()[self.selected]
        self.e_name.delete(0, tk.END); self.e_name.insert(0, w.name)
        self.e_city.delete(0, tk.END); self.e_city.insert(0, w.city)
        self.e_type.delete(0, tk.END); self.e_type.insert(0, w.wash_type)
        self.btn_save.config(text="Zapisz")

    # ------------------------------------------------------------
    def _delete(self):
        sel = self.lb.curselection()
        if not sel: return
        w = CarWash.all().pop(sel[0])
        if w.marker:
            self.map_service.remove_marker(w.marker)
        self.refresh(); self._clear()

    def _clear(self):
        for e in (self.e_name, self.e_city, self.e_type):
            e.delete(0, tk.END)
        self.btn_save.config(text="Dodaj")
        self.selected = None
