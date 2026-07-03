"""Точка входа для FastAPI приложения."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes import router
from app.config import (
    APP_TITLE,
    APP_DESCRIPTION,
    APP_VERSION,
    CORS_ORIGINS,
    LOG_LEVEL,
    LOG_FORMAT
)

# Настройка логирования
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT
)
logger = logging.getLogger(__name__)


# Жизненный цикл приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекстный менеджер для управления жизненным циклом приложения.
    """
    # Код при запуске
    logger.info(f"🚀 Запуск приложения {APP_TITLE} v{APP_VERSION}")
    
    yield
    
    # Код при завершении
    logger.info("🛑 Остановка приложения")


# Инициализация FastAPI приложения
app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    lifespan=lifespan
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Обработчик ошибок
@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    """Обработчик ошибок валидации."""
    logger.error(f"Ошибка валидации: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Общий обработчик ошибок."""
    logger.error(f"Неожиданная ошибка: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Внутренняя ошибка сервера"},
    )


# Health check
@app.get("/health", tags=["Health"])
async def health_check():
    """Проверка здоровья приложения."""
    return {"status": "ok", "version": APP_VERSION}


# Включение маршрутов
app.include_router(router)


# Info эндпоинт
@app.get("/api/info", tags=["Info"])
async def get_info():
    """Получить информацию о приложении."""
    return {
        "title": APP_TITLE,
        "description": APP_DESCRIPTION,
        "version": APP_VERSION,
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Запуск сервера...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8888,
        reload=True,
        log_level="info",
    )
