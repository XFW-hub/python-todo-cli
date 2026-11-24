
from alembic import context
from sqlalchemy import create_engine

from database import Base, get_database_url


target_metadata = Base.metadata


def run_migrations_offline():
    url = get_database_url()

    if hasattr(url, "render_as_string"):
        url = url.render_as_string(
            hide_password=False
        )

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    url = get_database_url()
    engine = create_engine(url)

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
