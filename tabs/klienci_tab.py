import tkinter as tk
from tkinter import ttk, messagebox

from models.customer import Customer
from models.car_wash import CarWash
from services.map_service import MapService

class ClientTab(ttk.Frame):
    def __init__(self, parent, map_widget, overview_tab):
        super().__init__(parent)

        # serwis mapy odpowiada za obsługę markerów
        self.map_service = MapService(map_widget)

        # odwołanie do zakładki „Przegląd” – trzeba ją odświeżać po zmianach
        self.overview_tab = overview_tab

        # indeks zaznaczonego wiersza w Listboxie; None = tryb „Dodaj”
        self.selected_index: int | None = None


        form = ttk.Frame(self)
        form.pack(fill="x", padx=4, pady=4)

        for col, text in enumerate(("Imię", "Nazwisko", "Miasto", "Myjnia")):
            ttk.Label(form, text=text).grid(row=0, column=col * 2, sticky="e")

        self.entry_first = ttk.Entry(form, width=12)
        self.entry_last  = ttk.Entry(form, width=12)
        self.entry_city  = ttk.Entry(form, width=12)
        self.combo_wash  = ttk.Combobox(form, state="readonly", width=14)

        self.entry_first.grid(row=0, column=1)
        self.entry_last.grid(row=0,  column=3)
        self.entry_city.grid(row=0,  column=5)
        self.combo_wash.grid(row=0,  column=7)

        self.btn_add_save = ttk.Button(form, text="Dodaj", command=self._save)
        self.btn_add_save.grid(row=0, column=8, padx=2)

        # lista klientów
        self.listbox = tk.Listbox(self, height=10)
        self.listbox.pack(fill="both", expand=True, padx=4)
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

        # pasek przycisków pod listą
        bar = ttk.Frame(self)
        bar.pack(fill="x", padx=4, pady=3)
        ttk.Button(bar, text="Usuń",    command=self._delete).pack(side="left")
        ttk.Button(bar, text="Wyczyść", command=self._clear).pack(side="right")

        # inicjalne wczytanie danych
        self.refresh()

    # metoda odświeża combobox z myjniami i zawartość listboxa
    def refresh(self):
        # lista nazw myjni do wyboru
        self.combo_wash["values"] = [w.name for w in CarWash.all()]
        if self.combo_wash.get() not in self.combo_wash["values"]:
            self.combo_wash.set("")

        # przeładowanie listy
        self.listbox.delete(0, tk.END)
        for cust in Customer.all():
            self.listbox.insert(tk.END, cust.full_name())

    # zapisuje nowego lub edytowanego klienta
    def _save(self):
        first = self.entry_first.get().strip()
        last  = self.entry_last.get().strip()
        city  = self.entry_city.get().strip()
        wash  = self.combo_wash.get().strip()

        if not all([first, last, city, wash]):
            messagebox.showwarning("Błąd", "Wszystkie pola są wymagane")
            return

        if self.selected_index is None:
            # tworzymy nowy obiekt
            cust = Customer(first, last, city, wash)
        else:
            # modyfikujemy istniejący
            cust = Customer.all()[self.selected_index]
            if cust.marker:
                self.map_service.remove_marker(cust.marker)
            cust.update(first, last, city, wash)

        # stawiamy/odświeżamy marker
        cust.marker = self.map_service.add_marker(*cust.coordinates,
                                                  label=cust.full_name())

        # odśwież GUI
        self.refresh()
        self.overview_tab.refresh()
        self._clear()

    # reakcja na wybór wiersza w Listboxie (tryb edycji)
    def _on_select(self, _event):
        selected = self.listbox.curselection()
        if not selected:
            return
        self.selected_index = selected[0]
        cust = Customer.all()[self.selected_index]

        # wypełniamy pola formularza danymi klienta
        self.entry_first.delete(0, tk.END); self.entry_first.insert(0, cust.first_name)
        self.entry_last.delete(0,  tk.END); self.entry_last.insert(0,  cust.last_name)
        self.entry_city.delete(0,  tk.END); self.entry_city.insert(0,  cust.city)
        self.combo_wash.set(cust.assigned_car_wash)

        self.btn_add_save.config(text="Zapisz")

    # usuwa zaznaczonego klienta
    def _delete(self):
        selected = self.listbox.curselection()
        if not selected:
            return
        idx = selected[0]
        cust = Customer.all().pop(idx)
        if cust.marker:
            self.map_service.remove_marker(cust.marker)

        self.refresh()
        self.overview_tab.refresh()
        self._clear()

    # czyści formularz i przywraca tryb „Dodaj”
    def _clear(self):
        for entry in (self.entry_first, self.entry_last, self.entry_city):
            entry.delete(0, tk.END)
        self.combo_wash.set("")
        self.btn_add_save.config(text="Dodaj")
        self.selected_index = None
