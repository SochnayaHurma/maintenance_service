import jwt
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from app.models.users import UserInDB
from app.core.config import SECRET_KEY, JWT_ALGORITHM, JWT_TOKEN_PREFIX, JWT_AUDIENCE


class TestUserLogin:
    @pytest.mark.asyncio
    async def test_user_can_login_successfully_and_receives_valid_token(
            self,
            app: FastAPI,
            client: AsyncClient,
            test_user: UserInDB
    ) -> None:
        client.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        login_data = {
            'username': test_user.email,
            'password': 'heatcavs'
        }
        response = await client.post(
            app.url_path_for('users:login-email-and-password'),
            data=login_data
        )
        assert response.status_code == status.HTTP_200_OK

        token = response.json().get('access_token')
        creds = jwt.decode(token, key=str(SECRET_KEY), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM])
        assert "username" in creds
        assert creds.get("username") == test_user.username
        assert "sub" in creds
        assert creds.get("sub") == test_user.email
        assert "token_type" in response.json()
        assert response.json().get('token_type') == JWT_TOKEN_PREFIX

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'credential, wrong_value, status_code',
        [
            ("email", "wrong@email.com", 401),
            ("email", None, 401),
            ("email", "notemail", 401),
            ("password", "wrongpassword", 401),
            ("password", None, 422)
        ],
    )
    async def test_user_with_wrong_creds_doesnt_receive_token(
            self,
            app: FastAPI,
            client: AsyncClient,
            test_user: UserInDB,
            credential: str,
            wrong_value: str,
            status_code: int,
    ) -> None:
        client.headers['content-type'] = 'application/x-www-form-urlencoded'
        login_data = {
            'username': test_user.email,
            'password': "heatcavsqq",
            credential: wrong_value
        }
        response = await client.post(
            app.url_path_for("users:login-email-and-password"),
            data=login_data
        )
        assert response.status_code == status_code
        assert "access_token" not in response.json()
