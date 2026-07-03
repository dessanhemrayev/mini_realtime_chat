# GitHub Actions CI/CD

Этот проект использует GitHub Actions для автоматизации тестирования, проверки качества кода и безопасности.

## 📋 Workflows

### 1. Tests (.github/workflows/tests.yml)

**Триггер:** Push и Pull Request на ветки `main`, `dev`

**Матрица тестирования:**
- ОС: Ubuntu, macOS, Windows
- Python: 3.10, 3.11, 3.12
- Всего комбинаций: 9

**Действия:**
- ✅ Установка зависимостей
- ✅ Запуск pytest с покрытием
- ✅ Загрузка отчетов в Codecov
- ✅ Генерация артефактов покрытия

**Выходные данные:**
- Coverage report на Codecov
- Артефакты с HTML отчетом (30 дней)

### 2. Lint (.github/workflows/lint.yml)

**Триггер:** Push и Pull Request на ветки `main`, `dev`

**Инструменты проверки:**
- **Black** - форматирование кода
- **isort** - сортировка импортов
- **flake8** - линтинг (E501, F401, W503 игнорируются)
- **mypy** - проверка типов
- **pylint** - анализ кода (порог: 8.0)

**Конфигурация:**
- Max line length: 120
- Python version: 3.11
- mypy, pylint выполняются с обязательной проверкой: job упадёт при ошибках типов или рейтинге ниже 8.0

### 3. Security (.github/workflows/security.yml)

**Триггер:**
- Push и Pull Request на ветки `main`, `dev`
- Еженедельное расписание (по воскресеньям в 00:00 UTC)

**Инструменты безопасности:**
- **Bandit** - поиск уязвимостей в коде
- **Safety** - проверка зависимостей на известные уязвимости

**Выходные данные:**
- Отчет Bandit в JSON формате
- Артефакты хранятся 30 дней

### 4. Docker (.github/workflows/docker.yml)

**Триггер:**
- Push на ветки `main`, `dev` и теги
- Pull Request на ветки `main`, `dev`

**Работа 1: docker-build**
- Сборка Docker образа
- Кеширование через GitHub Actions
- **Не** пушит образ в registry

**Работа 2: docker-build-push** (только для main branch и tags)
- Требует успешной первой работы
- Логин в GitHub Container Registry
- Сборка и пуш образа
- Автоматические теги (branch, semver, sha)

## 🔧 Конфигурация

### Требуемые секреты

- `GITHUB_TOKEN` - автоматически доступен (не нужно настраивать)

### Опциональные улучшения

Для пуша образов в DockerHub:

```yaml
- name: Login to DockerHub
  uses: docker/login-action@v2
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}
```

## 🚀 Использование

### Просмотр статуса

1. Откройте репозиторий на GitHub
2. Перейдите на вкладку "Actions"
3. Выберите workflow для просмотра деталей

### Бейджи статуса

Добавьте в README.md:

```markdown
![Tests](https://github.com/dessanhemrayev/my_mini_chat/workflows/Tests/badge.svg)
![Lint](https://github.com/dessanhemrayev/my_mini_chat/workflows/Lint%20and%20Code%20Quality/badge.svg)
![Security](https://github.com/dessanhemrayev/my_mini_chat/workflows/Security/badge.svg)
![Docker](https://github.com/dessanhemrayev/my_mini_chat/workflows/Docker%20Build/badge.svg)
```

### Перезапуск workflow

1. Откройте страницу workflow на GitHub Actions
2. Нажмите кнопку "Re-run all jobs" или "Re-run failed jobs"

## 📊 Статистика

### Время выполнения

| Workflow | Среднее время |
|----------|---------------|
| Tests | 2-5 минут |
| Lint | 1-2 минут |
| Security | 1-2 минут |
| Docker | 3-7 минут |

### Конкурентность

Все workflows запускаются параллельно при совместном триггере.

## 🛠️ Локальное воспроизведение

Для локального воспроизведения GitHub Actions используйте [act](https://github.com/nektos/act):

```bash
# Установка (macOS)
brew install act

# Запуск всех workflows
act

# Запуск конкретного workflow
act -j test

# Запуск с определенным событием
act pull_request
```

## ⚙️ Кастомизация

### Добавление новых Python версий

Отредактируйте `tests.yml`:

```yaml
matrix:
  python-version: ["3.10", "3.11", "3.12", "3.13"]
```

### Отключение некоторых OS

Отредактируйте `tests.yml`:

```yaml
matrix:
  os: [ubuntu-latest]  # Только Linux
```

### Изменение условий для пуша в registry

Отредактируйте `docker.yml`:

```yaml
docker-build-push:
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
```

## 📚 Ссылки

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pytest Plugin for Actions](https://github.com/marketplace/actions/pytest-coverage-comment)
- [Docker Build Action](https://github.com/docker/build-push-action)
- [codecov Action](https://github.com/codecov/codecov-action)

## 🐛 Решение проблем

### Workflow не запускается

Проверьте:
1. YAML синтаксис в файле workflow
2. Правильность названия ветки в `on.push.branches`
3. Наличие файла в правильной директории (`.github/workflows/`)

### Тесты падают в Actions но проходят локально

Вероятные причины:
1. Разные версии Python
2. Отличия в окружении (PATH, переменные окружения)
3. Проблемы с зависимостями

Решение:
```bash
# Используйте точно такую же версию Python
python --version

# Установите точно такие же зависимости
pip install -r requirements.txt --upgrade
```

### Медленные тесты

Оптимизируйте:
1. Уменьшите количество Python версий в матрице
2. Используйте кеширование зависимостей
3. Запускайте тесты параллельно

---

Для любых вопросов о CI/CD смотрите [README.md](../README.md#-cicd-pipeline-github-actions)
