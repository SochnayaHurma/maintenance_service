import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from app.models.users import UserInDB
from app.models.profile import ProfilePublic


class TestProfilesView:
    """Набор тестов с проверками представления профиля"""
    @pytest.mark.asyncio
    async def test_authenticated_user_can_view_other_users_profile(
            self, app: FastAPI,
            authorized_client: AsyncClient,
            test_user: UserInDB, test_user2: UserInDB,
    ) -> None:
        response = await authorized_client.get(
            app.url_path_for("profiles:get-profile-by-username", username=test_user2.username)
        )
        assert response.status_code == status.HTTP_200_OK, "Некорректный адрес при запросе зарегистрированного профиля"
        profile = ProfilePublic(**response.json())
        assert profile.username == test_user2.username

    @pytest.mark.asyncio
    async def test_unregistered_users_cannot_access_other_user_profile(
            self,
            app: FastAPI,
            client: AsyncClient,
            test_user: UserInDB,
    ) -> None:
        response = await client.get(
            app.url_path_for("profiles:get-profile-by-username", username=test_user.username)
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, \
            "Некорректный статус в проверке на доступ неавторизованнго пользователя"

    @pytest.mark.asyncio
    async def test_no_profile_is_returned_when_username_matches_no_user(
            self, app: FastAPI,
            authorized_client: AsyncClient,
    ) -> None:
        response = await authorized_client.get(app.url_path_for("profiles:get-profile-by-username", username="usernamedoesntmatch"))
        assert response.status_code == status.HTTP_404_NOT_FOUND, \
            "Некорректный статус при попытке найти несуществующего пользователя"
