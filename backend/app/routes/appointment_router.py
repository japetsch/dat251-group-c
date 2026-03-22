from fastapi import HTTPException
from fastapi.routing import APIRouter
from pydantic import BaseModel

from ..db.db import DBConnection
from ..db.sqlc.appointment import (
    AsyncQuerier as AppointmentQuerier,
    DeleteAppointmentByIdRow,
    GetAppointmentsByUserIdRow,
    UpdateAppointmentRow,
)
from ..db.sqlc.models import Appointment


class AppointmentRouter(APIRouter):
    def __init__(self) -> None:
        super().__init__()

        # Register the routes here. Dependencies are request-scoped
        self.add_api_route("/{id}", self.find_all, methods=["GET"])
        self.add_api_route("/{id}", self.update, methods=["PATCH"])
        self.add_api_route("/{id}", self.delete_one, methods=["DELETE"])

    async def find_all(
        self, id: int, engine: DBConnection
    ) -> list[GetAppointmentsByUserIdRow]:
        q = AppointmentQuerier(engine)

        rows: list[GetAppointmentsByUserIdRow] = []
        async for x in q.get_appointments_by_user_id(donor_id=id):
            rows.append(x)

        return rows

    class AppointmentUpdateRequest(BaseModel):
        bookingslot_id: int
        cancelled: bool

    async def update(
        self, id: int, updateRequest: AppointmentUpdateRequest, engine: DBConnection
    ) -> UpdateAppointmentRow:
        q = AppointmentQuerier(engine)

        updatedAppointment: UpdateAppointmentRow | None = await q.update_appointment(
            id=id,
            cancelled=updateRequest.cancelled,
            bookingslot_id=updateRequest.bookingslot_id,
        )
        if updatedAppointment is None:
            raise HTTPException(
                status_code=404,
                detail="Appointment not found or no capacity on booking slot",
            )
        return updatedAppointment

    async def delete_one(
        self, id: int, engine: DBConnection
    ) -> DeleteAppointmentByIdRow:
        q = AppointmentQuerier(engine)
        deletedAppointment: DeleteAppointmentByIdRow | None = (
            await q.delete_appointment_by_id(id=id)
        )
        if deletedAppointment is None:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return deletedAppointment
