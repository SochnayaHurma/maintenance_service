import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from app.core.config import SECRET_KEY
from app.models.users import UserInDB, UserPublic
from app.services.authentication import AuthService


class TestUserMe:
    @pytest.mark.asyncio
    async def test_authenticated_user_can_retrieve_own_data(
            self,
            app: FastAPI,
            authorized_client: AsyncClient,
            test_user: UserInDB
    ) -> None:
        response = await authorized_client.get(app.url_path_for("users:get-current-user"))
        assert response.status_code == status.HTTP_200_OK
        user_from_response = UserPublic(**response.json())
        assert test_user.username == user_from_response.username, "Получен не ожидаемый username"
        assert test_user.email == user_from_response.email, "Получен не ожидаемый email"
        assert test_user.id == user_from_response.id, "Получен не ожидаемый id"


    @pytest.mark.asyncio
    async def test_user_cannot_access_own_data_if_not_authenticated(
            self,
            app: FastAPI,
            client: AsyncClient,
            test_user: UserInDB
    ) -> None:
        response = await client.get(app.url_path_for("users:get-current-user"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "jwt_prefix",
        [
            ("",), ("value",), ("Token",),
            ("JWT",), ("Swearer",)
        ]
    )
    async def test_user_cannot_access_own_data_with_incorrect_jwt_prefix(
            self,
            app: FastAPI,
            client: AsyncClient,
            test_user: UserInDB,
            jwt_prefix: str
    ) -> None:
        token = AuthService.create_access_token_for_user(user=test_user, secret_key=str(SECRET_KEY))
        response = await client.get(
            app.url_path_for("users:get-current-user"),
            headers={"Authorization": f"{jwt_prefix} {token}"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
