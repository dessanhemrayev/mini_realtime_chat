"""Тесты для Pydantic схем."""

import pytest
from pydantic import ValidationError

from app.schemas import MessageData, AuthorSchema, ChatMessageSchema, SystemMessageSchema


class TestMessageData:
    """Тесты для модели MessageData."""

    def test_valid_message(self):
        """Проверка валидного сообщения."""
        msg = MessageData(text="Hello", name="User")
        assert msg.text == "Hello"
        assert msg.name == "User"

    def test_empty_text(self):
        """Проверка что пустой текст не допускается."""
        with pytest.raises(ValidationError):
            MessageData(text="", name="User")

    def test_empty_name(self):
        """Проверка что пустое имя не допускается."""
        with pytest.raises(ValidationError):
            MessageData(text="Hello", name="")

    def test_long_text(self):
        """Проверка что длинный текст не допускается."""
        long_text = "a" * 5001
        with pytest.raises(ValidationError):
            MessageData(text=long_text, name="User")

    def test_long_name(self):
        """Проверка что длинное имя не допускается."""
        long_name = "a" * 101
        with pytest.raises(ValidationError):
            MessageData(text="Hello", name=long_name)

    def test_message_with_spaces(self):
        """Проверка сообщения с пробелами."""
        msg = MessageData(text="  Hello World  ", name="  User  ")
        assert msg.text == "  Hello World  "
        assert msg.name == "  User  "


class TestAuthorSchema:
    """Тесты для модели AuthorSchema."""

    def test_valid_author(self):
        """Проверка валидного автора."""
        author = AuthorSchema(
            author_id="user123",
            name="Иван",
            image="/avatar/user123.jpg"
        )
        assert author.author_id == "user123"
        assert author.name == "Иван"
        assert author.image == "/avatar/user123.jpg"

    def test_author_without_image(self):
        """Проверка автора без изображения."""
        author = AuthorSchema(author_id="user123", name="Иван")
        assert author.author_id == "user123"
        assert author.name == "Иван"
        assert author.image is None


class TestChatMessageSchema:
    """Тесты для модели ChatMessageSchema."""

    def test_valid_chat_message(self):
        """Проверка валидного чат-сообщения."""
        msg = ChatMessageSchema(
            author={
                "author_id": "user123",
                "name": "Иван",
                "image": "/avatar/user123.jpg"
            },
            text="Привет!",
            day="03.07.2026",
            time="14:30"
        )
        assert msg.author.author_id == "user123"
        assert msg.text == "Привет!"
        assert msg.day == "03.07.2026"
        assert msg.time == "14:30"

    def test_chat_message_dict(self):
        """Проверка преобразования сообщения в словарь."""
        msg = ChatMessageSchema(
            author={"author_id": "user123", "name": "Иван"},
            text="Test",
            day="03.07.2026",
            time="14:30"
        )
        msg_dict = dict(msg)
        assert isinstance(msg_dict, dict)
        assert "author" in msg_dict
        assert "text" in msg_dict
        assert msg_dict["text"] == "Test"


class TestSystemMessageSchema:
    """Тесты для модели SystemMessageSchema."""

    def test_valid_system_message(self):
        """Проверка валидного системного сообщения."""
        msg = SystemMessageSchema(message="Пользователь присоединился")
        assert msg.type == "system"
        assert msg.message == "Пользователь присоединился"

    def test_system_message_dict(self):
        """Проверка преобразования в словарь."""
        msg = SystemMessageSchema(message="Test system message")
        msg_dict = dict(msg)
        assert msg_dict["type"] == "system"
        assert msg_dict["message"] == "Test system message"
        assert isinstance(msg_dict, dict)
