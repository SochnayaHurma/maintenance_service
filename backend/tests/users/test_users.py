from fastapi import status, FastAPI
import pytest
from httpx import AsyncClient
from databases import Database

from app.db.repositories.users import UsersRepository
from app.models.users import UserInDB, UserPublic
from app.services.authentication import AuthService


class TestUserRoutes:
    @pytest.mark.asyncio
    async def test_routes_exist(
            self,
            app: FastAPI,
            client: AsyncClient
    ) -> None:
        new_user = {
            "email": "test@email.io",
            "username": "test_username",
            "password": "testpassword",
        }
        response = await client.post(
            app.url_path_for("users:register-new-user"),
            json={"new_user": new_user}
        )
        assert response.status_code != status.HTTP_404_NOT_FOUND


class TestUserRegister:

    @pytest.mark.asyncio
    async def test_users_can_register_successfully(
            self,
            app: FastAPI,
            client: AsyncClient,
            db: Database
    ) -> None:
        user_repo = UsersRepository(db)
        new_user = {
            "email": "testqqw@email.io",
            "username": "test2_username",
            "password": "testpassword",
        }

        # проверяем что пользователь с таким эмайлом не существует
        user_in_db = await user_repo.get_user_by_email(email=new_user['email'], populate=False)
        assert user_in_db is None

        # делаем пост запрос на регистрацию пользователя
        response = await client.post(
            app.url_path_for("users:register-new-user"),
            json={"new_user": new_user}
        )
        assert response.status_code == status.HTTP_201_CREATED

        # Проверяем что после пост запрос на регистрацию в базе данных появился наш пользователь
        user_in_db = await user_repo.get_user_by_email(email=new_user['email'], populate=False)
        assert user_in_db is not None
        assert user_in_db.email == new_user['email']
        assert user_in_db.username == new_user['username']

        ## валидируем поля ответа и сравниваем вывод ответа с выводом из базы данных исключив пароль
        created_user = UserPublic(**response.json()).dict(exclude={"access_token", "profile"})
        assert created_user == user_in_db.dict(exclude={"password", "salt"})

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "attr, value, status_code",
        [
            ("email", "tadjik@mail.hu", 400),
            ("username", "prost", 400),
            ("email", "ploxoyemail.ru", 422),
            ("password", "short", 422),
            ("username", "asdasww$$@##", 422),
            ("username", "tw", 422)
        ]
    )
    async def test_user_registration_fails_when_credentials_are_taken(
            self,
            app: FastAPI,
            client: AsyncClient,
            db: Database,
            attr: str,
            value: str,
            status_code: int,
    ) -> None:
        new_user = {
            "email": "test@email.io",
            "username": "test_username",
            "password": "testpassword",
            attr: value
        }
        response = await client.post(
            app.url_path_for("users:register-new-user"),
            json={"new_user": new_user}
        )
        assert response.status_code == status_code

    @pytest.mark.asyncio
    async def test_users_saved_password_is_hashed_and_has_salt(
            self,
            app: FastAPI,
            client: AsyncClient,
            db: Database
    ):
        user_repo = UsersRepository(db)
        new_user = {"email": "gogago@qwe.com", "username": "qfffrew_w", "password": "destqew"}
        response = await client.post(
            app.url_path_for("users:register-new-user"),
            json={"new_user": new_user}
        )
        assert response.status_code == status.HTTP_201_CREATED

        user_in_db = await user_repo.get_user_by_email(email=new_user["email"], populate=False)
        assert user_in_db is not None
        assert user_in_db.salt is not None
        assert user_in_db.password != new_user["password"]
        assert AuthService.verify_password(
            password=new_user["password"],
            salt=user_in_db.salt,
            hashed_pw=user_in_db.password
        )
