from pydantic import BaseModel


class LoginRequestData(BaseModel):
    email: str
    password: str
