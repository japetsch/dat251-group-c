from datetime import datetime, timedelta
from typing import Any

from pydantic import BaseModel

from ..db.sqlc.appointment import GetAppointmentsByDonorIdRow, UpdateAppointmentRow


class AppointmentDTO(BaseModel):
    id: int
    username: str
    time: datetime
    duration: timedelta
    bloodbank_name: str
    cancelled: bool
    notes: list[NoteDTO]

    @staticmethod
    def map_appointment(row: GetAppointmentsByDonorIdRow) -> AppointmentDTO:
        return AppointmentDTO(
            id=row.id,
            username=row.username,
            time=row.time,
            duration=row.duration,
            bloodbank_name=row.bloodbank_name,
            cancelled=row.cancelled,
            notes=[NoteDTO.map_note(n) for n in row.notes],
        )


class AppointmentUpdateDTO(BaseModel):
    id: int
    bookingslot_id: int
    cancelled: bool
    donor_id: int

    @staticmethod
    def map_appointment_update(row: UpdateAppointmentRow) -> AppointmentUpdateDTO:
        return AppointmentUpdateDTO(
            id=row.id,
            bookingslot_id=row.bookingslot_id,
            cancelled=row.cancelled,
            donor_id=row.donor_id,
        )


class NoteDTO(BaseModel):
    author_user_id: int
    author_name: str
    message: str
    time: datetime

    @staticmethod
    def map_note(row: Any) -> NoteDTO:
        return NoteDTO(
            author_user_id=row["author_user_id"],
            author_name=row["author_name"],
            message=row["message"],
            time=row["time"],
        )
