
import pytest
from fastapi.testclient import TestClient

from api import create_app


@pytest.fixture
def client(tmp_path):
    data_file = tmp_path / "tasks.json"
    app = create_app(data_file)
    return TestClient(app)


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_empty_tasks(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={"title": "学习 FastAPI"},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "学习 FastAPI",
    }


def test_create_empty_task(client):
    response = client.post(
        "/tasks",
        json={"title": "   "},
    )

    assert response.status_code == 422


def test_delete_task(client):
    client.post(
        "/tasks",
        json={"title": "学习 Docker"},
    )

    response = client.delete("/tasks/1")

    assert response.status_code == 200
    assert client.get("/tasks").json() == []


def test_delete_missing_task(client):
    response = client.delete("/tasks/99")

    assert response.status_code == 404


def test_api_persistence(tmp_path):
    path = tmp_path / "tasks.json"

    client1 = TestClient(create_app(path))
    client1.post(
        "/tasks",
        json={"title": "学习 CI/CD"},
    )

    client2 = TestClient(create_app(path))

    assert client2.get("/tasks").json() == [
        {"id": 1, "title": "学习 CI/CD"}
    ]
