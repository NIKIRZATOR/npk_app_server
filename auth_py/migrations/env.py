from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

from app.db import Base
from app.config import settings

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Подставляем ENV в placeholders alembic.ini
config.set_main_option("DB_USERNAME", settings.DB_USERNAME)
config.set_main_option("DB_PASSWORD", settings.DB_PASSWORD)
config.set_main_option("DB_HOST", settings.DB_HOST)
config.set_main_option("DB_PORT", str(settings.DB_PORT))
config.set_main_option("DB_NAME", settings.DB_NAME)

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
