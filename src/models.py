from abc import ABC, abstractmethod
from typing import List


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов"""

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass


class MixinRepr:
    """Миксин для вывода информации о создании объекта"""

    def __init__(self, *args, **kwargs):
        # Сохраняем параметры для __repr__
        self._args = args
        self._kwargs = kwargs

        # Выводим информацию о создании объекта
        print(f"Создан объект {self.__class__.__name__} с параметрами: {args}, {kwargs}")
        # Вызываем следующий конструктор в цепочке наследования
        super().__init__()

    def __repr__(self):
        """Возвращает строку с информацией о создании объекта"""
        class_name = self.__class__.__name__

        # Формируем строку параметров
        params = []
        if hasattr(self, "_args"):
            for arg in self._args:
                params.append(repr(arg))
        if hasattr(self, "_kwargs"):
            for key, value in self._kwargs.items():
                params.append(f"{key}={repr(value)}")

        return f"{class_name}({', '.join(params)})"


class Product(BaseProduct, MixinRepr):
    def __init__(self, name: str, description: str, price: float, quantity: int):
        # Проверка на нулевое количество
        if quantity <= 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

        super().__init__(name, description, price, quantity)

        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        if isinstance(other, Product):
            return self.name == other.name
        return False

    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать разные типы продуктов")

        return self.price * self.quantity + other.price * other.quantity

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    @classmethod
    def new_product(cls, data: dict, products: list["Product"] | None = None):
        if products:
            for product in products:
                if product.name == data["name"]:
                    product.quantity += data["quantity"]
                    product.price = max(product.price, data["price"])
                    return product

        return cls(
            data["name"],
            data["description"],
            data["price"],
            data["quantity"],
        )

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if value < self.__price:
            answer = input("Вы уверены, что хотите понизить цену? (y/n): ")
            if answer != "y":
                return

        self.__price = value


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List["Product"]):
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только продукты или их наследников")

        self.__products.append(product)
        Category.product_count += 1

    def middle_price(self) -> float:
        """Подсчитывает средний ценник всех товаров в категории"""
        try:
            total_price = sum(product.price for product in self.__products)
            return total_price / len(self.__products)
        except ZeroDivisionError:
            return 0

    @property
    def products_list(self):
        return self.__products

    @property
    def products(self):
        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result.strip()


class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color
