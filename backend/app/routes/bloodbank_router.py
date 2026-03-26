from fastapi.routing import APIRouter
from pydantic import BaseModel

from app.auth import CurrentUserOptional

from ..db.db import DBConnection
from ..db.sqlc.bloodbank import AsyncQuerier as BloodbankQuerier


class BloodbankRouter(APIRouter):
    def __init__(self) -> None:
        super().__init__(tags=["bloodbank"])
        self.add_api_route("", self.get_all_bloodbanks, methods=["GET"])

    class BloodbankResponse(BaseModel):
        bloodbank_id: int
        name: str
        street_name: str
        street_number: str
        postal_code: str
        city: str
        country: str
        user_has_admin_access: bool

    async def get_all_bloodbanks(
        self, user: CurrentUserOptional, engine: DBConnection
    ) -> list[BloodbankResponse]:
        # If the current user is an admin, pass their admin id to the query, otherwise pass -1
        admin_id = -1
        if user is not None and getattr(user, "admin_id", None) is not None:
            admin_id = user.admin_id

        q = BloodbankQuerier(engine)

        rows: list = []
        async for r in q.get_all_blood_banks(admin_id=admin_id):
            rows.append(r)

        out: list[BloodbankRouter.BloodbankResponse] = [
            BloodbankRouter.BloodbankResponse(**r.model_dump()) for r in rows
        ]

        return out
