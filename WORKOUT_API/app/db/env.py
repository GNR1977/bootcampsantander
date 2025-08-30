from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy import create_engine
from alembic import context
import os

from app.db.base import Base
from app.models.user import User
from app.models.athlete import Athlete
from app.models.wod import WOD
from app.models.heat import Heat
from app.models.score import Score

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    url = os.getenv("DATABASE_URL_SYNC", "postgresql://app:app@localhost:5432/crossfit")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(os.getenv("DATABASE_URL_SYNC", "postgresql://app:app@localhost:5432/crossfit"), poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()