from fastapi import HTTPException
from fastapi.routing import APIRouter
from pydantic import BaseModel

from app.auth import DonorUserRequired

from ..db.db import DBConnection
from ..db.sqlc.appointment import (
    AsyncQuerier as AppointmentQuerier,
    DeleteAppointmentByIdRow,
    GetAppointmentsByUserIdRow,
    UpdateAppointmentRow,
)
from ..db.sqlc.auth import AsyncQuerier as AuthQuerier


class AppointmentRouter(APIRouter):
    def __init__(self) -> None:
        super().__init__()

        # Register the routes here. Dependencies are request-scoped
        self.add_api_route("", self.find_all, methods=["GET"])
        self.add_api_route("/{appointment_id}", self.update, methods=["PATCH"])
        self.add_api_route("/{appointment_id}", self.delete_one, methods=["DELETE"])

    async def find_all(
        self, user: DonorUserRequired, engine: DBConnection
    ) -> list[GetAppointmentsByUserIdRow]:
        q = AppointmentQuerier(engine)

        rows: list[GetAppointmentsByUserIdRow] = []
        async for x in q.get_appointments_by_user_id(donor_id=user.donor_id):
            rows.append(x)

        return rows

    class AppointmentUpdateRequest(BaseModel):
        bookingslot_id: int
        cancelled: bool

    async def update(
        self,
        appointment_id: int,
        updateRequest: AppointmentUpdateRequest,
        user: DonorUserRequired,
        engine: DBConnection,
    ) -> UpdateAppointmentRow:
        q = AppointmentQuerier(engine)
        aq = AuthQuerier(engine)

        access = await aq.appointment_belongs_to(
            appointment_id=appointment_id, donor_id=user.donor_id
        )
        if not access:
            raise HTTPException(
                status_code=404,
                detail="Appointment not found",
            )

        updatedAppointment: UpdateAppointmentRow | None = await q.update_appointment(
            id=appointment_id,
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
        self, appointment_id: int, user: DonorUserRequired, engine: DBConnection
    ) -> DeleteAppointmentByIdRow:
        q = AppointmentQuerier(engine)
        aq = AuthQuerier(engine)

        access = await aq.appointment_belongs_to(
            appointment_id=appointment_id, donor_id=user.donor_id
        )
        if not access:
            raise HTTPException(
                status_code=404,
                detail="Appointment not found",
            )

        deletedAppointment: DeleteAppointmentByIdRow | None = (
            await q.delete_appointment_by_id(id=appointment_id)
        )
        if deletedAppointment is None:
            raise HTTPException(status_code=404, detail="Appointment not found")

        return deletedAppointment
