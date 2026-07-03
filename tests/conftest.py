"""Конфигурация и fixtures для тестов."""

import pytest
from fastapi.testclient import TestClient

from app.managers import ConnectionManager


@pytest.fixture
def client():
    """Клиент для тестирования FastAPI приложения."""
    from main import app

    return TestClient(app)


@pytest.fixture
def connection_manager():
    """Инстанс ConnectionManager для тестирования."""
    return ConnectionManager()


@pytest.fixture
def sample_room_id():
    """Пример ID комнаты."""
    return "test_room_1"


@pytest.fixture
def sample_client_id():
    """Пример ID клиента."""
    return "test_user_1"


@pytest.fixture
def sample_message():
    """Пример сообщения."""
    return {"text": "Это тестовое сообщение", "name": "Тестовый пользователь"}
