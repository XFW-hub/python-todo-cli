
import pytest

from todo import TodoList


def test_add_task():
    todo = TodoList()
    todo.add_task("学习 Python")

    assert todo.get_tasks() == ["学习 Python"]


def test_add_multiple_tasks():
    todo = TodoList()
    todo.add_task("学习 Git")
    todo.add_task("学习 pytest")

    assert todo.get_tasks() == [
        "学习 Git",
        "学习 pytest",
    ]


def test_add_empty_task():
    todo = TodoList()

    with pytest.raises(ValueError):
        todo.add_task("   ")


def test_get_empty_tasks():
    todo = TodoList()

    assert todo.get_tasks() == []


def test_get_tasks_returns_copy():
    todo = TodoList()
    todo.add_task("学习 Python")

    tasks = todo.get_tasks()
    tasks.clear()

    assert todo.get_tasks() == ["学习 Python"]


def test_delete_task():
    todo = TodoList()
    todo.add_task("学习 Git")
    todo.add_task("学习 Python")

    removed = todo.delete_task(1)

    assert removed == "学习 Git"
    assert todo.get_tasks() == ["学习 Python"]


def test_delete_invalid_task():
    todo = TodoList()
    todo.add_task("学习 Python")

    with pytest.raises(IndexError):
        todo.delete_task(10)


def test_delete_zero_index():
    todo = TodoList()
    todo.add_task("学习 Git")

    with pytest.raises(IndexError):
        todo.delete_task(0)


def test_delete_from_empty_list():
    todo = TodoList()

    with pytest.raises(IndexError):
        todo.delete_task(1)


def test_save_tasks(tmp_path):
    todo = TodoList()
    todo.add_task("学习 Git")

    file_path = tmp_path / "tasks.json"
    todo.save_tasks(file_path)

    assert file_path.exists()

    import json
    data = json.loads(
        file_path.read_text(encoding="utf-8")
    )
    assert data == {"tasks": ["学习 Git"]}


def test_load_tasks(tmp_path):
    file_path = tmp_path / "tasks.json"

    file_path.write_text(
        '{"tasks": ["学习 Python"]}',
        encoding="utf-8"
    )

    todo = TodoList()
    todo.load_tasks(file_path)

    assert todo.get_tasks() == ["学习 Python"]


def test_save_and_reload(tmp_path):
    file_path = tmp_path / "tasks.json"

    todo1 = TodoList()
    todo1.add_task("学习 pytest")
    todo1.save_tasks(file_path)

    todo2 = TodoList()
    todo2.load_tasks(file_path)

    assert todo2.get_tasks() == ["学习 pytest"]


def test_load_missing_file(tmp_path):
    file_path = tmp_path / "missing.json"

    todo = TodoList()
    todo.load_tasks(file_path)

    assert todo.get_tasks() == []


def test_load_invalid_json(tmp_path):
    file_path = tmp_path / "tasks.json"

    file_path.write_text(
        "{invalid json}",
        encoding="utf-8"
    )

    todo = TodoList()

    with pytest.raises(ValueError):
        todo.load_tasks(file_path)


def test_load_invalid_structure(tmp_path):
    file_path = tmp_path / "tasks.json"

    file_path.write_text(
        '{"tasks": [123, null]}',
        encoding="utf-8"
    )

    todo = TodoList()

    with pytest.raises(ValueError):
        todo.load_tasks(file_path)

