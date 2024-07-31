import jwt
import pytest
from pydantic import ValidationError, SecretStr
from fastapi import FastAPI, HTTPException
from httpx import AsyncClient
from typing import Union, Optional

from app.models.users import UserInDB
from app.services.authentication import AuthService
from app.core.config import SECRET_KEY, JWT_AUDIENCE, ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM


class TestAuthTokens:
    @pytest.mark.asyncio
    async def test_can_create_access_token_successfully(
            self,
            app: FastAPI,
            client: AsyncClient,
            test_user: UserInDB
    ) -> None:
        access_token = AuthService.create_access_token_for_user(
            user=test_user,
            secret_key=str(SECRET_KEY),
            audience=JWT_AUDIENCE,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        creds = jwt.decode(
            access_token,
            key=str(SECRET_KEY),
            audience=JWT_AUDIENCE,
            algorithms=[JWT_ALGORITHM]
        )
        assert creds.get("username") is not None
        assert creds.get("username") == test_user.username
        assert creds.get("aud") == JWT_AUDIENCE

    @pytest.mark.asyncio
    async def test_token_missing_user_is_invalid(
            self,
            app: FastAPI,
            client: AsyncClient,
    ) -> None:
        access_token = AuthService.create_access_token_for_user(
            user=None,
            secret_key=SECRET_KEY,
            audience=JWT_AUDIENCE,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        with pytest.raises(jwt.PyJWTError):
            jwt.decode(access_token, str(SECRET_KEY), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM])

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "secret, jwt_audience, exception",
        [
            ("wrong-secret", JWT_AUDIENCE, TypeError),
            (None, JWT_AUDIENCE, TypeError),
            (SECRET_KEY, "othersite:auth", TypeError),
            (SECRET_KEY, None, ValidationError)
        ]
    )
    async def test_invalid_token_content_raises_error(
            self,
            app: FastAPI,
            client: AsyncClient,
            test_user: UserInDB,
            secret: str,
            jwt_audience: str,
            exception: BaseException
    ) -> None:
        with pytest.raises(exception):
            access_token = AuthService.create_access_token_for_user(
                user=test_user,
                secret_key=SECRET_KEY,
                audience=jwt_audience,
                expires_in=ACCESS_TOKEN_EXPIRE_MINUTES
            )
            jwt.decode(
                access_token,
                str(SECRET_KEY),
                audience=JWT_AUDIENCE,
                algorithms=[JWT_ALGORITHM]
            )

    @pytest.mark.asyncio
    async def test_can_retrieve_username_from_token(
            self,
            app: FastAPI,
            client: AsyncClient,
            test_user: UserInDB
    ) -> None:
        token = AuthService.create_access_token_for_user(user=test_user, secret_key=str(SECRET_KEY))
        username = AuthService.get_username_from_token(token=token, secret_key=str(SECRET_KEY))
        assert username == test_user.username

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "secret, wrong_token",
        [
            (SECRET_KEY, "asdf"),
            (SECRET_KEY, ""),
            (SECRET_KEY, None),
            ("ABC123", "use correct token"),
        ]
    )
    async def test_error_when_token_or_secret_is_wrong(
            self,
            app: FastAPI,
            client: AsyncClient,
            test_user: UserInDB,
            secret: Union[SecretStr, str],
            wrong_token: Optional[str],
    ) -> None:
        token = AuthService.create_access_token_for_user(user=test_user, secret_key=str(SECRET_KEY))

        if wrong_token == "use correct token":
            wrong_token = token
        with pytest.raises(HTTPException):
            username = AuthService.get_username_from_token(token=wrong_token, secret_key=secret)
