
import os

import pytest

from cache import TaskCache


pytestmark = [
    pytest.mark.redis,
    pytest.mark.skipif(
        os.getenv("RUN_REDIS_TESTS") != "1",
        reason="Redis tests are disabled",
    ),
]


@pytest.fixture
def task_cache():
    cache = TaskCache(
        url="redis://127.0.0.1:6380/0",
        ttl=60,
    )

    cache.client.ping()
    cache.invalidate()

    try:
        yield cache
    finally:
        cache.invalidate()
        cache.close()


def test_cache_miss(task_cache):
    assert task_cache.get_tasks() is None


def test_cache_hit(task_cache):
    tasks = [
        {"id": 1, "title": "Redis test"}
    ]

    task_cache.set_tasks(tasks)

    assert task_cache.get_tasks() == tasks


def test_cache_empty_list(task_cache):
    task_cache.set_tasks([])

    assert task_cache.get_tasks() == []


def test_cache_ttl(task_cache):
    task_cache.set_tasks([])

    ttl = task_cache.client.ttl(
        task_cache.TASKS_KEY
    )

    assert 0 < ttl <= 60


def test_cache_invalidation(task_cache):
    task_cache.set_tasks([
        {"id": 1, "title": "Old task"}
    ])

    task_cache.invalidate()

    assert task_cache.get_tasks() is None


def test_cache_disabled():
    cache = TaskCache(url=None)

    assert cache.get_tasks() is None

    cache.set_tasks([])
    cache.invalidate()
    cache.close()


def test_cache_unavailable():
    cache = TaskCache(
        url="redis://127.0.0.1:1/0"
    )

    try:
        assert cache.get_tasks() is None

        cache.set_tasks([])
        cache.invalidate()

    finally:
        cache.close()


from fastapi.testclient import TestClient
from alembic import command
from alembic.config import Config

from api import create_app


def test_api_cache_consistency(
    task_cache,
    tmp_path,
    monkeypatch,
):
    db_path = tmp_path / "cache_test.db"

    # 确保使用独立 SQLite 测试数据库
    monkeypatch.delenv(
        "DB_HOST",
        raising=False,
    )

    monkeypatch.setenv(
        "TODO_DB_PATH",
        str(db_path),
    )

    monkeypatch.setenv(
        "REDIS_URL",
        "redis://127.0.0.1:6380/0",
    )

    command.upgrade(
        Config("alembic.ini"),
        "head",
    )

    app = create_app(db_path)

    with TestClient(app) as client:

        response = client.get("/tasks")

        assert response.status_code == 200
        assert response.json() == []
        assert task_cache.get_tasks() == []

        response = client.post(
            "/tasks",
            json={"title": "New task"},
        )

        assert response.status_code == 201

        # 新增任务后，旧缓存必须失效
        assert task_cache.get_tasks() is None

        response = client.get("/tasks")

        assert response.status_code == 200

        tasks = response.json()

        assert len(tasks) == 1
        assert tasks[0]["title"] == "New task"

        # 再次查询后，缓存重新生成
        assert task_cache.get_tasks() == tasks
