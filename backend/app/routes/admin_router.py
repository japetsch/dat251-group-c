from typing import final

from fastapi.routing import APIRouter


@final
class AdminRouter(APIRouter):
    def __init__(self) -> None:
        super().__init__(
            tags=["admin"],
        )

        # Register the routes here. Dependencies are request-scoped
        self.add_api_route("", self.index, methods=["GET"])

    async def index(self):
        return "Hello, world"
