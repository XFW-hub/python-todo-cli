
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    create_engine,
    text,
)
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
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(
        nullable=False,
    )

    completed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("0"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )


def create_database(db_path):
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={
            "check_same_thread": False
        },
    )

    session_factory = sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )

    return engine, session_factory
