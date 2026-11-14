
import os
from pathlib import Path
from threading import Lock

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from todo import TodoList


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)


def create_app(file_path="tasks.json"):
    app = FastAPI(
        title="Python Todo API",
        version="1.3.0",
    )

    todo = TodoList()
    todo.load_tasks(file_path)
    lock = Lock()

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/tasks")
    def get_tasks():
        with lock:
            tasks = todo.get_tasks()

        return [
            {"id": index, "title": title}
            for index, title in enumerate(tasks, start=1)
        ]

    @app.post("/tasks", status_code=201)
    def create_task(payload: TaskCreate):
        with lock:
            try:
                todo.add_task(payload.title)
            except ValueError as exc:
                raise HTTPException(
                    status_code=422,
                    detail=str(exc),
                ) from exc

            todo.save_tasks(file_path)
            tasks = todo.get_tasks()

            return {
                "id": len(tasks),
                "title": tasks[-1],
            }

    @app.delete("/tasks/{task_id}")
    def delete_task(task_id: int):
        with lock:
            try:
                removed = todo.delete_task(task_id)
            except IndexError as exc:
                raise HTTPException(
                    status_code=404,
                    detail=str(exc),
                ) from exc

            todo.save_tasks(file_path)

            return {
                "message": "任务已删除",
                "title": removed,
            }

    return app


DATA_FILE = Path(os.getenv("TODO_DATA_FILE", "tasks.json"))
app = create_app(DATA_FILE)
