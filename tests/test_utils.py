"""Тесты для утилит."""

import pytest
from app.utils import get_hash, instance_attributes


class TestGetHash:
    """Тесты для функции get_hash."""

    def test_hash_string(self):
        """Проверка хеширования строки."""
        result = get_hash("test")
        assert isinstance(result, str)
        assert len(result) == 7

    def test_hash_consistency(self):
        """Проверка консистентности хеша."""
        hash1 = get_hash("same_data")
        hash2 = get_hash("same_data")
        assert hash1 == hash2

    def test_different_data_different_hash(self):
        """Проверка что разные данные дают разные хеши."""
        hash1 = get_hash("data1")
        hash2 = get_hash("data2")
        assert hash1 != hash2

    def test_hash_dict(self):
        """Проверка хеширования словаря."""
        data = {"text": "hello"}
        result = get_hash(data)
        assert isinstance(result, str)
        assert len(result) == 7

    def test_hash_custom_length(self):
        """Проверка кастомной длины хеша."""
        result = get_hash("test", length=10)
        assert len(result) == 10

    def test_hash_number(self):
        """Проверка хеширования числа."""
        result = get_hash(123)
        assert isinstance(result, str)
        assert len(result) == 7


class TestInstanceAttributes:
    """Тесты для функции instance_attributes."""

    def test_simple_class(self):
        """Проверка получения атрибутов простого класса."""
        class SimpleClass:
            def __init__(self):
                self.attr1 = "value1"
                self.attr2 = "value2"

        obj = SimpleClass()
        attrs = instance_attributes(obj)
        assert isinstance(attrs, dict)
        assert attrs["attr1"] == "value1"
        assert attrs["attr2"] == "value2"

    def test_empty_class(self):
        """Проверка получения атрибутов пустого класса."""
        class EmptyClass:
            pass

        obj = EmptyClass()
        attrs = instance_attributes(obj)
        assert isinstance(attrs, dict)

    def test_builtin_type(self):
        """Проверка встроенного типа."""
        result = instance_attributes("string")
        assert isinstance(result, dict)

    def test_slots_class(self):
        """Проверка класса со слотами."""
        class SlotsClass:
            __slots__ = ["attr1", "attr2"]

            def __init__(self):
                self.attr1 = "value1"
                self.attr2 = "value2"

        obj = SlotsClass()
        attrs = instance_attributes(obj)
        assert "attr1" in attrs
        assert "attr2" in attrs
