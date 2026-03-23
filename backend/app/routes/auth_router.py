from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi.routing import APIRouter
from pydantic import BaseModel

from ..db.db import DBConnection
from ..db.sqlc.auth import AsyncQuerier as AuthQuerier


class AuthRouter(APIRouter):
    def __init__(self) -> None:
        super().__init__()

        self.ph = PasswordHasher()

        # Register the routes here. Dependencies are request-scoped
        self.add_api_route("/login", self.log_in, methods=["POST"])

    class LoginRequest(BaseModel):
        email: str
        password: str

    async def log_in(self, req: LoginRequest, engine: DBConnection):
        q = AuthQuerier(engine)
        user = await q.get_user(email=req.email)
        if user is None or user.password_hash is None:
            return "failure"

        try:
            password_valid = self.ph.verify(user.password_hash, req.password)
        except VerifyMismatchError:
            password_valid = False

        if not password_valid:
            return "failure"

        return "hello, world"
