import pytest
from unittest.mock import patch

from src.models import Category, LawnGrass, Product, Smartphone


@pytest.fixture
def sample_products():
    return [
        Product("Phone", "Smartphone", 999.99, 10),
        Product("Laptop", "Gaming laptop", 1999.99, 5),
    ]


def test_product_init():
    product = Product("TV", "Smart TV", 500.0, 3)

    assert product.name == "TV"
    assert product.description == "Smart TV"
    assert product.price == 500.0
    assert product.quantity == 3


def test_category_init(sample_products):
    category = Category("Electronics", "Devices", sample_products)
    assert category.name == "Electronics"
    assert category.description == "Devices"
    assert len(category.products_list) == 2  # Используем products_list


def test_category_count(sample_products):
    Category.category_count = 0

    Category("Cat1", "Desc", sample_products)
    Category("Cat2", "Desc", sample_products)

    assert Category.category_count == 2


def test_product_count(sample_products):
    Category.product_count = 0

    Category("Cat1", "Desc", sample_products)
    Category("Cat2", "Desc", sample_products)

    assert Category.product_count == 4


def test_add_product():
    category = Category("Test", "Desc", [])
    product = Product("Test", "Desc", 100, 1)

    category.add_product(product)

    assert "Test" in category.products


def test_price_setter():
    product = Product("Test", "Desc", 100, 1)

    product.price = -10

    assert product.price == 100


def test_price_setter_lower_price_confirmed():
    """Тест понижения цены с подтверждением"""
    product = Product("Test", "Desc", 100, 1)

    with patch('builtins.input', return_value='y'):
        product.price = 80

    assert product.price == 80


def test_price_setter_lower_price_cancelled():
    """Тест понижения цены с отменой"""
    product = Product("Test", "Desc", 100, 1)

    with patch('builtins.input', return_value='n'):
        product.price = 80

    assert product.price == 100  # Цена не изменилась


def test_price_setter_higher_price():
    """Тест повышения цены"""
    product = Product("Test", "Desc", 100, 1)

    product.price = 150

    assert product.price == 150


def test_new_product():
    data = {
        "name": "Phone",
        "description": "Smartphone",
        "price": 1000,
        "quantity": 5,
    }

    product = Product.new_product(data)

    assert product.name == "Phone"


def test_new_product_update_existing():
    """Тест обновления существующего продукта"""
    existing_products = [
        Product("Phone", "Smartphone", 1000, 5)
    ]

    new_data = {
        "name": "Phone",
        "description": "Smartphone",
        "price": 1200,  # Больше, чем было
        "quantity": 3,  # Добавляем 3 к существующим 5
    }

    updated_product = Product.new_product(new_data, existing_products)

    assert updated_product.quantity == 8  # 5 + 3
    assert updated_product.price == 1200  # Обновилась на большую цену


def test_new_product_update_existing_lower_price():
    """Тест обновления существующего с более низкой ценой"""
    existing_products = [
        Product("Phone", "Smartphone", 1000, 5)
    ]

    new_data = {
        "name": "Phone",
        "description": "Smartphone",
        "price": 800,  # Меньше, чем было
        "quantity": 3,
    }

    updated_product = Product.new_product(new_data, existing_products)

    assert updated_product.quantity == 8
    assert updated_product.price == 1000  # Цена осталась старая (больше)


def test_product_eq():
    """Тест сравнения продуктов"""
    product1 = Product("Phone", "Desc", 100, 5)
    product2 = Product("Phone", "Desc", 200, 3)
    product3 = Product("Laptop", "Desc", 500, 2)

    assert product1 == product2  # Одинаковые имена
    assert product1 != product3
    assert product1 == "Phone"  # Со строкой
    assert product1 != "Laptop"


def test_product_str():
    """Тест строкового представления продукта"""
    product = Product("Phone", "Desc", 100, 5)
    expected = "Phone, 100 руб. Остаток: 5 шт."
    assert str(product) == expected


def test_product_add():
    """Тест сложения продуктов"""
    product1 = Product("Phone", "Desc", 100, 5)
    product2 = Product("Phone", "Desc", 200, 3)

    result = product1 + product2
    expected = 100 * 5 + 200 * 3  # 500 + 600 = 1100
    assert result == expected


def test_product_add_different_types():
    """Тест сложения разных типов продуктов"""
    phone = Smartphone("iPhone", "Desc", 1000, 5, 90, "X", 128, "Black")
    grass = LawnGrass("Grass", "Desc", 100, 20, "USA", "7 days", "Green")

    with pytest.raises(TypeError):
        phone + grass


def test_smartphone_init():
    phone = Smartphone("iPhone", "Desc", 1000, 5, 95.5, "15 Pro", 256, "Black")

    assert phone.name == "iPhone"
    assert phone.model == "15 Pro"


def test_lawngrass_init():
    grass = LawnGrass("Grass", "Desc", 100, 20, "USA", "7 days", "Green")

    assert grass.country == "USA"


def test_add_invalid_product():
    category = Category("Test", "Desc", [])

    with pytest.raises(TypeError):
        category.add_product("not a product")


def test_category_str():
    """Тест строкового представления категории"""
    products = [
        Product("Phone", "Desc", 100, 5),
        Product("Laptop", "Desc", 500, 3)
    ]
    category = Category("Electronics", "Devices", products)

    expected = "Electronics, количество продуктов: 8 шт."
    assert str(category) == expected


def test_category_products_property():
    """Тест свойства products (с выводом в строку)"""
    products = [
        Product("Phone", "Desc", 100, 5),
        Product("Laptop", "Desc", 500, 3)
    ]
    category = Category("Electronics", "Devices", products)

    expected = "Phone, 100 руб. Остаток: 5 шт.\nLaptop, 500 руб. Остаток: 3 шт."
    assert category.products == expected


def test_category_products_list_property():
    """Тест свойства products_list (приватный список)"""
    products = [Product("Phone", "Desc", 100, 5)]
    category = Category("Electronics", "Devices", products)

    assert len(category.products_list) == 1
    assert category.products_list[0].name == "Phone"

pass