from pydantic import BaseModel

from ..db.sqlc.bookingslot import (
    GetBookingSlotsRow,
)


class AvailableBookingSlot(GetBookingSlotsRow):
    valid: bool


class BookAppointmentRequest(BaseModel):
    bookingslot_id: int
