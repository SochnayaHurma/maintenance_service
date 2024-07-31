from fastapi import FastAPI, status
from httpx import AsyncClient
import pytest

from app.models.users import UserInDB


class TestProfilesRoutes:
    """
    Содержит тесты эндпойнта profile
    """

    @pytest.mark.asyncio
    async def test_route_get_profile_exist(
            self,
            app: FastAPI,
            client: AsyncClient,
            test_user: UserInDB
    ) -> None:
        response = await client.get(app.url_path_for("profiles:get-profile-by-username", username=test_user.username))
        assert response.status_code != status.HTTP_404_NOT_FOUND, "Маршрут get-profile не найден"

    @pytest.mark.asyncio
    async def test_route_update_profile_exist(
            self,
            app: FastAPI,
            authorized_client: AsyncClient,
            test_user: UserInDB
    ) -> None:
        response = await authorized_client.put(app.url_path_for("profiles:update-own-profile"))
        assert response.status_code != status.HTTP_404_NOT_FOUND, "Маршрут update-profile не найден"

