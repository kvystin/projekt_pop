"""
Zakładka „Pracownicy” – CRUD.
"""
import tkinter as tk
from tkinter import ttk, messagebox

from models.employee import Employee
from models.car_wash import CarWash
from services.map_service import MapService
from services.geolocation import get_coordinates


class EmployeeTab(ttk.Frame):
    def __init__(self, parent, map_widget, overview_tab=None):
        super().__init__(parent)

        self.map_service = MapService(map_widget)
        self.overview_tab = overview_tab
        self.selected: int | None = None

        form = ttk.Frame(self); form.pack(fill="x", padx=4, pady=4)
        for col, txt in enumerate(("Imię", "Nazwisko", "Miasto", "Myjnia")):
            ttk.Label(form, text=txt).grid(row=0, column=col*2, sticky="e")

        self.e_first = ttk.Entry(form, width=14); self.e_first.grid(row=0, column=1)
        self.e_last  = ttk.Entry(form, width=14); self.e_last.grid(row=0, column=3)
        self.e_city  = ttk.Entry(form, width=14); self.e_city.grid(row=0, column=5)
        self.cb_wash = ttk.Combobox(form, state="readonly", width=16); self.cb_wash.grid(row=0, column=7)

        self.btn_save = ttk.Button(form, text="Dodaj", command=self._save)
        self.btn_save.grid(row=0, column=8, padx=3)

        self.lb = tk.Listbox(self, height=10)
        self.lb.pack(fill="both", expand=True, padx=4)
        self.lb.bind("<<ListboxSelect>>", self._pick)

        bar = ttk.Frame(self); bar.pack(fill="x", padx=4, pady=3)
        ttk.Button(bar, text="Usuń",    command=self._delete).pack(side="left")
        ttk.Button(bar, text="Wyczyść", command=self._clear).pack(side="right")

        self.refresh()

    def refresh(self):
        self.cb_wash["values"] = [w.name for w in CarWash.all()]
        if self.cb_wash.get() not in self.cb_wash["values"]:
            self.cb_wash.set("")
        self.lb.delete(0, tk.END)
        for emp in Employee.all():
            self.lb.insert(tk.END, emp.full_name())

    def _save(self):
        first = self.e_first.get().strip()
        last  = self.e_last.get().strip()
        city  = self.e_city.get().strip()
        wash  = self.cb_wash.get().strip()

        if not all([first, last, city, wash]):
            messagebox.showwarning("Błąd", "Wszystkie pola są wymagane")
            return

        if self.selected is None:
            emp = Employee(first, last, city, wash)
        else:
            emp = Employee.all()[self.selected]
            if emp.marker:
                self.map_service.remove_marker(emp.marker)
            emp.update(first, last, city, wash)

        lat, lon = get_coordinates(city)
        emp.marker = self.map_service.add_marker(lat, lon, label=emp.full_name())

        self.refresh()
        if self.overview_tab: self.overview_tab.refresh()
        self._clear()

    def _pick(self, _):
        sel = self.lb.curselection()
        if not sel: return
        self.selected = sel[0]; e = Employee.all()[self.selected]
        self.e_first.delete(0, tk.END); self.e_first.insert(0, e.first_name)
        self.e_last.delete(0, tk.END);  self.e_last.insert(0, e.last_name)
        self.e_city.delete(0, tk.END);  self.e_city.insert(0, e.city)
        self.cb_wash.set(e.assigned_car_wash)
        self.btn_save.config(text="Zapisz")

    def _delete(self):
        sel = self.lb.curselection()
        if not sel: return
        e = Employee.all().pop(sel[0])
        if e.marker:
            self.map_service.remove_marker(e.marker)
        self.refresh()
        if self.overview_tab: self.overview_tab.refresh()
        self._clear()

    def _clear(self):
        for ent in (self.e_first, self.e_last, self.e_city):
            ent.delete(0, tk.END)
        self.cb_wash.set("")
        self.btn_save.config(text="Dodaj")
        self.selected = None
