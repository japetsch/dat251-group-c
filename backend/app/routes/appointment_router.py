import datetime

from fastapi import HTTPException
from fastapi.routing import APIRouter
from pydantic import BaseModel

from ..db.db import DBConnection
from ..db.sqlc.appointment import (
    AsyncQuerier as AppointmentQuerier,
    GetAllAppointmentsRow,
)
from ..db.sqlc.free_appointment import (
    AsyncQuerier as FreeAppointmentQuerier,
    GetAvailableAppointmentsRow,
)
from ..db.sqlc.models import Appointment


class AppointmentRouter(APIRouter):
    def __init__(self) -> None:
        super().__init__()

        # Register the routes here. Dependencies are request-scoped
        self.add_api_route("", self.find_all, methods=["GET"])
        self.add_api_route("/available", self.get_available, methods=["GET"])
        self.add_api_route("/book", self.book, methods=["POST"])
        self.add_api_route("", self.update, methods=["PATCH"])
        self.add_api_route("/{id}", self.delete_one, methods=["DELETE"])

    async def find_all(self, engine: DBConnection) -> list[GetAllAppointmentsRow]:
        q = AppointmentQuerier(engine)

        rows: list[GetAllAppointmentsRow] = []
        async for x in q.get_all_appointments():
            rows.append(x)

        return rows

    class AppointmentUpdateRequest(BaseModel):
        id: int
        time: datetime.datetime

    class BookAppointmentRequest(BaseModel):
        free_appointment_id: int
        user_id: int

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

    async def get_available(
        self, engine: DBConnection
    ) -> list[GetAvailableAppointmentsRow]:
        q = FreeAppointmentQuerier(engine)
        rows: list[GetAvailableAppointmentsRow] = []
        async for x in q.get_available_appointments():
            rows.append(x)
        return rows

    async def book(
        self, request: BookAppointmentRequest, engine: DBConnection
    ) -> Appointment:
        q = AppointmentQuerier(engine)
        booked: Appointment | None = await q.book_appointment(
            free_appointment_id=request.free_appointment_id,
            user_id=request.user_id,
        )
        if booked is None:
            raise HTTPException(status_code=404, detail="Free appointment not found")
        return booked
