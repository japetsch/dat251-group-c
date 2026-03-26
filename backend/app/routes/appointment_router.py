from datetime import datetime, timedelta

from fastapi import HTTPException, status
from fastapi.routing import APIRouter
from pydantic import BaseModel

from app.auth import DonorInfo, DonorUserRequired, UserUnionRequired

from ..db.db import DBConnection
from ..db.sqlc.appointment import (
    AsyncQuerier as AppointmentQuerier,
    GetAppointmentsByDonorIdRow,
    UpdateAppointmentRow,
)
from ..db.sqlc.auth import AsyncQuerier as AuthQuerier


class AppointmentRouter(APIRouter):
    def __init__(self) -> None:
        super().__init__()

        # Register the routes here. Dependencies are request-scoped
        self.add_api_route("", self.find_all, methods=["GET"])
        self.add_api_route("/{appointment_id}", self.update, methods=["PATCH"])
        self.add_api_route(
            "/{appointment_id}/note",
            self.add_note,
            methods=["POST"],
            status_code=status.HTTP_204_NO_CONTENT,
        )

    class AppointmentType(BaseModel):
        id: int
        username: str
        time: datetime
        duration: timedelta
        bloodbank_name: str
        cancelled: bool
        notes: list[AppointmentRouter.NoteType]

    # TODO: refactor (this is duplicate of a structure in AdminRouter)
    class NoteType(BaseModel):
        author_user_id: int
        author_name: str
        message: str
        time: datetime

    async def find_all(
        self, user: DonorUserRequired, engine: DBConnection
    ) -> list[AppointmentRouter.AppointmentType]:
        q = AppointmentQuerier(engine)

        rows: list[AppointmentRouter.AppointmentType] = []
        async for x in q.get_appointments_by_donor_id(donor_id=user.donor_id):
            rows.append(
                AppointmentRouter.AppointmentType.model_validate(
                    x, from_attributes=True
                )
            )
        return rows

    async def _assert_appointment_owner(
        self, appointment_id: int, donor_id: int, engine: DBConnection
    ):
        aq = AuthQuerier(engine)

        access = await aq.appointment_belongs_to(
            appointment_id=appointment_id, donor_id=donor_id
        )
        if not access:
            raise HTTPException(
                status_code=404,
                detail="Appointment not found",
            )

    class AppointmentUpdateRequest(BaseModel):
        bookingslot_id: int
        cancelled: bool

    async def update(
        self,
        appointment_id: int,
        updateRequest: AppointmentUpdateRequest,
        user: UserUnionRequired,
        engine: DBConnection,
    ) -> UpdateAppointmentRow:
        """
        Update an appointment, either changing its booking slot or cancelling it altogether

        This action can be performed by the donor or an admin at the blood bank(s) in question

        TODO:
        - validate that requested bookingslot works
        - add appointment note entry documenting the change
        """
        if isinstance(user, DonorInfo):
            await self._assert_appointment_owner(appointment_id, user.donor_id, engine)
        else:
            # TODO: refactor. Check is duplicate of AdminRouter._assert_appt_access
            aq = AuthQuerier(engine)
            res = await aq.has_admin_where_appointment_is(
                appointment_id=appointment_id, admin_id=user.admin_id
            )
            if not res:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User is not admin for this appointment",
                )

        q = AppointmentQuerier(engine)
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

    class AppointmentNote(BaseModel):
        message: str

    async def add_note(
        self,
        user: DonorUserRequired,
        appointment_id: int,
        data: AppointmentNote,
        engine: DBConnection,
    ):
        await self._assert_appointment_owner(appointment_id, user.donor_id, engine)
        q = AppointmentQuerier(engine)
        await q.add_note(
            appointment_id=appointment_id,
            author_id=user.user_id,  # NOTE: this is the user_id, not admin_id
            message=data.message,
        )
