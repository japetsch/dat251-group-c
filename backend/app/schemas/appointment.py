from datetime import datetime, timedelta

from pydantic import BaseModel


class AppointmentType(BaseModel):
    id: int
    username: str
    time: datetime
    duration: timedelta
    bloodbank_name: str
    cancelled: bool
    notes: list[NoteType]


class NoteType(BaseModel):
    author_user_id: int
    author_name: str
    message: str
    time: datetime


class AppointmentUpdateRequest(BaseModel):
    bookingslot_id: int
    cancelled: bool


class AddNoteRequest(BaseModel):
    message: str
