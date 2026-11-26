
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select

from database import Task, create_database

from cache import create_cache
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

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


def create_app(db_path=None):
    engine, SessionLocal = create_database(db_path)
    cache = create_cache()
    app = FastAPI(
        title="Python Todo API",
        version="1.5.0",
    )
    app.state.cache = cache
    
    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/tasks")
    def get_tasks():
        cached_tasks = cache.get_tasks()

        if cached_tasks is not None:
            return cached_tasks

        with SessionLocal() as session:
            tasks = session.scalars(
                select(Task).order_by(Task.id)
            ).all()

            result = [
                {
                    "id": task.id,
                    "title": task.title,
                    "completed": task.completed,
                    "created_at": task.created_at,
                }
                for task in tasks
            ]

            result = jsonable_encoder(result)

        cache.set_tasks(result)

        return result


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

            result = task_to_dict(task)
        cache.invalidate()
        return result

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
            result = task_to_dict(task)
        cache.invalidate()
        return result

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
            result = task_to_dict(task)
        cache.invalidate()
        return result

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

        cache.invalidate()
        return {
            "message": "任务已删除",
            "title": title,
        }

    return app


app = create_app()
