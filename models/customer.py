class Customer:
    _registry: list["Customer"] = []

    def __init__(self, first: str, last: str, city: str, wash: str):
        self.first_name, self.last_name = first.title(), last.title()
        self.city  = city.title()
        self.assigned_car_wash = wash
        Customer._registry.append(self)

    @classmethod
    def all(cls):
        return cls._registry

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
