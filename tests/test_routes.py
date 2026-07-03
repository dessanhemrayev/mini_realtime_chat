"""Тесты для API маршрутов."""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestHealthRoute:
    """Тесты для health check маршрута."""

    def test_health_check(self):
        """Проверка health check эндпоинта."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
        assert "version" in response.json()


class TestInfoRoute:
    """Тесты для информационного маршрута."""

    def test_get_info(self):
        """Проверка получения информации о приложении."""
        response = client.get("/api/info")
        assert response.status_code == 200
        data = response.json()
        assert "title" in data
        assert "description" in data
        assert "version" in data


class TestAuthRoute:
    """Тесты для маршрутов аутентификации."""

    def test_get_auth_page(self):
        """Проверка получения страницы входа."""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert (
            "Mini Chat" in response.text
            or "Мини Чат" in response.text
            or "chat" in response.text.lower()
        )

    def test_get_chat_page(self):
        """Проверка получения страницы чата."""
        response = client.get("/room/test_room/test_user")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestRoomsAPI:
    """Тесты для API комнат."""

    def test_get_active_rooms_empty(self):
        """Проверка получения пустого списка комнат."""
        response = client.get("/api/rooms")
        assert response.status_code == 200
        data = response.json()
        assert "rooms" in data
        assert "total" in data
        assert isinstance(data["rooms"], list)

    def test_get_room_info_not_found(self):
        """Проверка получения информации о несуществующей комнате."""
        response = client.get("/api/rooms/nonexistent")
        assert response.status_code == 404

    def test_get_room_messages_not_found(self):
        """Проверка получения сообщений из несуществующей комнаты."""
        response = client.get("/api/rooms/nonexistent/messages")
        assert response.status_code == 404


class TestAPIDocumentation:
    """Тесты для документации API."""

    def test_swagger_ui(self):
        """Проверка доступности Swagger UI."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc(self):
        """Проверка доступности ReDoc."""
        response = client.get("/redoc")
        assert response.status_code == 200

    def test_openapi_schema(self):
        """Проверка доступности OpenAPI схемы."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "info" in data
        assert "paths" in data


class TestErrorHandling:
    """Тесты для обработки ошибок."""

    def test_404_not_found(self):
        """Проверка обработки 404 ошибки."""
        response = client.get("/nonexistent/route")
        assert response.status_code == 404

    def test_method_not_allowed(self):
        """Проверка обработки метода POST на GET маршруте."""
        response = client.post("/health")
        assert response.status_code in [
            405,
            422,
        ]  # Method Not Allowed или Validation Error


class TestRequestValidation:
    """Тесты для валидации запросов."""

    def test_invalid_room_id_length(self):
        """Проверка валидации длины room_id."""
        long_room_id = "a" * 101
        response = client.get(f"/room/{long_room_id}/user")
        assert response.status_code in [404, 422]

    def test_invalid_client_id_length(self):
        """Проверка валидации длины client_id."""
        long_client_id = "a" * 101
        response = client.get(f"/room/room1/{long_client_id}")
        assert response.status_code in [404, 422]
