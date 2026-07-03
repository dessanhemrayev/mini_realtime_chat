"""Конфигурация приложения."""

import logging
from pathlib import Path

# Пути
BASE_DIR = Path(__file__).parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"

# Логирование
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# WebSocket
WEBSOCKET_TIMEOUT = 60

# Приложение
APP_TITLE = "Mini Chat"
APP_DESCRIPTION = "Простой мини чат на FastAPI с WebSocket"
APP_VERSION = "1.0.0"

# CORS (если нужно)
CORS_ORIGINS = ["*"]

# Максимальные размеры
MAX_MESSAGE_LENGTH = 5000
MAX_NAME_LENGTH = 100
MAX_ROOM_ID_LENGTH = 100

# Сообщения
MESSAGE_FORMAT = {
    "user_joined": "Пользователь #{client_id} присоединился к чату",
    "user_left": "Пользователь #{client_id} покинул чат",
}
