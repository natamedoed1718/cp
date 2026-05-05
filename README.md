# Проект: Категории и продукты

##  Описание проекта

В рамках данного проекта реализована базовая модель интернет-магазина с использованием объектно-ориентированного программирования (ООП).

Реализованы две основные сущности:

* **Product (Продукт)** — описывает товар
* **Category (Категория)** — объединяет товары в группы

Проект включает:

* классы с атрибутами и инициализацией
* атрибуты класса для подсчёта объектов
* тестирование с использованием pytest
* настройку линтеров и форматеров
* работу с виртуальным окружением через Poetry

---

## ⚙ Используемые технологии

* Python 3.14
* Poetry (управление зависимостями)
* pytest (тестирование)
* pytest-cov (покрытие тестами)
* flake8 (линтер)
* black (форматирование кода)
* isort (сортировка импортов)

---

##  Структура проекта

```
c_and_p/
├── shop_pr/
│   ├── __init__.py
│   ├── models.py
│   └── utils.py
├── tests/
│   └── test_models.py
├── main.py
├── pyproject.toml
└── README.md
```

---

##  Реализованные классы

###  Product

Содержит:

* `name` — название товара
* `description` — описание
* `price` — цена (float)
* `quantity` — количество на складе (int)

---

###  Category

Содержит:

* `name` — название категории
* `description` — описание
* `products` — список объектов Product

Атрибуты класса:

* `category_count` — количество категорий
* `product_count` — общее количество товаров

---

##  Тестирование

Для тестирования используется pytest.

Проверяется:

* корректность инициализации Product
* корректность инициализации Category
* подсчёт количества категорий
* подсчёт количества товаров

###  Запуск тестов

```
pytest
```

---

##  Покрытие тестами

Для анализа покрытия используется pytest-cov.

###  Запуск:

```
pytest --cov=shop_pr --cov-report=term-missing --cov-report=html
```

После выполнения будет создан отчёт:

```
htmlcov/index.html
```

---

##  Качество кода

Используются инструменты:

### Проверка:

```
flake8 .
```

### Форматирование:

```
black .
```

### Сортировка импортов:

```
isort .
```

---

##  Установка и запуск

### 1. Клонировать репозиторий

```
git clone <repo_url>
cd c_and_p
```

### 2. Установить зависимости

```
poetry install
```

### 3. Активировать окружение

```
poetry shell
```

### 4. Запустить тесты

```
pytest
```

---

##  Запуск примера

Файл `main.py` демонстрирует работу классов:

```
python main.py
```

---

##  Дополнительно

Реализована функция загрузки данных из JSON:

* чтение файла
* создание объектов Product и Category

---


 Наследование и новые классы
В рамках развития проекта добавлены два класса-наследника от Product:

📱 Smartphone (Смартфон)
Дополнительные атрибуты:

Атрибут	Тип	Описание
efficiency	float	Производительность (ГГц)
model	str	Модель устройства
memory	int	Объем встроенной памяти (ГБ)
color	str	Цвет
Пример создания:

python
iphone = Smartphone(
    name="iPhone 15",
    description="Флагманский смартфон",
    price=999.99,
    quantity=25,
    efficiency=3.8,
    model="A2849",
    memory=256,
    color="Black"
)
 LawnGrass (Трава газонная)
Дополнительные атрибуты:

Атрибут	Тип	Описание
country	str	Страна-производитель
germination_period	int	Срок прорастания (дни)
color	str	Цвет
Пример создания:

python
grass = LawnGrass(
    name="Изумрудная",
    description="Газонная трава для тени",
    price=15.99,
    quantity=100,
    country="Нидерланды",
    germination_period=14,
    color="Green"
)
➕ Перегрузка оператора сложения (__add__)
Реализована возможность сложения товаров с проверкой типов.

Правила сложения:
Ситуация	Результат
Smartphone + Smartphone	 Сумма цен
LawnGrass + LawnGrass	 Сумма цен
Smartphone + LawnGrass	 TypeError
Product + Product (разные наследники)	 TypeError
Пример использования:
python
phone1 = Smartphone(..., price=50000)
phone2 = Smartphone(..., price=60000)
total = phone1 + phone2  # 110000

grass1 = LawnGrass(..., price=1000)
grass2 = LawnGrass(..., price=1500)
total_grass = grass1 + grass2  # 2500

# Ошибка:
result = phone1 + grass1  # TypeError: Нельзя складывать товары разных классов
️ Защита добавления продуктов в категорию
Метод добавления продукта в категорию теперь проверяет тип добавляемого объекта.

Правила:
Добавляемый объект	Результат
Product или его наследник	 Добавляется
Любой другой тип (int, str, list и т.д.)	 TypeError
Пример использования:
python
category = Category("Электроника", "Устройства", [])

phone = Smartphone(...)
grass = LawnGrass(...)

category.add_product(phone)   # 
category.add_product(grass)   # 
category.add_product("телефон")  #  TypeError
 Тестирование новой функциональности
1. Тесты для классов-наследников
python
def test_smartphone_init():
    phone = Smartphone("iPhone", "desc", 999.99, 10, 3.8, "A2849", 256, "Black")
    assert phone.efficiency == 3.8
    assert phone.model == "A2849"
    assert phone.memory == 256
    assert phone.color == "Black"

def test_lawn_grass_init():
    grass = LawnGrass("Grass", "desc", 15.99, 100, "Нидерланды", 14, "Green")
    assert grass.country == "Нидерланды"
    assert grass.germination_period == 14
    assert grass.color == "Green"
2. Тесты для __add__
python
def test_add_same_types():
    phone1 = Smartphone("iPhone", "desc", 50000, 10, 3.8, "A2849", 256, "Black")
    phone2 = Smartphone("Samsung", "desc", 60000, 5, 3.9, "S24", 512, "White")
    assert phone1 + phone2 == 110000

def test_add_different_types_raises_error():
    phone = Smartphone("iPhone", "desc", 50000, 10, 3.8, "A2849", 256, "Black")
    grass = LawnGrass("Grass", "desc", 1000, 100, "NL", 14, "Green")
    
    with pytest.raises(TypeError) as exc:
        result = phone + grass
    assert "Нельзя складывать товары разных классов" in str(exc.value)
3. Тесты для защищённого добавления
python
def test_add_product_type_check():
    category = Category("Electronics", "Devices", [])
    phone = Smartphone("iPhone", "desc", 999.99, 10, 3.8, "A2849", 256, "Black")
    
    category.add_product(phone)  #  не должно быть ошибки
    assert len(category.products) == 1
    
    with pytest.raises(TypeError):
        category.add_product("not a product")  # 
 Запуск всех тестов
bash
# Запуск всех тестов с покрытием
pytest --cov=shop_pr -v

# Запуск только тестов наследования
pytest tests/test_models.py -k "Smartphone or LawnGrass" -v

# Запуск тестов сложения
pytest tests/test_models.py -k "add" -v

# Запуск тестов проверки типов
pytest tests/test_models.py -k "type" -v
 Ожидаемое покрытие тестами
После добавления новой функциональности:

Модуль	Покрытие
models.py (Product)	100%
models.py (Smartphone)	100%
models.py (LawnGrass)	100%
models.py (Category)	100%
models.py (__add__)	100%
models.py (add_product)	100%
 Итоговый чек-лист выполнения
Реализован класс Smartphone (наследник Product)

Реализован класс LawnGrass (наследник Product)

Переопределён метод __add__ с проверкой типов через type()

Реализована защита метода add_product через isinstance()

Написаны тесты для всех новых классов и методов

Все старые тесты остаются зелёными 

🐛 Известные проблемы и решения
Проблема: zsh: command not found: pytest
Решение: Используйте poetry run pytest или активируйте виртуальное окружение:

bash
poetry run pytest
# или
poetry shell
pytest
Проблема: TypeError при сложении разных типов
Это ожидаемое поведение — так и задумано по заданию.

 Полезные ссылки
Документация pytest

Poetry — управление зависимостями

Наследование в Python

Магические методы (__add__)

## Управление товарами и категориями

### Задание 1: Абстрактный базовый класс BaseProduct
- Создан абстрактный класс `BaseProduct` с абстрактными методами `__str__` и `__add__`
- Классы `Product`, `Smartphone` и `LawnGrass` наследуются от `BaseProduct`
- Обеспечено единообразие интерфейса для всех продуктов

### Задание 2: Класс-миксин MixinRepr
- Реализован миксин `MixinRepr` для автоматического вывода информации о создании объектов
- Миксин добавлен в цепочку наследования класса `Product`
- При создании объекта выводится сообщение: `Создан объект Product с параметрами: (...)`
- Реализован метод `__repr__` для получения строкового представления объекта

### Задание 3: Тестирование
- Написаны тесты для новой функциональности
- Все существующие тесты успешно выполняются

##  Автор---

Проект выполнен в рамках учебного задания.