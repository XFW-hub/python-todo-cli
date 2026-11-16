
import pytest
from fastapi.testclient import TestClient

from api import create_app


@pytest.fixture
def client(tmp_path):
    data_file = tmp_path / "tasks.db"
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
    path = tmp_path / "tasks.db"

    client1 = TestClient(create_app(path))
    client1.post(
        "/tasks",
        json={"title": "学习 CI/CD"},
    )

    client2 = TestClient(create_app(path))

    assert client2.get("/tasks").json() == [
        {"id": 1, "title": "学习 CI/CD"}
    ]


def test_stable_task_ids(client):
    for title in ["任务A", "任务B", "任务C"]:
        response = client.post(
            "/tasks",
            json={"title": title},
        )
        assert response.status_code == 201

    client.delete("/tasks/2")

    tasks = client.get("/tasks").json()

    assert [task["id"] for task in tasks] == [1, 3]

    response = client.post(
        "/tasks",
        json={"title": "任务D"},
    )

    assert response.status_code == 201
    assert response.json()["id"] == 4


def test_update_task(client):
    created = client.post(
        "/tasks",
        json={"title": "旧任务"},
    ).json()

    response = client.put(
        f"/tasks/{created['id']}",
        json={"title": "新任务"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": created["id"],
        "title": "新任务",
    }


def test_update_missing_task(client):
    response = client.put(
        "/tasks/999",
        json={"title": "不存在的任务"},
    )

    assert response.status_code == 404

