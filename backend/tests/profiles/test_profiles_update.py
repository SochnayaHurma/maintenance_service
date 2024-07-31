import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from app.models.users import UserInDB
from app.models.profile import ProfilePublic

class TestProfileManagement:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "attrs, value",
        [
            ("full_name", "Broun Black"),
            ("phone_number", "555-333-1000"),
            ("bio", "This is a test bio"),
            ("image", "http://qweqwe.com/hashhash.jpg")
        ]
    )
    async def test_user_can_update_own_profile(
            self,
            app: FastAPI,
            authorized_client: AsyncClient,
            test_user: UserInDB,
            attrs: str,
            value: str
    ) -> None:
        assert getattr(test_user.profile, attrs) != value
        response = await authorized_client.put(
            app.url_path_for("profiles:update-own-profile"),
            json={"profile_update": {attrs: value}}
        )
        assert response.status_code == status.HTTP_200_OK, "Некорректный статус вывода после обновления профиля"
        profile = ProfilePublic(**response.json())
        assert getattr(profile, attrs) == value

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "attrs, value, status_code",
        [
            ("full_name", [], 422),
            ("bio", {}, 422),
            ("image", "./image-string.png", 422),
            ("image", 5, 422),
        ]
    )
    async def test_user_recieves_error_for_invalid_update_params(
            self,
            app: FastAPI,
            authorized_client: AsyncClient,
            test_user: UserInDB,
            attrs: str,
            value: str,
            status_code: int
    ) -> None:
        response = await authorized_client.put(
            app.url_path_for("profiles:update-own-profile"),
            json={"profile_update": {attrs: value}}
        )
        assert response.status_code == status_code, \
            "Неожидаемый статус код при обновлении профиля с некорректными данными"
