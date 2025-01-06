import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from app.database import Base
from app.models import User, Debt

# Interpretar o arquivo de configuração do logging
fileConfig(context.config.config_file_name)

# Adicionar a metadata do seu modelo para que o Alembic possa detectar alterações
target_metadata = Base.metadata

def run_migrations_offline():
    """Executa migrações em modo offline."""
    url = context.config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Executa migrações em modo online."""
    connectable = engine_from_config(
        context.config.get_section(context.config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

# Executa as migrações dependendo do modo (offline ou online)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
