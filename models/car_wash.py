class CarWash:
    _registry: list["CarWash"] = []

    def __init__(self, name: str, city: str, wash_type: str):
        self.name      = name.title()
        self.city      = city.title()
        self.wash_type = wash_type
        CarWash._registry.append(self)

    @classmethod
    def all(cls) -> list["CarWash"]:
        return cls._registry
