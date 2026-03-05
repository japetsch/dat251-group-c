import datetime

from fastapi import HTTPException
from fastapi.routing import APIRouter
from pydantic import BaseModel

from ..db.db import DBConnection
from ..db.sqlc.appointment import (
    AsyncQuerier as AppointmentQuerier,
    GetAllAppointmentsRow,
)
from ..db.sqlc.models import Appointment


class AppointmentRouter(APIRouter):
    def __init__(self) -> None:
        super().__init__()

        # Register the routes here. Dependencies are request-scoped
        self.add_api_route("", self.find_all, methods=["GET"])
        self.add_api_route("/{id}", self.delete_one, methods=["DELETE"])
        self.add_api_route("", self.update, methods=["PATCH"])

    async def find_all(self, engine: DBConnection) -> list[GetAllAppointmentsRow]:
        q = AppointmentQuerier(engine)

        rows: list[GetAllAppointmentsRow] = []
        async for x in q.get_all_appointments():
            rows.append(x)

        return rows

    class AppointmentUpdateRequest(BaseModel):
        id: int
        time: datetime.datetime

    async def update(
        self, updateRequest: AppointmentUpdateRequest, engine: DBConnection
    ) -> Appointment:
        q = AppointmentQuerier(engine)

        updatedAppointment: Appointment | None = await q.update_appointment(
            id=updateRequest.id, time=updateRequest.time
        )
        if updatedAppointment is None:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return updatedAppointment

    async def delete_one(self, id: int, engine: DBConnection) -> Appointment:
        q = AppointmentQuerier(engine)
        deletedAppointment: Appointment | None = await q.delete_appointment_by_id(id=id)
        if deletedAppointment is None:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return deletedAppointment
