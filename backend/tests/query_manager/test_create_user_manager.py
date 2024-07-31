from typing import Sequence, Dict

import pytest
import pytest_asyncio
from asyncpg.protocol.protocol import Record
from databases import Database
from httpx import AsyncClient

from app.db.repositories.users import UsersRepository
from app.models.users import UserCreate


SELECT_ALL_USERS = "SELECT * FROM %(table)s"


async def select_one(db: Database, table: str) -> Record:
    sql = SELECT_ALL_USERS % {"table": table}
    return await db.execute(sql)


class TestUserCreateManager:
    """
    Набор тестов проверяющих менеджера отвечающего за создание объекта пользователя в базе данных
    """
    @pytest.mark.asyncio
    async def test_user_create_with_expected_credentials(self, client: AsyncClient, db: Database) -> None:
        """
        Тест: Метод register_user создает объект в базе данных с ожидаемыми атрибутами
        """
        data = {
            "email": "q1@mail.ru",
            "password": "qweqweqwe",
            "username": "qqq1"
        }
        user_instance = UserCreate(
            email=data["email"],
            password=data["password"],
            username=data["username"]
        )
        await UsersRepository(db).register_new_user(user_instance)
        q = await select_one(db, "users")
        print(q)


