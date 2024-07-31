import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi import FastAPI, status
from databases import Database

from typing import Dict, Optional, List, Union

from app.models.cleaning import CleaningCreate, CleaningInDB, CleaningPublic
from app.models.offer import CleaningOffersListPublic
from app.models.users import UserInDB
from app.db.repositories.cleanings import CleaningRepository


@pytest.fixture
def new_cleaning() -> CleaningCreate:
    return CleaningCreate(
        name="test cleaning",
        description="test description",
        price=0.00,
        cleaning_type="spot_clean"
    )


@pytest_asyncio.fixture
async def test_cleanings_list(db: Database, test_user2: UserInDB) -> List[CleaningPublic]:
    cleaning_repo = CleaningRepository(db)
    return [
        await cleaning_repo.create_cleaning(
            new_cleaning=CleaningCreate(name=f"cleaning-{num}", desc=f"test desc-{num}",
                                        price=20.00, cleaning_type="full_clean"),
            current_user=test_user2
        ) for num in range(5)
    ]


class TestCleaningsRoutes:
    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        """
        Тест: проверяет на корректность выдачи маршрута по функции представления
        """
        response_get_all = await client.get(app.url_path_for("cleanings:get-all-user-cleanings"))
        assert response_get_all.status_code != status.HTTP_404_NOT_FOUND, "Не найден маршрут list-all-user-cleanings"
        response_get_one = await client.get(app.url_path_for("cleanings:get-cleaning-by-id", cleaning_id=1))
        assert response_get_one.status_code != status.HTTP_404_NOT_FOUND, "не найден маршрут get-cleaning-by-id"
        response_post = await client.post(app.url_path_for("cleanings:create-cleaning"), json={})
        assert response_post.status_code != status.HTTP_404_NOT_FOUND, "Не найден маршрут create-cleaning"
        response_put = await client.put(app.url_path_for("cleanings:update-cleaning-by-id", cleaning_id=1))
        assert response_put.status_code != status.HTTP_404_NOT_FOUND, "Не найден маршрут update-cleaning-by-id"
        response_delete = await client.delete(app.url_path_for("cleanings:delete-cleaning-by-id", cleaning_id=1))
        assert response_delete.status_code != status.HTTP_404_NOT_FOUND, "Не найден маршрут delete-cleaning-by-id"

    @pytest.mark.asyncio
    async def test_invalid_input_raises_error(self, app: FastAPI, authorized_client: AsyncClient) -> None:
        """
        Тест: проверяет реакцию на отправленое пустое тело в пост запросе
        """
        response = await authorized_client.post(app.url_path_for("cleanings:create-cleaning"), json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestCreateCleaning:
    """Набор тестов представления создания услуги"""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "invalid_payload, status_code",
        (
                (None, 422),
                ({}, 422),
                ({"name": "test_name"}, 422),
                ({"price": 10.00}, 422),
                ({"name": "test_name", "description": "test"}, 422),
        )
    )
    async def test_invalid_input_raises_error(
            self,
            app: FastAPI,
            authorized_client: AsyncClient,
            invalid_payload: Optional[Dict[str, Union[str, float]]],
            status_code: int
    ) -> None:
        response = await authorized_client.post(
            url=app.url_path_for("cleanings:create-cleaning"),
            json={"new_cleaning": invalid_payload}
        )
        assert response.status_code == status_code, "Неожидаемый статус код %s".format(
            response.status_code
        )

    @pytest.mark.asyncio
    async def test_valid_input_creates_cleaning_belonging_to_user(
            self,
            app: FastAPI,
            authorized_client: AsyncClient,
            test_user: UserInDB,
            new_cleaning: CleaningCreate,
    ) -> None:
        """Проверка на наличие обязательных полей у вернувшейся после создания услуги"""
        response = await authorized_client.post(
            app.url_path_for("cleanings:create-cleaning"),
            json={"new_cleaning": new_cleaning.dict()},
        )
        assert response.status_code == status.HTTP_201_CREATED
        created_cleaning = CleaningPublic(**response.json())
        assert created_cleaning.name == new_cleaning.name
        assert created_cleaning.price == new_cleaning.price
        assert created_cleaning.cleaning_type == new_cleaning.cleaning_type
        assert created_cleaning.owner == test_user.id

    @pytest.mark.asyncio
    async def test_unauthorized_user_unable_to_create_cleaning(
            self,
            app: FastAPI,
            client: AsyncClient,
            new_cleaning: CleaningCreate
    ) -> None:
        """Проверяет отсутсвие доступа неавторизованного пользователя к созданию услуги"""
        response = await client.post(
            app.url_path_for("cleanings:create-cleaning"),
            json={"new_cleaning": new_cleaning.dict()}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, \
            "Получен некорректный код при попытки создания записи неавторизованным пользователем"


class TestGetCleaning:
    @pytest.mark.asyncio
    async def test_get_cleaning_by_id(
            self,
            app: FastAPI,
            authorized_client: AsyncClient,
            test_cleaning: CleaningInDB
    ) -> None:
        response = await authorized_client.get(app.url_path_for("cleanings:get-cleaning-by-id", cleaning_id=test_cleaning.id))
        assert response.status_code == status.HTTP_200_OK
        validate_body_response = CleaningOffersListPublic(**response.json())
        assert validate_body_response.cleaning.id == test_cleaning.id
        assert validate_body_response.cleaning.name == test_cleaning.name
        assert validate_body_response.cleaning.description == test_cleaning.description
        assert validate_body_response.cleaning.price == test_cleaning.price
        assert validate_body_response.cleaning.cleaning_type == test_cleaning.cleaning_type

    @pytest.mark.asyncio
    async def test_unauthorized_users_cant_access_cleanings(
            self,
            app: FastAPI,
            client: AsyncClient,
            test_cleaning: CleaningInDB
    ) -> None:
        response = await client.get(app.url_path_for("cleanings:get-cleaning-by-id", cleaning_id=test_cleaning.id))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "cleaning_id, status_code",
        (
                (500, 404),
                (-1, 422),
                (None, 422)
        )
    )
    async def test_wrong_id_returns_error(
            self,
            app: FastAPI,
            authorized_client: AsyncClient,
            cleaning_id: Optional[int],
            status_code: int
    ):
        response = await authorized_client.get(
            url=app.url_path_for("cleanings:get-cleaning-by-id", cleaning_id=cleaning_id)
        )
        assert response.status_code == status_code

    @pytest.mark.asyncio
    async def test_get_all_cleanings_returns_only_user_owned_cleanings(
            self,
            app: FastAPI,
            # authorized_client: AsyncClient,
            create_authorized_client,

        test_user2: UserInDB,
            db: Database,
            test_cleaning: CleaningInDB,
            test_cleanings_list: List[CleaningInDB],
    ) -> None:
        authorized_client = create_authorized_client(test_user2)
        response = await authorized_client.get(app.url_path_for("cleanings:get-all-user-cleanings"))
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0

        cleanings = [CleaningOffersListPublic(**cleaning) for cleaning in response.json()]
        {cleaning.cleaning.id for cleaning in cleanings} == {cleaning.id for cleaning in test_cleanings_list}
        for clean in cleanings:
            assert clean.cleaning.owner.id == test_user2.id


class TestUpdateCleaning:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "attrs_to_change, values",
        [
            (["name"], ["new fake cleaning name"]),
            (["description"], ["new fake cleaning description"]),
            (["price"], [3.14]),
            (["cleaning_type"], ["full_clean"]),
            (["price", "cleaning_type"], [42.00, "dust_up"]),
            (
                ["name", "description"],
                [
                    "extra new fake cleaning name",
                    "extra new fake cleaning desc"
                ]
            ),

        ]
    )
    async def test_update_cleaning_with_valid_input(
            self,
            app: FastAPI,
            authorized_client: AsyncClient,
            test_cleaning: CleaningInDB,
            attrs_to_change: list,
            values: list
    ) -> None:
        count_attr_to_change = range(len(attrs_to_change))
        cleaning_update = {
            "cleaning_update": {
                attrs_to_change[i]: values[i] for i in count_attr_to_change
            }
        }
        response = await authorized_client.put(
            app.url_path_for("cleanings:update-cleaning-by-id", cleaning_id=test_cleaning.id),
            json=cleaning_update
        )
        assert response.status_code == status.HTTP_200_OK
        updated_cleaning = CleaningPublic(**response.json())
        assert updated_cleaning.id == test_cleaning.id
        for i in count_attr_to_change:
            attr_to_change = getattr(updated_cleaning, attrs_to_change[i])
            assert attr_to_change != getattr(test_cleaning, attrs_to_change[i])
            assert attr_to_change == values[i]
        for attr, value in updated_cleaning.dict().items():
            if attr not in attrs_to_change and attr != "updated_at":
                assert getattr(test_cleaning, attr) == value

    @pytest.mark.asyncio
    async def test_user_receives_error_if_updating_other_users_cleaning(
            self,
            app: FastAPI,
            authorized_client: AsyncClient,
            test_cleanings_list: List[CleaningPublic],
    ) -> None:
        response = await authorized_client.put(
            app.url_path_for("cleanings:update-cleaning-by-id", cleaning_id=test_cleanings_list[0].id),
            json={"cleaning_update": {"price": 99.00}}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN, \
            "Некорректный статус код при попытки изменения услуги пользователем не имеющим к ней отношения"

    @pytest.mark.asyncio
    async def test_user_cant_change_ownership_of_cleaning(
            self,
            app: FastAPI,
            authorized_client: AsyncClient,
            test_cleaning: CleaningInDB,
            test_user: UserInDB,
            test_user2: UserInDB
    ) -> None:
        response = await authorized_client.put(
            app.url_path_for("cleanings:update-cleaning-by-id", cleaning_id=test_cleaning.id),
            json={"cleaning_update": {"owner": test_user2.id}}
        )
        assert response.status_code == status.HTTP_200_OK
        cleaning = CleaningPublic(**response.json())
        assert cleaning.owner == test_user.id

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "cleaning_id, payload, status_code",
        [
            (-1, {"name": "test"}, 422),
            (0, {"name": "test2"}, 422),
            (500, {"name": "test3"}, 404),
            (1, None, 422),
            (1, {"cleaning_type": "invalid_cleaning_type"}, 422),
            (1, {"cleaning_type": None}, 400)
        ]
    )
    async def test_update_cleaning_with_invalid_input_throws_error(
            self,
            app: FastAPI,
            authorized_client: AsyncClient,
            cleaning_id: int,
            payload: dict,
            status_code: int
    ) -> None:
        cleaning_update = {"cleaning_update": payload}
        response = await authorized_client.put(
            app.url_path_for("cleanings:update-cleaning-by-id", cleaning_id=cleaning_id),
            json=cleaning_update
        )
        assert response.status_code == status_code, \
            "Неожидаемый статус код ожидался %s :: получили %s".format(response.status_code, status_code)


class TestDeleteCleaning:
    @pytest.mark.asyncio
    async def test_can_delete_cleaning_successfully(
            self,
            app: FastAPI,
            authorized_client: AsyncClient,
            test_cleaning: CleaningInDB
    ) -> None:
        response_delete = await authorized_client.delete(
            app.url_path_for("cleanings:delete-cleaning-by-id", cleaning_id=test_cleaning.id),
        )
        assert response_delete.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.asyncio
    async def test_user_cant_delete_other_users_cleaning(
            self,
            app: FastAPI,
            authorized_client: AsyncClient,
            test_cleanings_list: List[CleaningInDB]
    ) -> None:
        """Тест: пользователь при попытке удалить чужую запись получает статус 403"""
        response = await authorized_client.delete(
            app.url_path_for("cleanings:delete-cleaning-by-id", cleaning_id=test_cleanings_list[0].id)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "cleaning_id, status_code",
        [
            (500, 404),
            (0, 422),
            (-1, 422),
            (None, 422)
        ]
    )
    async def test_delete_cleaning_with_invalid_input_throws_error(
            self,
            app: FastAPI,
            authorized_client: AsyncClient,
            test_cleaning: CleaningInDB,
            cleaning_id: int,
            status_code: int
    ) -> None:
        response = await authorized_client.delete(
            app.url_path_for("cleanings:delete-cleaning-by-id", cleaning_id=cleaning_id)
        )
        assert response.status_code == status_code
