from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, Field

from ..db.sqlc.admin import (
    GetAppointmentsAtBloodBankRow,
)
from ..db.sqlc.models import BloodType
from .appointment import NoteType


class CreateBloodBankRequest(BaseModel):
    name: str
    street_name: str
    street_number: str
    postal_code: str
    city: str
    country: str = "NO"
    # TODO: make optional + use geocoding
    loc_lat: float
    loc_lon: float


class CreateBloodBankResponse(BaseModel):
    bloodbank_id: int


class MutateBloodbankAdminsRequest(BaseModel):
    admin_id: int


class BookingSlotType(GetAppointmentsAtBloodBankRow):
    appointments: list[AppointmentTypeAdmin]


class AppointmentTypeAdmin(BaseModel):
    appointment_id: int
    appointment_cancelled: bool
    donor_id: int
    donor_blood_type: BloodType | None
    donor_name: str
    donor_email: str
    donor_phone: str
    notes: list[NoteType]
    donations: list[DonationType]


class DonationType(BaseModel):
    donation_id: int
    amount_ml: float
    is_blood_not_plasma: bool


class RegisterDonationRequest(BaseModel):
    amount_ml: float
    is_blood_not_plasma: bool = True


class RegisterDonationResponse(BaseModel):
    donation_id: int


class AbstractTestResultRequest(BaseModel):
    submitted_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )
    ok_to_donate: bool
    validity_duration: timedelta


class RegisterInterviewRequest(AbstractTestResultRequest):
    pass


class RegisterDonationTestRequest(AbstractTestResultRequest):
    donation_id: int
