"""API маршруты и WebSocket эндпоинты."""

import json
import logging
from datetime import datetime
from typing import Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Path, Query
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from .schemas import MessageData, ChatMessageSchema, SystemMessageSchema
from .managers import ConnectionManager
from .utils import get_hash
from .config import (
    MESSAGE_FORMAT, 
    MAX_MESSAGE_LENGTH, 
    MAX_NAME_LENGTH,
    MAX_ROOM_ID_LENGTH,
    STATIC_DIR
)

logger = logging.getLogger(__name__)
router = APIRouter()

# Инициализируем менеджер подключений
manager = ConnectionManager()


# HTML эндпоинты
@router.get("/", response_class=HTMLResponse, tags=["HTML"])
async def get_auth_page():
    """Главная страница с формой входа в чат."""
    try:
        with open(STATIC_DIR / "index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logger.error("Файл index.html не найден")
        return "<h1>Ошибка: страница не найдена</h1>"


@router.get("/room/{room_id}/{client_id}", response_class=HTMLResponse, tags=["HTML"])
async def get_chat_page(
    room_id: str = Path(..., max_length=MAX_ROOM_ID_LENGTH, description="ID комнаты"),
    client_id: str = Path(..., max_length=MAX_NAME_LENGTH, description="ID клиента")
):
    """
    Страница чата для конкретной комнаты.
    
    Args:
        room_id: ID комнаты
        client_id: ID клиента
        
    Returns:
        HTML страница чата
    """
    logger.info(f"Пользователь {client_id} запросил страницу чата для комнаты {room_id}")
    
    try:
        with open(STATIC_DIR / "chat.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logger.error("Файл chat.html не найден")
        raise HTTPException(status_code=404, detail="Страница чата не найдена")


# REST API эндпоинты
@router.get("/api/rooms", tags=["Rooms"])
async def get_active_rooms():
    """Получить список активных комнат."""
    rooms_info = []
    for room_id in manager.rooms.keys():
        info = manager.get_room_info(room_id)
        if info:
            rooms_info.append(info)
    
    return {"rooms": rooms_info, "total": len(rooms_info)}


@router.get("/api/rooms/{room_id}", tags=["Rooms"])
async def get_room_info(
    room_id: str = Path(..., max_length=MAX_ROOM_ID_LENGTH, description="ID комнаты")
):
    """
    Получить информацию о комнате.
    
    Args:
        room_id: ID комнаты
        
    Returns:
        Информация о комнате
    """
    info = manager.get_room_info(room_id)
    if not info:
        raise HTTPException(status_code=404, detail="Комната не найдена")
    
    return info


@router.get("/api/rooms/{room_id}/messages", tags=["Messages"])
async def get_room_messages(
    room_id: str = Path(..., max_length=MAX_ROOM_ID_LENGTH, description="ID комнаты"),
    limit: int = Query(100, ge=1, le=1000, description="Максимальное количество сообщений")
):
    """
    Получить сообщения из комнаты.
    
    Args:
        room_id: ID комнаты
        limit: Максимальное количество сообщений
        
    Returns:
        Список сообщений
    """
    messages = manager.get_room_messages(room_id)
    
    if not messages:
        raise HTTPException(status_code=404, detail="Сообщения не найдены")
    
    # Возвращаем последние N сообщений
    return {"messages": messages[-limit:]}


# WebSocket эндпоинт
@router.websocket("/ws/room/{room_id}/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str = Path(..., max_length=MAX_ROOM_ID_LENGTH, description="ID комнаты"),
    client_id: str = Path(..., max_length=MAX_NAME_LENGTH, description="ID клиента")
):
    """
    WebSocket эндпоинт для чата в реальном времени.
    
    Args:
        websocket: WebSocket соединение
        room_id: ID комнаты
        client_id: ID клиента
    """
    await manager.connect(room_id, websocket)
    
    try:
        # Отправляем системное сообщение о присоединении
        join_message = SystemMessageSchema(
            message=MESSAGE_FORMAT["user_joined"].format(client_id=client_id)
        )
        await manager.broadcast(room_id, join_message.model_dump())
        
        # Основной цикл приема сообщений
        while True:
            # Получаем текст сообщения
            raw_data = await websocket.receive_text()
            
            try:
                # Парсим JSON сообщение
                data = json.loads(raw_data)
                
                # Валидируем через Pydantic модель
                message_data = MessageData(
                    text=data.get("text", "").strip(),
                    name=data.get("name", client_id).strip()
                )
                
                # Проверяем длины
                if len(message_data.text) > MAX_MESSAGE_LENGTH:
                    logger.warning(f"Сообщение слишком длинное от {client_id}")
                    continue
                
                if len(message_data.name) > MAX_NAME_LENGTH:
                    logger.warning(f"Имя слишком длинное от {client_id}")
                    continue
                
                # Формируем сообщение для отправки
                send_date = datetime.now()
                
                chat_message = ChatMessageSchema(
                    author={
                        "author_id": client_id,
                        "name": message_data.name,
                        "image": f"/addres/users.account/avatar/{client_id}/{get_hash(message_data.text)}"
                    },
                    text=message_data.text,
                    day=send_date.strftime("%d.%m.%Y"),
                    time=send_date.strftime("%H:%M")
                )
                
                # Сохраняем сообщение в историю
                manager.add_message(room_id, chat_message.model_dump(), websocket)
                
                # Отправляем сообщение всем в комнате
                await manager.broadcast(room_id, chat_message.model_dump())
                
                logger.info(f"Сообщение от {client_id} в комнате {room_id}: {message_data.text[:50]}...")
                
            except json.JSONDecodeError:
                logger.warning(f"Невалидный JSON от {client_id}")
                continue
            except ValueError as e:
                logger.warning(f"Ошибка валидации от {client_id}: {e}")
                continue
    
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
        
        # Отправляем системное сообщение об отключении
        leave_message = SystemMessageSchema(
            message=MESSAGE_FORMAT["user_left"].format(client_id=client_id)
        )
        await manager.broadcast(room_id, leave_message.model_dump())
        
        logger.info(f"Пользователь {client_id} отключился от комнаты {room_id}")
    
    except Exception as e:
        logger.error(f"Ошибка WebSocket для {client_id} в комнате {room_id}: {e}")
        manager.disconnect(room_id, websocket)
        raise
