from fastapi.routing import APIRouter

from app.auth import AdminInfo, CurrentUserOptional

from ..db.db import DBConnection
from ..db.sqlc.bloodbank import AsyncQuerier as BloodbankQuerier
from ..schemas.bloodbank import BloodbankDTO


class BloodbankRouter(APIRouter):
    def __init__(self) -> None:
        super().__init__(tags=["bloodbank"])
        self.add_api_route("", self.get_all_bloodbanks, methods=["GET"])

    async def get_all_bloodbanks(
        self, user: CurrentUserOptional, engine: DBConnection
    ) -> list[BloodbankDTO]:
        # If the current user is an admin, pass their admin id to the query, otherwise pass -1
        admin_id = -1
        if isinstance(user, AdminInfo):
            admin_id = user.admin_id

        q = BloodbankQuerier(engine)

        rows: list[BloodbankDTO] = []
        async for r in q.get_all_blood_banks(admin_id=admin_id):
            rows.append(BloodbankDTO.map_bloodbank(r))

        return rows
