"""Менеджер для управления WebSocket подключениями и комнатами чата."""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Управляет WebSocket подключениями и обменом сообщениями между пользователями."""

    def __init__(self):
        """Инициализация менеджера подключений."""
        # Структура: {room_id: {'users': [WebSocket, ...], 'messages': [...]}}
        self.rooms: Dict[str, Dict[str, Any]] = {}

    async def connect(self, room_id: str, websocket: WebSocket) -> None:
        """
        Подключить нового пользователя к комнате.

        Args:
            room_id: ID комнаты
            websocket: WebSocket соединение
        """
        await websocket.accept()

        if room_id not in self.rooms:
            self.rooms[room_id] = {
                "users": [],
                "messages": [],
                "created_at": datetime.now(),
            }

        self.rooms[room_id]["users"].append(websocket)
        logger.info(
            f"Пользователь подключился к комнате {room_id}. "
            f"Всего пользователей: {len(self.rooms[room_id]['users'])}"
        )

    def disconnect(self, room_id: str, websocket: WebSocket) -> None:
        """
        Отключить пользователя от комнаты.

        Args:
            room_id: ID комнаты
            websocket: WebSocket соединение
        """
        if room_id in self.rooms:
            try:
                self.rooms[room_id]["users"].remove(websocket)
                logger.info(
                    f"Пользователь отключился от комнаты {room_id}. "
                    f"Осталось пользователей: {len(self.rooms[room_id]['users'])}"
                )

                # Удаляем пустую комнату
                if not self.rooms[room_id]["users"]:
                    del self.rooms[room_id]
                    logger.info(f"Комната {room_id} удалена (пуста)")
            except ValueError:
                logger.warning(f"WebSocket не найден в комнате {room_id}")

    async def send_personal_message(self, message: str, websocket: WebSocket) -> None:
        """
        Отправить персональное сообщение одному пользователю.

        Args:
            message: Сообщение для отправки
            websocket: WebSocket соединение получателя
        """
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Ошибка при отправке персонального сообщения: {e}")

    async def broadcast(self, room_id: str, message: dict) -> None:
        """
        Отправить сообщение всем пользователям в комнате.

        Args:
            room_id: ID комнаты
            message: JSON сообщение для отправки
        """
        if room_id not in self.rooms:
            logger.warning(f"Комната {room_id} не найдена при трансляции")
            return

        # Снапшот списка пользователей для безопасной итерации
        # (предотвращает race condition при конкурентном disconnect)
        users_snapshot = list(self.rooms[room_id]["users"])
        disconnected_users = []

        for connection in users_snapshot:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Ошибка при трансляции в комнату {room_id}: {e}")
                disconnected_users.append(connection)

        # Удаляем разорванные соединения
        for user in disconnected_users:
            self.disconnect(room_id, user)

    def add_message(self, room_id: str, message: dict, websocket: WebSocket) -> None:
        """
        Добавить сообщение в историю комнаты.

        Args:
            room_id: ID комнаты
            message: Сообщение для сохранения
            websocket: WebSocket отправителя
        """
        if room_id in self.rooms:
            self.rooms[room_id]["messages"].append(
                {
                    "message": message,
                    "timestamp": datetime.now(),
                }
            )
            logger.debug(
                f"Сообщение добавлено в комнату {room_id}. "
                f"Всего сообщений: {len(self.rooms[room_id]['messages'])}"
            )

    def get_room_messages(self, room_id: str) -> List[dict]:
        """
        Получить все сообщения комнаты.

        Args:
            room_id: ID комнаты

        Returns:
            Список сообщений
        """
        if room_id in self.rooms:
            return self.rooms[room_id]["messages"]
        return []

    def get_room_info(self, room_id: str) -> Optional[dict]:
        """
        Получить информацию о комнате.

        Args:
            room_id: ID комнаты

        Returns:
            Информация о комнате
        """
        if room_id in self.rooms:
            return {
                "room_id": room_id,
                "users_count": len(self.rooms[room_id]["users"]),
                "messages_count": len(self.rooms[room_id]["messages"]),
                "created_at": self.rooms[room_id].get("created_at"),
            }
        return None
