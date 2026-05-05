import json
import tempfile
from pathlib import Path

import pytest

from src.utils import load_data_from_json


def test_load_valid_data():
    """Тест загрузки корректных данных из JSON"""
    test_data = [
        {
            "name": "Электроника",
            "description": "Различные электронные устройства",
            "products": [
                {"name": "Смартфон", "description": "Мощный смартфон", "price": 50000.0, "quantity": 10},
                {"name": "Ноутбук", "description": "Игровой ноутбук", "price": 80000.0, "quantity": 5},
            ],
        }
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as tmp_file:
        json.dump(test_data, tmp_file, ensure_ascii=False)
        tmp_file_path = tmp_file.name

    try:
        categories = load_data_from_json(tmp_file_path)

        assert len(categories) == 1
        assert categories[0].name == "Электроника"
        assert len(categories[0].products_list) == 2
        assert categories[0].products_list[0].name == "Смартфон"
        assert categories[0].products_list[0].price == 50000.0
        assert categories[0].products_list[0].quantity == 10

    finally:
        Path(tmp_file_path).unlink()


def test_load_empty_products():
    """Тест загрузки категории без продуктов"""
    test_data = [{"name": "Пустая категория", "description": "Категория без товаров", "products": []}]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as tmp_file:
        json.dump(test_data, tmp_file, ensure_ascii=False)
        tmp_file_path = tmp_file.name

    try:
        categories = load_data_from_json(tmp_file_path)

        assert len(categories) == 1
        assert len(categories[0].products_list) == 0

    finally:
        Path(tmp_file_path).unlink()


def test_file_not_found():
    """Тест на отсутствие файла"""
    with pytest.raises(FileNotFoundError):
        load_data_from_json("nonexistent_file.json")


def test_invalid_json():
    """Тест на некорректный JSON"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as tmp_file:
        tmp_file.write("{invalid json")
        tmp_file_path = tmp_file.name

    try:
        with pytest.raises(json.JSONDecodeError):
            load_data_from_json(tmp_file_path)
    finally:
        Path(tmp_file_path).unlink()


def test_multiple_categories():
    """Тест загрузки нескольких категорий"""
    test_data = [
        {
            "name": "Категория 1",
            "description": "Описание 1",
            "products": [{"name": "Товар 1", "description": "Описание товара 1", "price": 100.0, "quantity": 5}],
        },
        {
            "name": "Категория 2",
            "description": "Описание 2",
            "products": [{"name": "Товар 2", "description": "Описание товара 2", "price": 200.0, "quantity": 3}],
        },
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as tmp_file:
        json.dump(test_data, tmp_file, ensure_ascii=False)
        tmp_file_path = tmp_file.name

    try:
        categories = load_data_from_json(tmp_file_path)

        assert len(categories) == 2
        assert categories[0].name == "Категория 1"
        assert categories[1].name == "Категория 2"
        assert categories[0].products_list[0].price == 100.0

    finally:
        Path(tmp_file_path).unlink()


def test_load_data_with_unicode():
    """Тест загрузки данных с юникод символами"""
    test_data = [
        {
            "name": "Электроника",
            "description": "Различные устройства",
            "products": [{"name": "Смартфон ©", "description": "Мощный смартфон", "price": 50000.0, "quantity": 10}],
        }
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as tmp_file:
        json.dump(test_data, tmp_file, ensure_ascii=False)
        tmp_file_path = tmp_file.name

    try:
        categories = load_data_from_json(tmp_file_path)
        assert categories[0].products_list[0].name == "Смартфон ©"
    finally:
        Path(tmp_file_path).unlink()
