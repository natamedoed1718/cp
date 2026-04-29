import pytest

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
    assert len(category.products) == 2


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


def test_new_product():
    data = {
        "name": "Phone",
        "description": "Smartphone",
        "price": 1000,
        "quantity": 5,
    }

    product = Product.new_product(data)

    assert product.name == "Phone"


def test_smartphone_init():
    phone = Smartphone("iPhone", "Desc", 1000, 5, 95.5, "15 Pro", 256, "Black")

    assert phone.name == "iPhone"
    assert phone.model == "15 Pro"


def test_lawngrass_init():
    grass = LawnGrass("Grass", "Desc", 100, 20, "USA", "7 days", "Green")

    assert grass.country == "USA"


def test_add_different_types():
    phone = Smartphone("iPhone", "Desc", 1000, 5, 90, "X", 128, "Black")
    grass = LawnGrass("Grass", "Desc", 100, 20, "USA", "7 days", "Green")

    with pytest.raises(TypeError):
        phone + grass


def test_add_invalid_product():
    category = Category("Test", "Desc", [])

    with pytest.raises(TypeError):
        category.add_product("not a product")
