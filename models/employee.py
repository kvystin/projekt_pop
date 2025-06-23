class Employee:
    _registry: list["Employee"] = []

    def __init__(self, first, last, city, wash):
        self.first_name, self.last_name = first.title(), last.title()
        self.city  = city.title()
        self.assigned_car_wash = wash
        Employee._registry.append(self)

    @classmethod
    def all(cls):
        return cls._registry

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
