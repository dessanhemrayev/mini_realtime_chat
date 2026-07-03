"""Тесты для ConnectionManager."""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock

from app.managers import ConnectionManager


class TestConnectionManager:
    """Тесты для менеджера подключений."""

    def test_initialization(self):
        """Проверка инициализации менеджера."""
        manager = ConnectionManager()
        assert isinstance(manager.rooms, dict)
        assert len(manager.rooms) == 0

    @pytest.mark.asyncio
    async def test_connect(self):
        """Проверка подключения пользователя."""
        manager = ConnectionManager()
        websocket = AsyncMock()
        
        await manager.connect("room1", websocket)
        
        assert "room1" in manager.rooms
        assert websocket in manager.rooms["room1"]["users"]
        assert len(manager.rooms["room1"]["users"]) == 1
        websocket.accept.assert_called_once()

    @pytest.mark.asyncio
    async def test_connect_multiple_users(self):
        """Проверка подключения нескольких пользователей."""
        manager = ConnectionManager()
        ws1 = AsyncMock()
        ws2 = AsyncMock()
        
        await manager.connect("room1", ws1)
        await manager.connect("room1", ws2)
        
        assert len(manager.rooms["room1"]["users"]) == 2

    @pytest.mark.asyncio
    async def test_disconnect(self):
        """Проверка отключения пользователя."""
        manager = ConnectionManager()
        websocket = AsyncMock()
        
        await manager.connect("room1", websocket)
        assert len(manager.rooms["room1"]["users"]) == 1
        
        manager.disconnect("room1", websocket)
        
        # После отключения последнего пользователя, комната должна быть удалена
        assert "room1" not in manager.rooms

    @pytest.mark.asyncio
    async def test_disconnect_removes_empty_room(self):
        """Проверка удаления пустой комнаты."""
        manager = ConnectionManager()
        websocket = AsyncMock()
        
        await manager.connect("room1", websocket)
        manager.disconnect("room1", websocket)
        
        assert "room1" not in manager.rooms

    @pytest.mark.asyncio
    async def test_send_personal_message(self):
        """Проверка отправки персонального сообщения."""
        manager = ConnectionManager()
        websocket = AsyncMock()
        
        await manager.send_personal_message("Hello", websocket)
        
        websocket.send_text.assert_called_once_with("Hello")

    @pytest.mark.asyncio
    async def test_broadcast(self):
        """Проверка трансляции сообщения."""
        manager = ConnectionManager()
        ws1 = AsyncMock()
        ws2 = AsyncMock()
        
        await manager.connect("room1", ws1)
        await manager.connect("room1", ws2)
        
        message = {"text": "Hello all"}
        await manager.broadcast("room1", message)
        
        ws1.send_json.assert_called_with(message)
        ws2.send_json.assert_called_with(message)

    @pytest.mark.asyncio
    async def test_broadcast_nonexistent_room(self):
        """Проверка трансляции в несуществующую комнату."""
        manager = ConnectionManager()
        message = {"text": "Hello"}
        
        # Не должно вызвать ошибку
        await manager.broadcast("nonexistent", message)

    def test_add_message(self):
        """Проверка добавления сообщения в историю."""
        manager = ConnectionManager()
        websocket = AsyncMock()
        message = {"text": "Hello"}
        
        # Сначала создаем комнату
        manager.rooms["room1"] = {"users": [], "messages": []}
        manager.add_message("room1", message, websocket)
        
        assert len(manager.rooms["room1"]["messages"]) == 1
        assert manager.rooms["room1"]["messages"][0]["message"] == message

    def test_get_room_messages(self):
        """Проверка получения сообщений комнаты."""
        manager = ConnectionManager()
        websocket = AsyncMock()
        message = {"text": "Hello"}
        
        manager.rooms["room1"] = {"users": [], "messages": []}
        manager.add_message("room1", message, websocket)
        
        messages = manager.get_room_messages("room1")
        assert len(messages) == 1

    def test_get_room_messages_empty_room(self):
        """Проверка получения сообщений пустой комнаты."""
        manager = ConnectionManager()
        
        messages = manager.get_room_messages("nonexistent")
        assert messages == []

    def test_get_room_info(self):
        """Проверка получения информации о комнате."""
        manager = ConnectionManager()
        websocket = AsyncMock()
        
        asyncio.run(manager.connect("room1", websocket))
        info = manager.get_room_info("room1")
        
        assert info is not None
        assert info["room_id"] == "room1"
        assert info["users_count"] == 1
        assert info["messages_count"] == 0

    def test_get_room_info_nonexistent(self):
        """Проверка информации о несуществующей комнате."""
        manager = ConnectionManager()
        
        info = manager.get_room_info("nonexistent")
        assert info is None
