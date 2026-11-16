
import os
from pathlib import Path

from alembic import context
from sqlalchemy import create_engine

from database import Base


target_metadata = Base.metadata

db_path = Path(
    os.getenv("TODO_DB_PATH", "tasks.db")
).expanduser().resolve()

db_url = f"sqlite:///{db_path.as_posix()}"


def run_migrations_offline():
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    db_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    engine = create_engine(db_url)

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()

    engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
