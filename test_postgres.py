
import os
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import text

from api import create_app
from database import create_database


pytestmark = [
    pytest.mark.postgres,
    pytest.mark.skipif(
        os.getenv("RUN_POSTGRES_TESTS") != "1",
        reason="PostgreSQL tests are disabled",
    ),
]


@pytest.fixture
def pg_client(monkeypatch):
    monkeypatch.setenv("DB_HOST", "127.0.0.1")
    monkeypatch.setenv("DB_PORT", "5433")
    monkeypatch.setenv("DB_USER", "test_user")
    monkeypatch.setenv("DB_PASSWORD", "test_password")
    monkeypatch.setenv("DB_NAME", "todo_test_db")

    config = Config(
        str(Path(__file__).parent / "alembic.ini")
    )

    command.upgrade(config, "head")

    engine, _ = create_database()

    # 确保连接的是专用测试数据库
    with engine.begin() as conn:
        db_name = conn.execute(
            text("SELECT current_database()")
        ).scalar_one()

        assert db_name == "todo_test_db"

        conn.execute(
            text("TRUNCATE TABLE tasks RESTART IDENTITY")
        )

    try:
        with TestClient(create_app()) as client:
            yield client
    finally:
        engine.dispose()


def test_pg_create_task(pg_client):
    response = pg_client.post(
        "/tasks",
        json={"title": "PostgreSQL test"},
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "PostgreSQL test"
    assert data["completed"] is False
    assert data["created_at"] is not None


def test_pg_get_tasks(pg_client):
    pg_client.post(
        "/tasks",
        json={"title": "任务A"},
    )

    response = pg_client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_pg_update_task(pg_client):
    task = pg_client.post(
        "/tasks",
        json={"title": "旧任务"},
    ).json()

    response = pg_client.put(
        f"/tasks/{task['id']}",
        json={"title": "新任务"},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "新任务"


def test_pg_complete_task(pg_client):
    task = pg_client.post(
        "/tasks",
        json={"title": "待完成任务"},
    ).json()

    response = pg_client.patch(
        f"/tasks/{task['id']}/complete"
    )

    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_pg_delete_task(pg_client):
    task = pg_client.post(
        "/tasks",
        json={"title": "待删除任务"},
    ).json()

    response = pg_client.delete(
        f"/tasks/{task['id']}"
    )

    assert response.status_code == 200
    assert pg_client.get("/tasks").json() == []


def test_pg_stable_ids(pg_client):
    for title in ["A", "B", "C"]:
        pg_client.post(
            "/tasks",
            json={"title": title},
        )

    pg_client.delete("/tasks/2")

    tasks = pg_client.get("/tasks").json()

    assert [task["id"] for task in tasks] == [1, 3]

    response = pg_client.post(
        "/tasks",
        json={"title": "D"},
    )

    assert response.json()["id"] == 4


def test_pg_actual_database_write(pg_client):
    pg_client.post(
        "/tasks",
        json={"title": "真实数据库写入测试"},
    )

    engine, _ = create_database()

    try:
        with engine.connect() as conn:
            title = conn.execute(
                text("SELECT title FROM tasks")
            ).scalar_one()

        assert title == "真实数据库写入测试"
    finally:
        engine.dispose()
