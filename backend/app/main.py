from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRoute

from .config import Settings
from .db.db import create_db_engine
from .routes.index_router import IndexRouter


class Main:
    app: FastAPI

    def __init__(self):
        self.app = FastAPI(
            lifespan=self.lifespan,
            title="Blood Bank API",
            description="API for the Blood Bank project",
            version="0.1.0",
            root_path="/api",
            docs_url="/docs",
            redoc_url="/redoc",
        )

        # Include custom routers here
        self.app.include_router(IndexRouter())

        # Make the OpenAPI operation ids match the route function name
        # Ensures nicer names on the generated client
        for route in self.app.routes:
            if isinstance(route, APIRoute):
                route.operation_id = route.name

    @classmethod
    @asynccontextmanager
    async def lifespan(cls, app: FastAPI):
        """
        Context manager to manage dependencies that last the entire lifetime of the app.
        """
        settings = Settings.get_settings()

        print("Creating SQLAlchemy engine...")
        app.state.db_engine = create_db_engine(settings)

        yield

        print("Disposing SQLAlchemy engine...")
        await app.state.db_engine.dispose()
        print("SQLAlchemy engine disposed.")


app = Main().app
