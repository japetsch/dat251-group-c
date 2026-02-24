from fastapi.routing import APIRouter

from ..db.db import DBConnection
from ..db.sqlc.appointment import (
    AsyncQuerier as AppointmentQuerier,
    GetAllAppointmentsRow,
)


class AppointmentRouter(APIRouter):
    def __init__(self) -> None:
        super().__init__()

        # Register the routes here. Dependencies are request-scoped
        self.add_api_route("", self.find_all, methods=["GET"])

    async def find_all(self, engine: DBConnection) -> list[GetAllAppointmentsRow]:
        q = AppointmentQuerier(engine)

        rows: list[GetAllAppointmentsRow] = []
        async for x in q.get_all_appointments():
            rows.append(x)

        return rows
