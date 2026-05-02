from pydantic import BaseModel

from ..db.sqlc.models import BloodType


class LoginRequestData(BaseModel):
    email: str
    password: str


class RegisterDonorRequestData(BaseModel):
    email: str
    password: str

    name: str
    phone_number: str
    street_name: str
    street_number: str
    apt_number: str | None
    postal_code: str
    city: str
    country: str

    preferred_bloodbank_id: int
    blood_type: BloodType | None
