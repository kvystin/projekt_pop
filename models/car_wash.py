"""
Model domenowy „Myjnia”.
Każdy obiekt ląduje w liście _registry, aby łatwo go pobierać z innych miejsc.
"""
from services.geolocation import get_coordinates

CAR_WASH_TYPES = ["Ręczna (Manualna)","Automatyczna – szczotkowa","Automatyczna – bezdotykowa","Tunelowa","Pętlowo-rotacyjna","Mobilna",]


class CarWash:
    _registry: list["CarWash"] = []

    def __init__(self, name: str, city: str, wash_type: str):
        self.name = name.title()
        self.city = city.title()
        self.wash_type = wash_type
        self.coordinates = get_coordinates(self.city)
        self.marker = None
        CarWash._registry.append(self)

    # publiczne API – zwrot listy wszystkich obiektów
    @classmethod
    def all(cls) -> list["CarWash"]:
        return cls._registry

    # alias do zachowania kompatybilności wstecznej
    @classmethod
    def get_all_instances(cls) -> list["CarWash"]:
        return cls._registry

    def update(self, name: str, city: str, wash_type: str) -> None:
        self.name, self.city, self.wash_type = name.title(), city.title(), wash_type
        self.coordinates = get_coordinates(self.city)
