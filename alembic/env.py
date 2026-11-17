
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Application database configuration
from app.core.config import DATABASE_URL

# Import your SQLAlchemy Base
from app.database.base import Base

# Import all models for Alembic autogenerate
from app.models.student import Student


# Alembic configuration
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Validate database URL
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is missing. Please check your .env file."
    )


# Override URL from alembic.ini with application DATABASE_URL
config.set_main_option(
    "sqlalchemy.url",
    DATABASE_URL.replace("%", "%%")
)


# SQLAlchemy metadata for autogenerate
target_metadata = Base.metadata


# --------------------------------------------------
# OFFLINE MIGRATIONS
# --------------------------------------------------

def run_migrations_offline() -> None:

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# --------------------------------------------------
# ONLINE MIGRATIONS
# --------------------------------------------------

def do_run_migrations(connection):

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:

        await connection.run_sync(
            do_run_migrations
        )

    await connectable.dispose()


def run_migrations_online() -> None:

    asyncio.run(run_async_migrations())


# --------------------------------------------------
# EXECUTION
# --------------------------------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
