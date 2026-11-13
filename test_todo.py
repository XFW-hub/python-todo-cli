
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
