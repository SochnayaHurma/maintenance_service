import os
import warnings
from typing import Callable, List

import pytest
import pytest_asyncio
from databases import Database
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from app.models.cleaning import CleaningInDB, CleaningCreate
from app.models.users import UserInDB, UserCreate
from app.models.offer import OfferCreate
from app.db.repositories.cleanings import CleaningRepository
from app.db.repositories.offers import OffersRepository
from app.db.repositories.users import UsersRepository
from app.services.authentication import AuthService
from app.core.config import JWT_TOKEN_PREFIX


@pytest.fixture(scope="session")
def apply_migrations():
    """
    Фикстура применяет миграцию на время теста и откатывает после
    """
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")
    command.upgrade(config, "head")
    yield
    command.downgrade(config, "base")


@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    """
    Фикстура создает приложение
    """
    from app.api.server import get_application
    return get_application()


@pytest.fixture
def db(app: FastAPI) -> Database:
    """
    Фикстура возвращает объект интерфейса для подключения к базе данных
    """
    return app.state._db


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncClient:
    """
    Фикстура создает клиента
    """
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={
                "Content-Type": "Application/json"
            }
        ) as client:
            yield client


@pytest_asyncio.fixture
async def test_cleaning(db: Database, test_user: UserInDB) -> CleaningInDB:
    """
    Фикстура создает одну запись услуги отчистки в базе данных
    """
    cleaning_repo = CleaningRepository(db)
    new_cleaning = CleaningCreate(
        name="fake cleaning name",
        description="fake cleaning description",
        price=9.99,
        cleaning_type="spot_clean",
    )
    return await cleaning_repo.create_cleaning(
        new_cleaning=new_cleaning,
        current_user=test_user
    )


async def user_fixture_helper(
        *, db: Database,
        user_instance: UserCreate,
) -> UserInDB:
    """Функция принимает объект модели пользователя и регистрирует её если она отсутствует в БД"""
    user_repo = UsersRepository(db)
    existing_user = await user_repo.get_user_by_email(email=user_instance.email)
    if existing_user:
        return existing_user
    return await user_repo.register_new_user(new_user=user_instance)


@pytest_asyncio.fixture
async def test_user(db: Database) -> UserInDB:
    """
    Фикстура создает одну запись пользователя в базе данных
    """
    return await user_fixture_helper(db=db, user_instance=UserCreate(
        email="blabla@bla.com",
        username="jabjab",
        password="heatcavs"
    ))


@pytest_asyncio.fixture
async def test_user2(db: Database) -> UserInDB:
    """
    Фикстура создает второго пользователя для проверок взаимодействия
    """
    return await user_fixture_helper(db=db, user_instance=UserCreate(
        email="beber223@mail.com",
        username="jwff_abjab2",
        password="heatcavsqq"
    ))


@pytest_asyncio.fixture
async def test_user3(db: Database) -> UserInDB:
    """
    Фикстура создает второго пользователя для проверок взаимодействия
    """
    return await user_fixture_helper(db=db, user_instance=UserCreate(
        email="gosha@gmail.com",
        username="jabfasfasfjab2",
        password="heatcavsqq"
    ))


@pytest_asyncio.fixture
async def test_user4(db: Database) -> UserInDB:
    """
    Фикстура создает второго пользователя для проверок взаимодействия
    """
    return await user_fixture_helper(db=db, user_instance=UserCreate(
        email="bobi@yahoo.com",
        username="bobibobi223",
        password="heatcaqqqw$$vsqq"
    ))


@pytest_asyncio.fixture
async def test_user5(db: Database) -> UserInDB:
    """
    Фикстура создает второго пользователя для проверок взаимодействия
    """
    return await user_fixture_helper(db=db, user_instance=UserCreate(
        email="vasiliy@rambler.ru",
        username="jqqabjabfff",
        password="heatcavsqq"
    ))


@pytest_asyncio.fixture
async def test_user6(db: Database) -> UserInDB:
    """
    Фикстура создает второго пользователя для проверок взаимодействия
    """
    return await user_fixture_helper(db=db, user_instance=UserCreate(
        email="loplop@yandex.ru",
        username="Favic",
        password="heatcff$###avsqq"
    ))


@pytest_asyncio.fixture
async def test_user_list(
        test_user3: UserInDB, test_user4: UserInDB,
        test_user5: UserInDB, test_user6: UserInDB
) -> List[UserInDB]:
    """Фикстура регистрирует и возвращает 4 пользователя"""
    return [test_user3, test_user4, test_user5, test_user6]


@pytest_asyncio.fixture
async def test_cleaning_with_offers(
        db: Database,
        test_user2: UserInDB,
        test_user_list: List[UserInDB],
) -> CleaningInDB:
    """Фикстура принимает одну услугу(Cleaning) и регистрирует на неё 5 заказов(Offers)"""
    new_cleaning = CleaningCreate(name="jobobjob", price=20.00)
    cleaning = await CleaningRepository(db).create_cleaning(new_cleaning=new_cleaning, current_user=test_user2)
    for user in test_user_list:
        await OffersRepository(db).create_offer_for_cleaning(
            new_offer=OfferCreate(user_id=user.id, cleaning_id=cleaning.id)
        )
    return cleaning


@pytest_asyncio.fixture
async def test_cleaning_with_accepted_offer(
        test_user_list: List[UserInDB],
        db: Database,
        test_user2: UserInDB,
        test_user3: UserInDB,
) -> CleaningInDB:
    """
    Фикстура создает и возвращает услугу(Cleaning), на которую
    1. Сделали заказ
    2. Заказ принял владелец услуги
    """
    offers = []
    offer_repo = OffersRepository(db)
    cleaning_repo = CleaningRepository(db)
    new_cleaning = CleaningCreate(
        name="cleaning with offers",
        description="desc from cleaning",
        price=9.99, cleaning_type="full_clean")
    created_cleaning = await cleaning_repo.create_cleaning(new_cleaning=new_cleaning, current_user=test_user2)
    for user in test_user_list:
        current_iter = await offer_repo.create_offer_for_cleaning(
                new_offer=OfferCreate(user_id=user.id, cleaning_id=created_cleaning.id)
            )
        offers.append(current_iter)
    [await offer_repo.accept_offer(offer=offer) for offer in offers if offer.user_id == test_user3.id]

    return created_cleaning


@pytest.fixture
def create_authorized_client(client: AsyncClient) -> Callable:
    def wrap(user: UserInDB) -> AsyncClient:
        token = AuthService.create_access_token_for_user(user=user)
        client.headers = {**client.headers, "Authorization": f"{JWT_TOKEN_PREFIX} {token}"}
        return client
    return wrap


@pytest_asyncio.fixture
async def authorized_client(client: AsyncClient, test_user: UserInDB) -> AsyncClient:
    access_token = AuthService.create_access_token_for_user(user=test_user)
    client.headers["Authorization"] = f"{JWT_TOKEN_PREFIX} {access_token}"
    return client
