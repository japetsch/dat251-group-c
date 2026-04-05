from datetime import datetime, timedelta

from pydantic import BaseModel

from app.db.sqlc.bookingslot import BookBookingslotRow, GetBookingSlotsRow


class BookingSlotDTO(BaseModel):
    id: int
    time: datetime
    duration: timedelta
    capacity: int
    bloodbank_id: int
    bloodbank_name: str
    location_id: int

    # Not part of the db model
    valid: bool

    @staticmethod
    def map_bookingslot(row: GetBookingSlotsRow, valid: bool) -> BookingSlotDTO:
        return BookingSlotDTO(
            id=row.id,
            time=row.time,
            duration=row.duration,
            capacity=row.capacity,
            bloodbank_id=row.bloodbank_id,
            bloodbank_name=row.bloodbank_name,
            location_id=row.location_id,
            valid=valid,
        )


class BookBookingSlotDTO(BaseModel):
    id: int
    donor_id: int
    bookingslot_id: int
    cancelled: bool

    @staticmethod
    def map(row: BookBookingslotRow) -> BookBookingSlotDTO:
        return BookBookingSlotDTO(
            id=row.id,
            donor_id=row.donor_id,
            bookingslot_id=row.bookingslot_id,
            cancelled=row.cancelled,
        )
