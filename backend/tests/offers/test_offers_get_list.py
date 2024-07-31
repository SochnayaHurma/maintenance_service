import pytest
from fastapi import FastAPI, status
from databases import Database
from typing import Callable, List, Dict, Tuple
from httpx import AsyncClient
import pytest_asyncio

from app.db.repositories.offers import OffersRepository
from app.db.repositories.cleanings import CleaningRepository, CleaningCreate
from app.models.core import IDModelMixin
from app.models.users import UserInDB
from app.models.cleaning import CleaningInDB
from app.models.offer import CleaningOffersListPublic, OfferInDB
from tests.error_message_enum import ErrorMessages


@pytest_asyncio.fixture
async def test_cleanings_list(db: Database, test_user2: UserInDB) -> List[CleaningInDB]:
    cleaning_repo = CleaningRepository(db)
    return [
        await cleaning_repo.create_cleaning(
            new_cleaning=CleaningCreate(name=f"cleaning-{num}", desc=f"test desc-{num}",
                                        price=20.00, cleaning_type="full_clean"),
            current_user=test_user2
        ) for num in range(5)
    ]


class TestPopulatedOfferList:
    """
    Набор тестов: Проверяющих контроллер выдачи списка заказов на указанную услугу
    """

    @pytest.mark.asyncio
    async def test_user_owned_cleanings_are_populated__with_correct_offers(
            self,
            app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user: UserInDB,
            test_list_of_cleanings_with_pending_offers: Dict[int, Tuple[CleaningInDB, List[OfferInDB]]],
            get_all_detail_cleanings_from_user: Callable[[UserInDB, bool], CleaningOffersListPublic]
    ) -> None:
        """
        Тест: при GET запросе владельцем услуги ожидаем корректный вывод услуги и
        связанных с ней заказов
        !!!
        """
        expected_cleanings = await get_all_detail_cleanings_from_user(test_user, True)
        expected_cleaning_to_dict = {
            cleaning.cleaning.id: cleaning.dict()
            for cleaning in expected_cleanings
        }
        print(expected_cleaning_to_dict)
        authorized_client = create_authorized_client(user=test_user)

        response = await authorized_client.get(
            app.url_path_for("cleanings:get-all-user-cleanings")
        )
        assert response.status_code == status.HTTP_200_OK, ErrorMessages.WRONG_STATUS_CODE.value

        cleanings = [CleaningOffersListPublic(**cleaning) for cleaning in response.json()]
        for cleaning in cleanings:
            current_expected_cleaning = expected_cleaning_to_dict[cleaning.cleaning.id]
            assert cleaning == current_expected_cleaning
            assert cleaning.offers == current_expected_cleaning['offers']
            assert cleaning.total_offers == len(current_expected_cleaning['offers'])

    @pytest.mark.asyncio
    async def test_public_cleaning_jobs_list_number_of_total_offers(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user2: UserInDB,
            test_list_of_cleanings_with_pending_offers: Tuple[List[CleaningInDB], Dict[int, Dict[int, OfferInDB]]],
            test_user_list: List[UserInDB]
    ) -> None:
        authorized_client = create_authorized_client(user=test_user2)
        for clean_id, clean_detail in test_list_of_cleanings_with_pending_offers.items():
            response = await authorized_client.get(
                app.url_path_for("cleanings:get-cleaning-by-id", cleaning_id=clean_id)
            )
            assert response.status_code == status.HTTP_200_OK, ErrorMessages.WRONG_STATUS_CODE.value
            cleaning = CleaningOffersListPublic(**response.json())
            assert cleaning.total_offers == len(cleaning.offers)
        #     assert cleaning.offers == []

