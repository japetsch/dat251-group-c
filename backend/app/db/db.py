from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine

from app.config import Settings


class DBManager:
    @classmethod
    def create_db_engine(cls, settings: Settings) -> AsyncEngine:
        return create_async_engine(settings.DB_URL)

    @classmethod
    async def get_db_connection(
        cls, request: Request
    ) -> AsyncGenerator[AsyncConnection, None]:
        """
        Provides a connection and a transaction context.
        Handles transaction (commit on success, rollback on error) automatically.
        """
        engine: AsyncEngine = request.app.state.db_engine
        async with engine.begin() as conn:
            yield conn


# Injectable dependency for our routes
DBConnection = Annotated[AsyncConnection, Depends(DBManager.get_db_connection)]
