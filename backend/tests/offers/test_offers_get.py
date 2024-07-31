import random
from typing import List, Callable
import pytest
from httpx import AsyncClient
from fastapi import FastAPI, status

from app.models.cleaning import CleaningInDB
from app.models.offer import OfferPublic
from app.models.users import UserInDB


class TestGetOffers:
    """Класс содержит набор тестов проверяющих маршрут(GET) на получение заказа по username"""

    @pytest.mark.asyncio
    async def test_cleaning_owner_can_get_offer_from_user(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user2: UserInDB,
            test_user_list: List[UserInDB],
            test_cleaning_with_offers: CleaningInDB,
    ) -> None:
        """
        Тест проверяет что создавший услугу(Cleaning)
        может просматривать заказчиков(Offers.user_id) на неё
        """
        authorized_client = create_authorized_client(test_user2)
        selected_user = random.choice(test_user_list)
        response = await authorized_client.get(
            app.url_path_for(
                "offers:get-offer-from-user",
                cleaning_id=test_cleaning_with_offers.id,
                username=selected_user.username
            )
        )
        assert response.status_code == status.HTTP_200_OK, response.json()
        offer = OfferPublic(**response.json())
        assert offer.user_id == selected_user.id

    @pytest.mark.asyncio
    async def test_offer_owner_can_get_own_offer(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_cleaning_with_offers: CleaningInDB,
            test_user_list: List[UserInDB],
    ) -> None:
        """Тест проверяет что заказчик(Offers.user_id) может получить доступ к своему заказау"""
        first_test_user = test_user_list[0]
        authorized_client = create_authorized_client(user=first_test_user)
        response = await authorized_client.get(
            app.url_path_for(
                "offers:get-offer-from-user",
                cleaning_id=test_cleaning_with_offers.id,
                username=first_test_user.username,
            )
        )
        assert response.status_code == status.HTTP_200_OK
        offer = OfferPublic(**response.json())
        assert offer.user_id == first_test_user.id

    @pytest.mark.asyncio
    async def test_other_authenticated_users_cant_view_offer_from_user(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user_list: List[UserInDB],
            test_cleaning_with_offers: CleaningInDB,
    ) -> None:
        """Тест проверяет что пользователь не имеющий отношения к сделке получит ответ 403 Frobidden"""
        first_user = test_user_list[0]
        second_user = test_user_list[1]
        authorization_client = create_authorized_client(user=first_user)
        response = await authorization_client.get(
            app.url_path_for(
                "offers:get-offer-from-user",
                cleaning_id=test_cleaning_with_offers.id,
                username=second_user.username,
            )
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_cleaning_owner_can_get_all_offers_for_cleanings(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user2: UserInDB,
            test_user_list: List[UserInDB],
            test_cleaning_with_offers: CleaningInDB,
    ) -> None:
        """Тест проверяет что создатель услуги может получить список заказов на неё"""
        authorization_client = create_authorized_client(user=test_user2)
        response = await authorization_client.get(
            app.url_path_for("offers:list-offers-for-cleaning", cleaning_id=test_cleaning_with_offers.id)
        )
        assert response.status_code == status.HTTP_200_OK
        for offer in response.json()['offers']:
            assert offer["executor"]['id'] in [user.id for user in test_user_list]

    @pytest.mark.asyncio
    async def test_non_owners_forbidden_from_fetching_all_offers_for_cleaning(
            self, app: FastAPI,
            authorized_client: AsyncClient,
            test_cleaning_with_offers: CleaningInDB,
    ) -> None:
        """Тест проверяет что пользователь не являющийся создателем услуги не может получить к ней доступ"""
        response = await authorized_client.get(
            app.url_path_for("offers:list-offers-for-cleaning", cleaning_id=test_cleaning_with_offers.id)
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
