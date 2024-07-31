import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient
from typing import Callable, Optional

from app.models.users import UserInDB
from app.models.cleaning import CleaningInDB
from app.models.offer import OfferStatus, OfferPublic


class TestCreateOffers:
    """Набор тестов проверяющих маршрут по созданию заказа"""
    OFFER_CREATE_ROUTE = "offers:create-offer"

    @pytest.mark.asyncio
    async def test_user_can_successfully_create_offer_for_other_users_cleaning_job(
            self,
            app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user3: UserInDB,
            test_cleaning: CleaningInDB
    ) -> None:
        """Тест проверяет корректность выходных данных после создания заказа """
        authorized_client = create_authorized_client(user=test_user3)
        response = await authorized_client.post(
            app.url_path_for("offers:create-offer", cleaning_id=test_cleaning.id),
        )
        assert response.status_code == status.HTTP_201_CREATED, "Статус при создании заказа некорректный"
        offer = OfferPublic(**response.json())
        assert offer.user_id == test_user3.id
        assert offer.cleaning_id == test_cleaning.id
        assert offer.status == OfferStatus.pending

    @pytest.mark.asyncio
    async def test_user_cant_create_duplicate_offers(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user4: UserInDB,
            test_cleaning: CleaningInDB
    ) -> None:
        """Тест проверяет что пользователь не может дважды брать заказ на одну и ту же услугу"""
        authorized_client = create_authorized_client(user=test_user4)
        response_one = await authorized_client.post(
            app.url_path_for("offers:create-offer", cleaning_id=test_cleaning.id)
        )
        assert response_one.status_code == status.HTTP_201_CREATED
        response_second = await authorized_client.post(
            app.url_path_for("offers:create-offer", cleaning_id=test_cleaning.id)
        )
        assert response_second.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_user_unable_to_create_offer_for_their_own_cleaning_job(
            self, app: FastAPI,
            authorized_client: AsyncClient,
            test_cleaning: CleaningInDB
    ) -> None:
        """Тест проверяет что владелец услуги не может брать на неё заказ"""
        response = await authorized_client.post(
            app.url_path_for("offers:create-offer", cleaning_id=test_cleaning.id)
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_unauthenticated_users_cant_create_offers(
           self, app: FastAPI,
            client: AsyncClient,
            test_cleaning: CleaningInDB
    ) -> None:
        response = await client.post(app.url_path_for("offers:create-offer", cleaning_id=test_cleaning.id))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "cleaning_id, status_code",
        [
            (5000000, 404),
            (-1, 422),
            (None, 422),
        ]
    )
    async def test_wrong_id_gives_proper_error_status(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user5: UserInDB,
            test_cleaning: CleaningInDB,
            cleaning_id: Optional[int],
            status_code: int,
    ) -> None:
        authorized_client = create_authorized_client(user=test_user5)
        response = await authorized_client.post(
            app.url_path_for("offers:create-offer", cleaning_id=cleaning_id)
        )
        assert response.status_code == status_code
