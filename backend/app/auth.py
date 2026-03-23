from typing import Annotated, final

import jwt
from fastapi import Depends, HTTPException, Request, Response, status
from jwt.exceptions import DecodeError
from pydantic import BaseModel

from app.config import Settings


class UserInfo(BaseModel):
    user_id: int
    user_name: str
    extended: DonorInfo | AdminInfo


class DonorInfo(BaseModel):
    donor_id: int


class AdminInfo(BaseModel):
    admin_id: int


@final
class AuthUtil:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def set_auth_cookie(self, user_info: UserInfo, response: Response):
        token = jwt.encode(
            user_info.model_dump(), self._settings.JWT_SECRET, algorithm="HS256"
        )
        response.set_cookie(
            key=self._settings.COOKIE_NAME,
            value=token,
            httponly=True,
            secure=False,  # TODO: set this to True (breaks the TestClient)
            samesite="strict",
            max_age=3600,  # 1 hour
        )

    def clear_auth_cookie(self, response: Response):
        response.delete_cookie(self._settings.COOKIE_NAME)

    def token_validate_and_renew(
        self, request: Request, response: Response
    ) -> UserInfo | None:
        token_str = request.cookies.get(self._settings.COOKIE_NAME)
        if not token_str:
            return None

        # TODO: Validate more properly (checking timestamps etc.)
        try:
            token = jwt.decode(
                token_str, self._settings.JWT_SECRET, algorithms=["HS256"]
            )
        except DecodeError:
            raise

        user = UserInfo.model_validate(token)

        # Renew the token
        self.set_auth_cookie(user, response)

        return user

    @staticmethod
    def get_current_user_optional(
        request: Request, response: Response
    ) -> UserInfo | None:
        s = AuthUtil.get_auth_util(request)
        return s.token_validate_and_renew(request, response)

    @staticmethod
    def get_current_user_required(request: Request, response: Response) -> UserInfo:
        u = AuthUtil.get_current_user_optional(request, response)
        if u is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )

        return u

    @staticmethod
    def get_admin_user_requried(request: Request, response: Response) -> UserInfo:
        u = AuthUtil.get_current_user_required(request, response)
        if not isinstance(u.extended, AdminInfo):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not of type admin",
            )
        return u

    @staticmethod
    def get_donor_user_requried(request: Request, response: Response) -> UserInfo:
        u = AuthUtil.get_current_user_required(request, response)
        if not isinstance(u.extended, DonorInfo):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not of type donor",
            )
        return u

    @staticmethod
    def get_auth_util(request: Request) -> AuthUtil:
        return request.app.state.auth_utils


AuthUtilDependency = Annotated[AuthUtil, Depends(AuthUtil.get_auth_util)]
CurrentUserOptional = Annotated[
    UserInfo | None, Depends(AuthUtil.get_current_user_optional)
]
CurrentUserRequired = Annotated[UserInfo, Depends(AuthUtil.get_current_user_required)]
AdminUserRequired = Annotated[UserInfo, Depends(AuthUtil.get_admin_user_requried)]
DonorUserRequired = Annotated[UserInfo, Depends(AuthUtil.get_donor_user_requried)]
