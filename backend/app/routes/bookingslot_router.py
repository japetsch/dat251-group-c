import datetime

from fastapi import HTTPException
from fastapi.routing import APIRouter
from pydantic import BaseModel

from ..db.db import DBConnection
from ..db.sqlc.bookingslot import (
    AsyncQuerier as BookingslotQuerier,
    BookBookingslotRow,
    GetBookingSlotsRow,
)
from ..db.sqlc.models import Appointment


class BookingslotRouter(APIRouter):
    def __init__(self) -> None:
        super().__init__()

        self.add_api_route("/available", self.get_available, methods=["GET"])
        self.add_api_route("/book", self.book, methods=["POST"])

    async def get_available(self, engine: DBConnection) -> list[GetBookingSlotsRow]:
        q = BookingslotQuerier(engine)
        rows: list[GetBookingSlotsRow] = []
        async for x in q.get_booking_slots():
            rows.append(x)
        return rows

    class BookAppointmentRequest(BaseModel):
        bookingslot_id: int
        donor_id: int

    async def book(
        self, request: BookAppointmentRequest, engine: DBConnection
    ) -> BookBookingslotRow:
        q = BookingslotQuerier(engine)
        booked: BookBookingslotRow | None = await q.book_bookingslot(
            bookingslot_id=request.bookingslot_id,
            donor_id=request.donor_id,
        )
        if booked is None:
            raise HTTPException(status_code=404, detail="Bookingslot not available")
        return booked
