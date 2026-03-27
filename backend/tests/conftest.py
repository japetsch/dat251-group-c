import logging
import os
import subprocess
from pathlib import Path

import httpx
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import Settings
from app.db.db import DBManager
from app.main import app

logging.basicConfig(level=logging.INFO)


@pytest.fixture(scope="session", autouse=True)
async def migrate_test_db():
    """Create a fresh testing DB for the entire lifetime of the testing session"""
    settings = Settings.get_settings()
    db_url = settings.TEST_DB_URL.replace("+asyncpg", "") + "?sslmode=disable"
    env = {**os.environ, "DATABASE_URL": db_url}

    subprocess.run(["dbmate", "drop"], env=env, check=True)
    subprocess.run(["dbmate", "up"], env=env, check=True)

    sql = Path("./tests/db_mocks.sql").read_text()

    engine = create_async_engine(settings.TEST_DB_URL)

    statements = [stmt.strip() for stmt in sql.split(";") if stmt.strip()]

    async with engine.begin() as conn:
        for stmt in statements:
            await conn.execute(text(stmt))


@pytest.fixture(autouse=True)
async def test_db_conn():
    """
    Provide a DB connection wrapped in a transaction that is rolled back after
    each test, so tests never mutate the shared mock data.
    """
    settings = Settings.get_settings()
    engine = create_async_engine(settings.TEST_DB_URL)
    conn = await engine.connect()
    tx = await conn.begin()

    async def _override_get_db_connection():
        yield conn

    app.dependency_overrides[DBManager.get_db_connection] = _override_get_db_connection
    yield conn
    await tx.rollback()
    await conn.close()
    await engine.dispose()
    app.dependency_overrides.clear()


@pytest.fixture
async def client():
    async with app.router.lifespan_context(app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app, root_path=""),
            base_url="http://test",
        ) as c:
            yield c


@pytest.fixture
async def olav_client(client: httpx.AsyncClient):
    resp = await client.post(
        "/api/auth/login",
        json={"email": "olav@uib.no", "password": "correct horse battery staple"},
    )
    assert resp.status_code == 204
    return client


@pytest.fixture
async def peter_client(client: httpx.AsyncClient):
    resp = await client.post(
        "/api/auth/login",
        json={"email": "peter@hvl.no", "password": "password123"},
    )
    assert resp.status_code == 204
    return client


@pytest.fixture
async def sigrid_client(client: httpx.AsyncClient):
    resp = await client.post(
        "/api/auth/login",
        json={"email": "sigrid@gmain.com", "password": "hunter2"},
    )
    assert resp.status_code == 204
    return client


@pytest.fixture
async def admin_haukeland_client(client: httpx.AsyncClient):
    resp = await client.post(
        "/api/auth/login",
        json={"email": "admin@haukeland.no", "password": "hunter2"},
    )
    assert resp.status_code == 204
    return client


@pytest.fixture
async def admin_blodbuss_client(client: httpx.AsyncClient):
    resp = await client.post(
        "/api/auth/login",
        json={"email": "admin@blodbuss.no", "password": "hunter2"},
    )
    assert resp.status_code == 204
    return client
