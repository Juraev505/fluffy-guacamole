
class Vehicle:
    def __init__(self, brand, year):
        self.brand = brand
        self.year = year

    def display_info(self):
        print(f"Марка: {self.brand}")
        print(f"Год выпуска: {self.year}")


class Car(Vehicle):
    def __init__(self, brand, year, num_doors):
        super().__init__(brand, year)
        self.num_doors = num_doors

    def display_info(self):
        super().display_info()
        print(f"Количество дверей: {self.num_doors}")


class Motorcycle(Vehicle):
    def __init__(self, brand, year, type_motorcycle):
        super().__init__(brand, year)
        self.type_motorcycle = type_motorcycle

    def display_info(self):
        super().display_info()
        print(f"Тип мотоцикла: {self.type_motorcycle}")

car = Car("Toyota", 2020, 4)
motorcycle = Motorcycle("Yamaha", 2022, "Спортивный")


print("Информация об автомобиле:")
car.display_info()

print("\nИнформация о мотоцикле:")
motorcycle.display_info()
