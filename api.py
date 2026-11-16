
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select

from database import Task, create_database


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1)


def task_to_dict(task):
    return {
        "id": task.id,
        "title": task.title,
        "completed": task.completed,
        "created_at": task.created_at.isoformat(),
    }


def create_app(db_path="tasks.db"):
    path = Path(db_path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    engine, SessionLocal = create_database(path)

    app = FastAPI(
        title="Python Todo API",
        version="1.5.0",
    )

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/tasks")
    def get_tasks():
        with SessionLocal() as session:
            tasks = session.scalars(
                select(Task).order_by(Task.id)
            ).all()

            return [
                task_to_dict(task)
                for task in tasks
            ]

    @app.post("/tasks", status_code=201)
    def create_task(payload: TaskCreate):
        title = payload.title.strip()

        if not title:
            raise HTTPException(
                status_code=422,
                detail="任务内容不能为空",
            )

        with SessionLocal.begin() as session:
            task = Task(title=title)
            session.add(task)
            session.flush()
            session.refresh(task)

            return task_to_dict(task)

    @app.put("/tasks/{task_id}")
    def update_task(task_id: int, payload: TaskUpdate):
        title = payload.title.strip()

        if not title:
            raise HTTPException(
                status_code=422,
                detail="任务内容不能为空",
            )

        with SessionLocal.begin() as session:
            task = session.get(Task, task_id)

            if task is None:
                raise HTTPException(
                    status_code=404,
                    detail="任务不存在",
                )

            task.title = title
            return task_to_dict(task)

    @app.patch("/tasks/{task_id}/complete")
    def complete_task(task_id: int):
        with SessionLocal.begin() as session:
            task = session.get(Task, task_id)

            if task is None:
                raise HTTPException(
                    status_code=404,
                    detail="任务不存在",
                )

            task.completed = True
            return task_to_dict(task)

    @app.delete("/tasks/{task_id}")
    def delete_task(task_id: int):
        with SessionLocal.begin() as session:
            task = session.get(Task, task_id)

            if task is None:
                raise HTTPException(
                    status_code=404,
                    detail="任务不存在",
                )

            title = task.title
            session.delete(task)

            return {
                "message": "任务已删除",
                "title": title,
            }

    return app


DB_PATH = os.getenv("TODO_DB_PATH", "tasks.db")
app = create_app(DB_PATH)
