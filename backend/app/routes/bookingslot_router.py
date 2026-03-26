from datetime import timedelta

from fastapi import HTTPException
from fastapi.routing import APIRouter
from pydantic import BaseModel

from app.auth import DonorUserRequired

from ..db.db import DBConnection
from ..db.sqlc.appointment import (
    AsyncQuerier as AppointmentQuerier,
    GetAppointmentsByDonorIdRow,
)
from ..db.sqlc.bookingslot import (
    AsyncQuerier as BookingslotQuerier,
    BookBookingslotRow,
    GetBookingSlotsRow,
)


class BookingslotRouter(APIRouter):
    def __init__(self) -> None:
        super().__init__()

        self.add_api_route("/available", self.get_available, methods=["GET"])
        self.add_api_route("/book", self.book, methods=["POST"])

    class AvailableBookingSlot(GetBookingSlotsRow):
        valid: bool

    async def get_available(
        self, user: DonorUserRequired, engine: DBConnection
    ) -> list[AvailableBookingSlot]:
        q = BookingslotQuerier(engine)
        a = AppointmentQuerier(engine)
        # Approximate 3 months since timedelta can't compare months
        MIN_WAITTIME = timedelta(days=90)

        appointments: list[GetAppointmentsByDonorIdRow] = []
        async for x in a.get_appointments_by_donor_id(donor_id=user.donor_id):
            appointments.append(x)

        rows: list[BookingslotRouter.AvailableBookingSlot] = []
        async for x in q.get_booking_slots():
            lower = x.time - MIN_WAITTIME
            upper = x.time + MIN_WAITTIME

            is_valid = x.capacity != 0 and not any(
                (lower < a.time < upper and a.cancelled != True) for a in appointments
            )
            rows.append(self.AvailableBookingSlot(**x.model_dump(), valid=is_valid))
        return rows

    class BookAppointmentRequest(BaseModel):
        bookingslot_id: int

    async def book(
        self,
        request: BookAppointmentRequest,
        user: DonorUserRequired,
        engine: DBConnection,
    ) -> BookBookingslotRow:
        q = BookingslotQuerier(engine)
        booked: BookBookingslotRow | None = await q.book_bookingslot(
            bookingslot_id=request.bookingslot_id,
            donor_id=user.donor_id,
        )
        if booked is None:
            raise HTTPException(status_code=404, detail="Bookingslot not available")
        return booked
