
from datetime import datetime
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient

from api import create_app


def prepare_database(db_path, monkeypatch):
    monkeypatch.setenv("TODO_DB_PATH", str(db_path))

    config = Config(
        str(Path(__file__).parent / "alembic.ini")
    )

    command.upgrade(config, "head")


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "tasks.db"
    prepare_database(db_path, monkeypatch)

    return TestClient(create_app(db_path))


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

    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "学习 FastAPI"
    assert data["completed"] is False
    datetime.fromisoformat(data["created_at"])


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


def test_api_persistence(tmp_path, monkeypatch):
    db_path = tmp_path / "tasks.db"
    prepare_database(db_path, monkeypatch)

    client1 = TestClient(create_app(db_path))
    client1.post(
        "/tasks",
        json={"title": "学习 CI/CD"},
    )

    client2 = TestClient(create_app(db_path))
    tasks = client2.get("/tasks").json()

    assert len(tasks) == 1
    assert tasks[0]["title"] == "学习 CI/CD"


def test_stable_task_ids(client):
    for title in ["任务A", "任务B", "任务C"]:
        client.post("/tasks", json={"title": title})

    client.delete("/tasks/2")

    tasks = client.get("/tasks").json()
    assert [task["id"] for task in tasks] == [1, 3]

    response = client.post(
        "/tasks",
        json={"title": "任务D"},
    )

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
    assert response.json()["title"] == "新任务"


def test_update_missing_task(client):
    response = client.put(
        "/tasks/999",
        json={"title": "不存在"},
    )
    assert response.status_code == 404


def test_complete_task(client):
    created = client.post(
        "/tasks",
        json={"title": "完成测试"},
    ).json()

    task_id = created["id"]

    response = client.patch(
        f"/tasks/{task_id}/complete"
    )

    assert response.status_code == 200
    assert response.json()["completed"] is True

    tasks = client.get("/tasks").json()
    assert tasks[0]["completed"] is True


def test_complete_missing_task(client):
    response = client.patch(
        "/tasks/999/complete"
    )

    assert response.status_code == 404


import sqlite3


def test_migration_preserves_existing_tasks(
    tmp_path, monkeypatch
):
    db_path = tmp_path / "old_tasks.db"

    monkeypatch.setenv(
        "TODO_DB_PATH",
        str(db_path),
    )

    config = Config(
        str(Path(__file__).parent / "alembic.ini")
    )

    # 先创建旧版本数据库
    command.upgrade(config, "baseline_tasks")

    with sqlite3.connect(db_path) as con:
        con.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            ("历史任务",),
        )
        con.commit()

    # 从旧版本升级到最新版本
    command.upgrade(config, "head")

    with sqlite3.connect(db_path) as con:
        row = con.execute(
            """
            SELECT id, title, completed, created_at
            FROM tasks
            WHERE title = ?
            """,
            ("历史任务",),
        ).fetchone()

    assert row is not None
    assert row[0] == 1
    assert row[1] == "历史任务"
    assert row[2] == 0
    assert row[3] is not None
