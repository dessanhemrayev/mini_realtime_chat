# GitHub Actions Status Badge Template

Скопируйте эти строки в ваш README.md для отображения статуса workflows:

## Полный набор бейджей

```markdown
# 💬 Mini Chat - FastAPI WebSocket Chat

[![Tests](https://github.com/dessanhemrayev/my_mini_chat/actions/workflows/tests.yml/badge.svg)](https://github.com/dessanhemrayev/my_mini_chat/actions/workflows/tests.yml)
[![Lint](https://github.com/dessanhemrayev/my_mini_chat/actions/workflows/lint.yml/badge.svg)](https://github.com/dessanhemrayev/my_mini_chat/actions/workflows/lint.yml)
[![Security](https://github.com/dessanhemrayev/my_mini_chat/actions/workflows/security.yml/badge.svg)](https://github.com/dessanhemrayev/my_mini_chat/actions/workflows/security.yml)
[![Docker](https://github.com/dessanhemrayev/my_mini_chat/actions/workflows/docker.yml/badge.svg)](https://github.com/dessanhemrayev/my_mini_chat/actions/workflows/docker.yml)
```

## Компактный набор

```markdown
[![Tests](https://github.com/dessanhemrayev/my_mini_chat/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/dessanhemrayev/my_mini_chat/actions)
```

## Запуск workflow'ов локально с act

```bash
# Установить act
# macOS
brew install act

# Ubuntu
sudo apt-get install act

# Windows
choco install act-cli

# Запустить все workflows
act

# Запустить конкретный workflow
act -j test
act -j lint
act -j security

# Запустить с определенным событием
act pull_request
act push
```

## Просмотр логов

На GitHub:
1. Перейдите в Actions
2. Выберите workflow run
3. Нажмите на job для просмотра логов

## Отладка

Если workflow падает:

1. **Проверьте синтаксис YAML:**
   ```bash
   python -m yaml <filename>
   ```

2. **Запустите локально с act:**
   ```bash
   act --list  # Показать доступные workflows
   act -j test --verbose
   ```

3. **Проверьте логи:**
   - Откройте Actions на GitHub
   - Найдите failed workflow
   - Прочитайте step logs

## Кастомизация для вашего репозитория

Если вы форкировали этот репозиторий, замените:

```yaml
# В docker.yml
- name: Login to GitHub Container Registry
  uses: docker/login-action@v2
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}

# На:
- name: Login to GitHub Container Registry
  uses: docker/login-action@v2
  with:
    registry: ghcr.io
    username: YOUR_USERNAME  # Замените на ваш username
    password: ${{ secrets.GITHUB_TOKEN }}
```

## Полезные переменные в workflows

```yaml
${{ github.actor }}                    # Имя пользователя
${{ github.repository }}               # owner/repo
${{ github.ref }}                      # refs/heads/branch
${{ github.event_name }}               # push, pull_request, etc
${{ secrets.GITHUB_TOKEN }}            # Автоматический токен
${{ matrix.python-version }}           # Текущая версия из матрицы
${{ matrix.os }}                       # Текущая ОС из матрицы
```

## Расширенная конфигурация

### Отправка результатов в Slack

```yaml
- name: Notify Slack
  if: always()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "Tests ${{ job.status }}",
        "status": "${{ job.status }}"
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### Автоматический релиз

```yaml
- name: Create Release
  if: startsWith(github.ref, 'refs/tags/')
  uses: actions/create-release@v1
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  with:
    tag_name: ${{ github.ref }}
    release_name: Release ${{ github.ref }}
```

### Автоматическое обновление документации

```yaml
- name: Deploy docs
  if: github.ref == 'refs/heads/main'
  run: |
    pip install sphinx sphinx-rtd-theme
    make -C docs html
    # Загрузить на GitHub Pages
```

---

Для более подробной информации смотрите [CI-CD.md](.github/CI-CD.md)
