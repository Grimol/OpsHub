from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# 1) Importer settings & metadata
from app.core.config import settings
from app.db.base import Base  # Base declarative
from app.db import models     # pour que les modèles soient importés
target_metadata = Base.metadata

config = context.config
# 2) Injecter dynamiquement l'URL DB
config.set_main_option("sqlalchemy.url", settings.database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(config.get_section(config.config_ini_section, {}), prefix='sqlalchemy.', poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
