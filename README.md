# 💬 Mini Chat - FastAPI WebSocket Chat

Современный мини-чат приложение на **FastAPI** с поддержкой **WebSocket** для общения в реальном времени. Проект реализует лучшие практики и каноны FastAPI разработки.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=flat&logo=python)](https://www.python.org/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-0.24.0-00a85c?style=flat)](https://www.uvicorn.org/)
[![WebSocket](https://img.shields.io/badge/WebSocket-RFC%206455-FF6B6B?style=flat)](https://tools.ietf.org/html/rfc6455)

## 🌟 Основные возможности

- 🚀 **FastAPI** - современный асинхронный веб-фреймворк
- 🔌 **WebSocket** - двусторонняя связь в реальном времени
- ✅ **Pydantic** - строгая валидация данных с типизацией
- 📚 **Auto API Docs** - автоматическая документация (Swagger UI, ReDoc)
- 🎨 **Responsive UI** - современный интерфейс с HTML5/CSS3
- 🪵 **Логирование** - структурированное логирование всех операций
- 🏗️ **Модульная архитектура** - чистое разделение ответственности
- 🔐 **CORS поддержка** - кросс-доменные запросы
- ⚡ **Асинхронность** - полная поддержка async/await
- 🛡️ **Обработка ошибок** - кастомные exception handlers

## 📋 Требования

- Python 3.8+
- pip или Poetry

## 📂 Структура проекта

```
my_mini_chat/
├── app/                          # Основной пакет приложения
│   ├── __init__.py               # Инициализация пакета
│   ├── config.py                 # Конфигурация и константы
│   ├── schemas.py                # Pydantic модели валидации
│   ├── managers.py               # ConnectionManager (менеджер подключений)
│   ├── utils.py                  # Вспомогательные функции
│   ├── routes.py                 # API маршруты и WebSocket
│   └── static/
│       ├── index.html            # Страница входа в чат
│       └── chat.html             # Страница чата
├── main.py                       # Точка входа приложения
├── requirements.txt              # Зависимости проекта
├── .env.example                  # Пример переменных окружения
├── .dockerignore                 # Исключение файлов из Docker образа
├── command.txt                   # Команда запуска сервера
├── Dockerfile                    # Docker образ для production
├── docker-compose.yml            # Docker compose для development
├── docker-compose.prod.yml       # Docker compose для production с Nginx
├── nginx.conf                    # Конфигурация Nginx reverse proxy
├── README.md                     # Этот файл
└── LICENSE                       # Лицензия проекта
```

### Описание модулей

| Файл | Назначение |
|------|-----------|
| `config.py` | Централизованная конфигурация, переменные окружения, константы |
| `schemas.py` | Pydantic модели для валидации входящих/исходящих данных |
| `managers.py` | ConnectionManager - управление WebSocket подключениями |
| `utils.py` | Вспомогательные функции (хеширование, рефлексия) |
| `routes.py` | API маршруты, HTML эндпоинты, WebSocket обработчик |

## 🚀 Установка

### 1. Клонируем/распаковываем проект

```bash
cd my_mini_chat
```

### 2. Создаем виртуальное окружение

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Устанавливаем зависимости

```bash
pip install -r requirements.txt
```

### 4. Запускаем приложение

**Способ 1 - через main.py:**
```bash
python main.py
```

**Способ 2 - прямо через uvicorn:**
```bash
uvicorn main:app --reload --port 8888
```

**Способ 3 - полная конфигурация:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8888 --reload --log-level info
```

**Результат:**
```
INFO:     Uvicorn running on http://127.0.0.1:8888 (Press CTRL+C to quit)
```

## 🌐 Использование

### Веб-интерфейс

1. Откройте браузер: **[http://localhost:8888](http://localhost:8888)**
2. Введите ID комнаты (например: `room1`)
3. Введите ваше имя (например: `Иван`)
4. Нажмите кнопку "Войти в чат"
5. Начните общаться! 💬

### API Документация

| Ссылка | Описание |
|--------|---------|
| [http://localhost:8888/docs](http://localhost:8888/docs) | Swagger UI - интерактивная документация |
| [http://localhost:8888/redoc](http://localhost:8888/redoc) | ReDoc - альтернативная документация |

## 🔌 REST API Эндпоинты

### HTML Эндпоинты

```http
GET /
```
Главная страница с формой входа в чат.

```http
GET /room/{room_id}/{client_id}
```
Страница чата для конкретной комнаты.

### REST API

```http
GET /health
```
Проверка здоровья приложения.
```json
{ "status": "ok", "version": "1.0.0" }
```

```http
GET /api/info
```
Информация о приложении.
```json
{
  "title": "Mini Chat",
  "description": "Простой мини чат на FastAPI с WebSocket",
  "version": "1.0.0"
}
```

```http
GET /api/rooms
```
Список активных чат-комнат с информацией.
```json
{
  "rooms": [
    {
      "room_id": "room1",
      "users_count": 2,
      "messages_count": 15,
      "created_at": "2026-07-03T14:30:00"
    }
  ],
  "total": 1
}
```

```http
GET /api/rooms/{room_id}
```
Информация о конкретной комнате.
```json
{
  "room_id": "room1",
  "users_count": 2,
  "messages_count": 15,
  "created_at": "2026-07-03T14:30:00"
}
```

```http
GET /api/rooms/{room_id}/messages?limit=100
```
История сообщений из комнаты.

**Параметры:**
- `limit` (int, default=100): Максимальное количество сообщений (1-1000)

### WebSocket

```websocket
ws://localhost:8888/ws/room/{room_id}/{client_id}
```

**Подключение к чату:**

```javascript
const ws = new WebSocket('ws://localhost:8888/ws/room/room1/user123');
```

**Отправка сообщения:**

```json
{
  "text": "Привет, это мое сообщение!",
  "name": "user123"
}
```

**Получение сообщения:**

```json
{
  "author": {
    "author_id": "user123",
    "name": "Иван",
    "image": "/addres/users.account/avatar/user123/abc1234"
  },
  "text": "Привет, это мое сообщение!",
  "day": "03.07.2026",
  "time": "14:30"
}
```

**Системное сообщение:**

```json
{
  "type": "system",
  "message": "Пользователь #user123 присоединился к чату"
}
```

## 💻 Примеры использования

### cURL

```bash
# Получить список активных комнат
curl http://localhost:8888/api/rooms

# Получить информацию о комнате
curl http://localhost:8888/api/rooms/room1

# Получить сообщения (последние 50)
curl "http://localhost:8888/api/rooms/room1/messages?limit=50"

# Проверка здоровья
curl http://localhost:8888/health
```

## 🔧 Конфигурация

### Переменные окружения

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Отредактируйте `.env`:

```env
APP_TITLE=Mini Chat
APP_VERSION=1.0.0
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8888
RELOAD=True
```

### Тестирование API

Используйте Swagger UI: [http://localhost:8888/docs](http://localhost:8888/docs)

## 🐛 Отладка

### Включение debug режима

Запустите с debug логированием:
```bash
uvicorn main:app --reload --log-level debug
```

### Логи приложения

Логи пишутся в консоль с форматом:
```
2026-07-03 14:30:00,123 - app.routes - INFO - Пользователь user1 запросил страницу чата
```

## 🧪 Тестирование

Проект включает полный набор тестов: unit, integration и API тесты.

### Структура тестов

```
tests/
├── __init__.py              # Инициализация пакета тестов
├── conftest.py              # Fixtures и конфигурация
├── test_routes.py           # Тесты API маршрутов
├── test_managers.py         # Тесты менеджера подключений
├── test_schemas.py          # Тесты Pydantic моделей
└── test_utils.py            # Тесты утилит
```

### Запуск тестов

**Запустить все тесты с покрытием:**
```bash
pytest tests/ -v --cov=app --cov-report=html
```

**Запустить быстрые тесты:**
```bash
pytest tests/ -v -m "not slow"
```

**Запустить конкретный тест:**
```bash
pytest tests/test_routes.py::TestHealthRoute::test_health_check -v
```

**Запустить с выводом покрытия:**
```bash
pytest tests/ --cov=app --cov-report=term-missing
```

### Скрипты для тестирования

**Linux/Mac:**
```bash
chmod +x run_tests.sh
./run_tests.sh all       # Все тесты
./run_tests.sh fast      # Быстрые тесты
./run_tests.sh coverage  # С покрытием
```

**Windows:**
```bash
run_tests.bat all       # Все тесты
run_tests.bat fast      # Быстрые тесты
run_tests.bat coverage  # С покрытием
```

### Примеры тестов

**Unit тест (Pydantic модель):**
```python
def test_valid_message():
    """Проверка валидного сообщения."""
    msg = MessageData(text="Hello", name="User")
    assert msg.text == "Hello"
    assert msg.name == "User"
```

**API тест:**
```python
def test_health_check():
    """Проверка health check эндпоинта."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

**Async тест:**
```python
@pytest.mark.asyncio
async def test_connect():
    """Проверка подключения пользователя."""
    manager = ConnectionManager()
    websocket = AsyncMock()
    
    await manager.connect("room1", websocket)
    
    assert "room1" in manager.rooms
```

### Рекомендации

- Запускайте тесты перед коммитом
- Старайтесь поддерживать покрытие выше 80%
- Используйте fixtures из conftest.py
- Пишите тесты для новых фич

## 📦 Зависимости

### Production

| Пакет | Версия | Назначение |
|-------|--------|-----------|
| FastAPI | 0.104.1 | Веб-фреймворк |
| uvicorn | 0.24.0 | ASGI сервер |
| Pydantic | 2.5.0 | Валидация данных |
| python-multipart | 0.0.6 | Парсинг форм |
| aiofiles | 23.2.1 | Асинхронная работа с файлами |
| Jinja2 | 3.1.2 | Шаблонизатор |
| python-dotenv | 1.0.0 | Загрузка .env переменных |

### Testing

| Пакет | Версия | Назначение |
|-------|--------|-----------|
| pytest | 7.4.3 | Фреймворк для тестирования |
| pytest-asyncio | 0.21.1 | Поддержка async тестов |
| httpx | 0.25.1 | HTTP клиент для тестов |
| pytest-cov | 4.1.0 | Измерение покрытия кода |

### Development

| Пакет | Версия | Назначение |
|-------|--------|-----------|
| black | 23.12.0 | Форматирование кода |
| isort | 5.13.2 | Сортировка импортов |
| flake8 | 6.1.0 | Линтинг кода |
| pylint | 3.0.3 | Анализ кода |
| mypy | 1.7.1 | Статическая типизация |

## � Docker и Docker Compose

### Основные файлы

| Файл | Назначение |
|------|-----------|
| `Dockerfile` | Образ для production |
| `docker-compose.yml` | Конфиг для development |
| `docker-compose.prod.yml` | Конфиг для production с Nginx |
| `.dockerignore` | Исключение файлов из образа |
| `nginx.conf` | Конфигурация reverse proxy |

### Development с Docker Compose

**1. Запуск контейнера:**

```bash
docker-compose up -d
```

**2. Просмотр логов:**

```bash
docker-compose logs -f mini-chat
```

**3. Доступ к приложению:**
- 🌐 Веб-интерфейс: [http://localhost:8888](http://localhost:8888)
- 📚 Swagger UI: [http://localhost:8888/docs](http://localhost:8888/docs)

**4. Hot-reload для разработки:**

Раскомментируйте строку в `docker-compose.yml`:

```yaml
command: uvicorn main:app --host 0.0.0.0 --port 8888 --reload
```

Затем перезагрузите:

```bash
docker-compose up -d --build
```

**5. Остановка контейнера:**

```bash
docker-compose down
```

### Production с Docker Compose

**1. Запуск с Nginx reverse proxy:**

```bash
docker-compose -f docker-compose.prod.yml up -d
```

**2. Приложение будет доступно через Nginx:**
- 🌐 Веб-интерфейс: [http://localhost](http://localhost)
- 📚 Swagger UI: [http://localhost/docs](http://localhost/docs)

**3. Просмотр статуса:**

```bash
docker-compose -f docker-compose.prod.yml ps
```

**4. Просмотр логов:**

```bash
# Логи приложения
docker-compose -f docker-compose.prod.yml logs -f mini-chat

# Логи Nginx
docker-compose -f docker-compose.prod.yml logs -f nginx
```

**5. Остановка:**

```bash
docker-compose -f docker-compose.prod.yml down
```

### Ручная сборка и запуск Docker

**Сборка образа:**

```bash
docker build -t mini-chat:latest .
```

**Запуск контейнера:**

```bash
docker run -d \
  --name mini-chat \
  -p 8888:8888 \
  -e LOG_LEVEL=INFO \
  --restart unless-stopped \
  mini-chat:latest
```

**Проверка статуса:**

```bash
docker ps
```

**Просмотр логов:**

```bash
docker logs -f mini-chat
```

**Остановка:**

```bash
docker stop mini-chat
docker rm mini-chat
```

### Полезные команды

```bash
# Просмотр образов
docker images | grep mini-chat

# Удаление образа
docker rmi mini-chat:latest

# Очистка неиспользуемых ресурсов
docker system prune -a

# Вход в контейнер
docker-compose exec mini-chat bash

# Проверка health статуса
docker-compose exec mini-chat curl http://localhost:8888/health

# Просмотр переменных окружения в контейнере
docker-compose exec mini-chat env | grep LOG_LEVEL
```

### Проблемы и решения

**Портт 8888 уже занят:**

```bash
# Найти процесс
lsof -i :8888

# Изменить порт в docker-compose.yml
ports:
  - "9999:8888"  # Вместо 8888:8888
```

**Отсутствует Docker:**

```bash
# Ubuntu/Debian
sudo apt-get install docker.io docker-compose

# macOS (через Homebrew)
brew install docker docker-compose
```

**Контейнер не стартует:**

```bash
# Проверьте логи
docker-compose logs mini-chat

# Пересоберите образ
docker-compose build --no-cache
```

## 🚀 Развертывание

### Production режим

**Запуск нескольких worker'ов:**

```bash
uvicorn main:app --host 0.0.0.0 --port 8888 --workers 4
```

**С автоперезагрузкой при ошибке:**

```bash
uvicorn main:app --host 0.0.0.0 --port 8888 --workers 4 --loop uvloop
```

### Облачное развертывание

**Heroku:**

```bash
heroku login
heroku create mini-chat
git push heroku main
```

**Railway.app:**

Просто подключите репозиторий GitHub и Railway автоматически обнаружит Dockerfile

**AWS/DigitalOcean/etc:**

Используйте docker-compose.prod.yml с Nginx и настройте SSL сертификаты

## 🤝 Контрибьютинг

Контрибьюции приветствуются! Пожалуйста:

1. Форкните репозиторий
2. Создайте ветку для вашей фичи (`git checkout -b feature/AmazingFeature`)
3. Коммитьте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Пушьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📝 Лицензия

Этот проект распространяется под лицензией MIT. Смотрите [LICENSE](LICENSE) файл для деталей.

## 🎯 Дорожная карта

Планы на будущее:

- [ ] 🔐 Аутентификация и авторизация (JWT)
- [ ] 💾 Сохранение истории в базе данных (PostgreSQL)
- [ ] 🔍 Поиск по сообщениям
- [ ] 👥 Управление пользователями
- [ ] 📁 Загрузка файлов и изображений
- [ ] 📱 Мобильное приложение
- [ ] 🎨 Кастомизация тем
- [ ] 🔔 Push-notifications
- [ ] 🌍 Интеграция с внешними сервисами
- [ ] ⚙️ Admin панель

## 💬 Поддержка

Если у вас есть вопросы или проблемы:

1. 📖 Проверьте документацию в [/docs](http://localhost:8888/docs)
2. 🔍 Посмотрите существующие issues
3. 💌 Создайте новый issue с описанием проблемы

---
