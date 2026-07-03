# 🚀 Быстрый старт

Все способы запуска Mini Chat приложения.

## 1️⃣ Вариант 1: Локальный запуск (Development)

### Требования
- Python 3.8+
- pip

### Установка

```bash
# Создаем виртуальное окружение
python -m venv venv

# Активируем (Linux/Mac)
source venv/bin/activate
# или (Windows)
venv\Scripts\activate

# Устанавливаем зависимости
pip install -r requirements.txt

# Запускаем приложение
python main.py
```

🌐 Откройте: **[http://localhost:8888](http://localhost:8888)**

---

## 2️⃣ Вариант 2: Docker (Рекомендуется)

### Требования
- Docker
- Docker Compose

### Запуск

```bash
# Development с hot-reload
docker-compose up -d

# Production с Nginx
docker-compose -f docker-compose.prod.yml up -d
```

**Development:** [http://localhost:8888](http://localhost:8888)  
**Production:** [http://localhost](http://localhost) (через Nginx)

---

## 3️⃣ Вариант 3: Uvicorn напрямую

```bash
# С перезагрузкой при изменениях
uvicorn main:app --reload --port 8888

# Production режим (4 worker'а)
uvicorn main:app --host 0.0.0.0 --port 8888 --workers 4
```

---

## 📚 Документация API

После запуска, откройте:

- **Swagger UI**: [http://localhost:8888/docs](http://localhost:8888/docs)
- **ReDoc**: [http://localhost:8888/redoc](http://localhost:8888/redoc)

---

## 🐛 Отладка

### Проверка здоровья

```bash
curl http://localhost:8888/health
```

### Логи контейнера

```bash
docker-compose logs -f mini-chat
```

### Вход в контейнер

```bash
docker-compose exec mini-chat bash
```

---

## 🛑 Остановка

```bash
# Локальный запуск
Ctrl+C

# Docker
docker-compose down
docker-compose -f docker-compose.prod.yml down
```

---

## 📖 Полная документация

Смотрите [README.md](README.md) для полного описания проекта.

---

**Выберите вариант запуска и наслаждайтесь! 🎉**
