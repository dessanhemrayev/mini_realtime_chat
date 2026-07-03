"""Pydantic модели для валидации данных."""

from typing import Optional

from pydantic import BaseModel, Field


class MessageData(BaseModel):
    """Входящее сообщение от клиента."""

    text: str = Field(..., min_length=1, max_length=5000, description="Текст сообщения")
    name: str = Field(..., min_length=1, max_length=100, description="Имя отправителя")

    class Config:
        json_schema_extra = {
            "example": {"text": "Привет, это сообщение!", "name": "Иван"}
        }


class AuthorSchema(BaseModel):
    """Информация об авторе сообщения."""

    author_id: str = Field(..., description="ID автора")
    name: str = Field(..., description="Имя автора")
    image: Optional[str] = Field(None, description="URL аватара")


class ChatMessageSchema(BaseModel):
    """Сообщение в чате (отправляемое клиентам)."""

    author: AuthorSchema
    text: str = Field(..., description="Текст сообщения")
    day: str = Field(..., description="Дата (dd.mm.yyyy)")
    time: str = Field(..., description="Время (HH:MM)")

    class Config:
        json_schema_extra = {
            "example": {
                "author": {
                    "author_id": "user123",
                    "name": "Иван",
                    "image": "/addres/users.account/avatar/user123/abc1234",
                },
                "text": "Привет, это сообщение!",
                "day": "03.07.2026",
                "time": "14:30",
            }
        }


class SystemMessageSchema(BaseModel):
    """Системное сообщение."""

    type: str = Field(default="system", description="Тип сообщения")
    message: str = Field(..., description="Текст системного сообщения")
