from typing import Callable, List
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from app.models.cleaning import CleaningInDB
from app.models.users import UserInDB
from app.db.repositories.offers import OffersRepository


class TestOfferDelete:
    """Набор методов проверяющих эндпойнт по удалению заказов"""

    @pytest.mark.asyncio
    async def test_user_can_successfully_rescind_pending_other(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user4: UserInDB,
            test_user_list: List[UserInDB],
            test_cleaning_with_offers: CleaningInDB,
    ) -> None:
        authorized_client = create_authorized_client(user=test_user4)
        response = await authorized_client.delete(
            app.url_path_for("offers:rescind-offer-from-user", cleaning_id=test_cleaning_with_offers.id)
        )
        assert response.status_code == status.HTTP_200_OK, "Некорректный статус при попытки удалить запись за заказчика"

        offer_repo = OffersRepository(app.state._db)
        offers = await offer_repo.list_offers_for_cleaning(cleaning=test_cleaning_with_offers)
        user_ids = [user.id for user in test_user_list]
        for offer in offers:
            assert offer.user_id in user_ids, "При проверке что все остальные заказы остались нетронутыми произошел сбой"
            assert offer.user_id != test_user4, "При проверке списка заказов обнаружен тот, который должен был быть удален"

    @pytest.mark.asyncio
    async def test_users_cannot_rescind_accepted_offers(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user3: UserInDB,
            test_cleaning_with_accepted_offer: CleaningInDB,
    ) -> None:
        authorized_client = create_authorized_client(user=test_user3)
        response = await authorized_client.delete(
            app.url_path_for("offers:rescind-offer-from-user", cleaning_id=test_cleaning_with_accepted_offer.id)
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST, "Некорректный статус код при попытки удалить принятый заказ"

    @pytest.mark.asyncio
    async def test_users_cannot_rescind_cancelled_offers(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user3: UserInDB,
            test_cleaning_with_accepted_offer: CleaningInDB,
    ) -> None:
        authorized_client = create_authorized_client(user=test_user3)
        response_put = await authorized_client.put(
            app.url_path_for("offers:cancel-offer-from-user", cleaning_id=test_cleaning_with_accepted_offer.id)
        )
        assert response_put.status_code == status.HTTP_200_OK, "некорректный статус код при попытки отменить принятый заказ"

        response_delete = await authorized_client.delete(
            app.url_path_for("offers:rescind-offer-from-user", cleaning_id=test_cleaning_with_accepted_offer.id)
        )
        assert response_delete.status_code == status.HTTP_400_BAD_REQUEST, "некорректный статус при попытки удалить отмененный заказ"

    @pytest.mark.asyncio
    async def test_users_cannot_rescind_rejected_offers(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user4: UserInDB,
            test_cleaning_with_accepted_offer: CleaningInDB
    ) -> None:
        authorized_client = create_authorized_client(user=test_user4)
        response = await authorized_client.delete(
            app.url_path_for("offers:rescind-offer-from-user", cleaning_id=test_cleaning_with_accepted_offer.id)
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST, "некорректный статус код при попытки удалить заказ с статусом rejected"