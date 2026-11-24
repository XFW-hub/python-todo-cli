
import os
from datetime import datetime
from pathlib import Path

from sqlalchemy import (
    Boolean,
    DateTime,
    create_engine,
    text,
)
from sqlalchemy.engine import URL
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
)


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    __table_args__ = {
        "sqlite_autoincrement": True
    }

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        nullable=False
    )

    completed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )


def get_database_url(db_path=None):
    # 显式传入 db_path 时使用 SQLite
    if db_path is not None:
        path = Path(db_path).resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{path}"

    # Docker Compose 环境使用 PostgreSQL
    if os.getenv("DB_HOST"):
        return URL.create(
            drivername="postgresql+psycopg",
            username=os.getenv("DB_USER", "todo_user"),
            password=os.environ["DB_PASSWORD"],
            host=os.environ["DB_HOST"],
            port=int(os.getenv("DB_PORT", "5432")),
            database=os.getenv("DB_NAME", "todo_db"),
        )

    # 默认使用 SQLite
    path = Path(
        os.getenv("TODO_DB_PATH", "tasks.db")
    ).resolve()

    path.parent.mkdir(parents=True, exist_ok=True)

    return f"sqlite:///{path}"


def create_database(db_path=None):
    url = get_database_url(db_path)

    kwargs = {}

    if str(url).startswith("sqlite:"):
        kwargs["connect_args"] = {
            "check_same_thread": False
        }

    engine = create_engine(
        url,
        pool_pre_ping=True,
        **kwargs,
    )

    session_factory = sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )

    return engine, session_factory
