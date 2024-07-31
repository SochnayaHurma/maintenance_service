import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient
from databases import Database

from app.db.repositories.profiles import ProfilesRepository
from app.models.profile import ProfileInDB
from app.models.users import UserInDB, UserPublic


class TestProfileCreate:
    """Содержит тесты проверяющие создание профиля во время регистрации"""

    @pytest.mark.asyncio
    async def test_profile_created_for_new_users(
            self,
            app: FastAPI,
            client: AsyncClient,
            db: Database
    ) -> None:
        profiles_repo = ProfilesRepository(db)
        new_user = {"email": "blabla@gmail.com", "username": "blablaprof", "password": "blabla223"}
        response = await client.post(
            app.url_path_for("users:register-new-user"),
            json={"new_user": new_user}
        )
        assert response.status_code == status.HTTP_201_CREATED, "Неверный статус ответа при регистрации профиля"

        created_user = UserPublic(**response.json())
        user_profile = await profiles_repo.get_profile_by_user_id(user_id=created_user.id)
        assert user_profile is not None
        assert isinstance(user_profile, ProfileInDB)
