from typing import final

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import HTTPException, Response, status
from fastapi.routing import APIRouter
from pydantic import BaseModel

from app.auth import (
    AdminInfo,
    AuthUtilDependency,
    CurrentUserRequired,
    DonorInfo,
    UserInfo,
)

from ..db.db import DBConnection
from ..db.sqlc.auth import AsyncQuerier as AuthQuerier


@final
class AuthRouter(APIRouter):
    def __init__(self) -> None:
        super().__init__()

        self.ph = PasswordHasher()

        # Register the routes here. Dependencies are request-scoped
        self.add_api_route(
            "/login",
            self.log_in,
            methods=["POST"],
            status_code=status.HTTP_204_NO_CONTENT,
            responses={
                status.HTTP_401_UNAUTHORIZED: {
                    "description": "Unauthorized. Incorrect email or password"
                }
            },
        )
        self.add_api_route(
            "/logout",
            self.log_out,
            methods=["GET"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self.add_api_route("/me", self.me, methods=["GET"])

    class LoginRequestData(BaseModel):
        email: str
        password: str

    async def log_in(
        self,
        data: LoginRequestData,
        engine: DBConnection,
        auth_utils: AuthUtilDependency,
        response: Response,
    ):
        q = AuthQuerier(engine)
        user = await q.get_user(email=data.email)
        if user is None or user.password_hash is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        try:
            _ = self.ph.verify(user.password_hash, data.password)
        except VerifyMismatchError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        if user.donor_id is not None:
            info = DonorInfo(
                user_id=user.id,
                user_name=user.name,
                donor_id=user.donor_id,
            )
        elif user.admin_id is not None:
            info = AdminInfo(
                user_id=user.id,
                user_name=user.name,
                admin_id=user.admin_id,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User entity is inconsistent",
            )

        auth_utils.set_auth_cookie(info, response)

    async def log_out(
        self, _: CurrentUserRequired, auth_utils: AuthUtilDependency, response: Response
    ):
        auth_utils.clear_auth_cookie(response)

    async def me(self, user: CurrentUserRequired) -> UserInfo:
        return user
