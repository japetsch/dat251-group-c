from pydantic import BaseModel


class UserInfo(BaseModel):
    user_id: int
    user_name: str


class DonorInfo(UserInfo):
    donor_id: int


class AdminInfo(UserInfo):
    admin_id: int
