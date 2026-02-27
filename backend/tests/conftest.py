import logging
import os
import subprocess

import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import Settings
from app.db.db import DBManager
from app.main import app

logging.basicConfig(level=logging.INFO)


@pytest.fixture(scope="session", autouse=True)
def migrate_test_db():
    """Create a fresh testing DB for the entire lifetime of the testing session"""
    settings = Settings.get_settings()
    db_url = settings.TEST_DB_URL.replace("+asyncpg", "") + "?sslmode=disable"
    env = {**os.environ, "DATABASE_URL": db_url}

    subprocess.run(["dbmate", "drop"], env=env, check=True)
    subprocess.run(["dbmate", "up"], env=env, check=True)

    cat = subprocess.Popen(
        ["cat", "./tests/db_mocks.sql"],
        stdout=subprocess.PIPE,
    )

    subprocess.run(
        [
            "docker",
            "exec",
            "-i",
            "postgres",
            "psql",
            "-h",
            "localhost",
            "-U",
            "postgres",
            "-f-",
        ],
        stdin=cat.stdout,
        check=True,
        env=env,
    )


async def _override_get_db_connection():
    settings = Settings.get_settings()
    engine = create_async_engine(settings.TEST_DB_URL)
    async with engine.begin() as conn:
        yield conn
    await engine.dispose()


@pytest.fixture(autouse=True)
def use_test_db():
    app.dependency_overrides[DBManager.get_db_connection] = _override_get_db_connection
    yield
    app.dependency_overrides.clear()
