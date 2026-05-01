from pydantic import BaseModel

from ..db.sqlc.bookingslot import (
    GetBookingSlotsRow,
)


class AvailableBookingSlot(GetBookingSlotsRow):
    valid: bool
    booked_by_user: bool


class BookAppointmentRequest(BaseModel):
    bookingslot_id: int
