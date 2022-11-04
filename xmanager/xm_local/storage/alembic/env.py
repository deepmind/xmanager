# Copyright 2021 DeepMind Technologies Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Alembic env.py."""

from logging import config as logging_config

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

config = context.config

if config.config_file_name is not None:
  logging_config.fileConfig(config.config_file_name)

target_metadata = None


def run_migrations_offline() -> None:
  """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
  """
  url = config.get_main_option('sqlalchemy.url')
  context.configure(
      url=url,
      target_metadata=target_metadata,
      literal_binds=True,
      dialect_opts={'paramstyle': 'named'},
  )

  with context.begin_transaction():
    context.run_migrations()


def run_migrations_online() -> None:
  """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
  """
  connectable = config.attributes.get('connection', None)

  if connectable is None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
      context.configure(connection=connection, target_metadata=target_metadata)

      with context.begin_transaction():
        context.run_migrations()
  else:
    context.configure(connection=connectable, target_metadata=target_metadata)

    with context.begin_transaction():
      context.run_migrations()


if context.is_offline_mode():
  run_migrations_offline()
else:
  run_migrations_online()