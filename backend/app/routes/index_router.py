from fastapi.routing import APIRouter

from ..db.db import DBConnection
from ..db.sqlc.first_table import AsyncQuerier as FirstTableQuerier


class IndexRouter(APIRouter):
    def __init__(self) -> None:
        super().__init__()

        # Register the routes here. Dependencies are request-scoped
        self.add_api_route("/", self.index, methods=["GET"])

    async def index(self, engine: DBConnection):
        q = FirstTableQuerier(engine)

        rows = []
        async for x in q.get_all_rows():
            rows.append(x)

        return rows
