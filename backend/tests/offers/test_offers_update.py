import random
from typing import List, Callable
import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from app.models.users import UserInDB
from app.models.cleaning import CleaningInDB
from app.models.offer import OfferStatus, OfferPublic, CleaningOffersListPublic
from app.db.repositories.offers import OffersRepository


class TestAcceptOffer:
    """Набор тестов проверяющих эндпойнт подтверждения заказа"""

    @pytest.mark.asyncio
    async def test_cleaning_owner_can_accept_offer_successfully(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user2: UserInDB,
            test_cleaning_with_offers: CleaningInDB,
            test_user_list: List[UserInDB],
    ) -> None:
        selected_user = random.choice(test_user_list)
        authorized_client = create_authorized_client(user=test_user2)
        response = await authorized_client.put(
            app.url_path_for(
                "offers:accept-offer-from-user",
                cleaning_id=test_cleaning_with_offers.id,
                username=selected_user.username
            )
        )
        assert response.status_code == status.HTTP_200_OK
        updated_offer = OfferPublic(**response.json())
        assert updated_offer.status == OfferStatus.accepted
        assert updated_offer.user_id == selected_user.id
        assert updated_offer.cleaning_id == test_cleaning_with_offers.id

    @pytest.mark.asyncio
    async def test_non_owner_forbidden_from_accepting_offer_for_cleaning(
            self, app: FastAPI,
            authorized_client: AsyncClient,
            test_cleaning_with_offers: CleaningInDB,
            test_user_list: List[UserInDB],
    ) -> None:
        response = await authorized_client.put(
            app.url_path_for(
                "offers:accept-offer-from-user",
                cleaning_id=test_cleaning_with_offers.id,
                username=test_user_list[0].username,
            )
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_non_authorization_user_cant_update_offer_status(
            self, app: FastAPI,
            client: AsyncClient,
            test_cleaning_with_offers: CleaningInDB,
            test_user_list: List[UserInDB],
    ) -> None:
        selected_user = random.choice(test_user_list)
        response = await client.put(
            app.url_path_for(
                "offers:accept-offer-from-user",
                cleaning_id=test_cleaning_with_offers.id,
                username=selected_user.username
            )
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_cleaning_owner_cant_accept_multiple_offers(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user2: UserInDB,
            test_cleaning_with_offers: CleaningInDB,
            test_user_list: List[UserInDB],
    ) -> None:
        authorized_client = create_authorized_client(user=test_user2)
        first_response = await authorized_client.put(
            app.url_path_for(
                "offers:accept-offer-from-user",
                cleaning_id=test_cleaning_with_offers.id,
                username=test_user_list[0].username
            )
        )
        assert first_response.status_code == status.HTTP_200_OK

        second_response = await authorized_client.put(
            app.url_path_for(
                "offers:accept-offer-from-user",
                cleaning_id=test_cleaning_with_offers.id,
                username=test_user_list[1].username,
            )
        )
        assert second_response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_accepting_one_offer_rejects_all_others_offers(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user2: UserInDB,
            test_user_list: List[UserInDB],
            test_cleaning_with_offers: CleaningInDB,
    ) -> None:
        selected_user = random.choice(test_user_list)
        authorized_client = create_authorized_client(user=test_user2)
        response_put = await authorized_client.put(
            app.url_path_for(
                "offers:accept-offer-from-user",
                cleaning_id=test_cleaning_with_offers.id,
                username=selected_user.username,
            )
        )
        assert response_put.status_code == status.HTTP_200_OK

        response_get = await authorized_client.get(
            app.url_path_for("offers:list-offers-for-cleaning", cleaning_id=test_cleaning_with_offers.id)
        )
        assert response_get.status_code == status.HTTP_200_OK

        response_to_json = response_get.json()
        offers_to_cleaning = CleaningOffersListPublic(
            cleaning=response_to_json['cleaning'],
            offers=response_to_json['offers']
        )
        for offer in offers_to_cleaning.offers:
            if offer.executor.id == selected_user.id:
                assert offer.status == OfferStatus.accepted
            else:
                assert offer.status == OfferStatus.rejected


class TestCancelOffer:
    """Набор тестов содержит проверки функциональности маршрута отмены заказа"""

    @pytest.mark.asyncio
    async def test_customer_can_cancel_offer_after_it_has_been_accepted(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user3: UserInDB,
            test_cleaning_with_accepted_offer: CleaningInDB,
    ) -> None:
        authorized_client = create_authorized_client(user=test_user3)
        response = await authorized_client.put(
            app.url_path_for("offers:cancel-offer-from-user", cleaning_id=test_cleaning_with_accepted_offer.id)
        )

        assert response.status_code == status.HTTP_200_OK, response.json()
        offer = OfferPublic(**response.json())
        assert offer.status == OfferStatus.cancelled
        assert offer.user_id == test_user3.id
        assert offer.cleaning_id == test_cleaning_with_accepted_offer.id

    @pytest.mark.asyncio
    async def test_unauthorized_user_cant_cancel_offer_after_it_has_been_accepted(
            self, app: FastAPI,
            client: AsyncClient,
            test_cleaning_with_accepted_offer: CleaningInDB,
    ) -> None:
        response = await client.put(
            app.url_path_for(
                "offers:cancel-offer-from-user",
                cleaning_id=test_cleaning_with_accepted_offer.id)
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_only_accepted_offers_can_be_cancelled(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user4: UserInDB,
            test_cleaning_with_accepted_offer: CleaningInDB,
    ) -> None:
        authorized_client = create_authorized_client(user=test_user4)
        response = await authorized_client.put(
            app.url_path_for("offers:cancel-offer-from-user", cleaning_id=test_cleaning_with_accepted_offer.id)
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_cancelling_offer_sets_all_others_to_pending(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user3: UserInDB,
            test_cleaning_with_accepted_offer: CleaningInDB,
    ) -> None:
        authorized_client = create_authorized_client(user=test_user3)
        offer_repo = OffersRepository(app.state._db)

        response = await authorized_client.put(
            app.url_path_for("offers:cancel-offer-from-user", cleaning_id=test_cleaning_with_accepted_offer.id)
        )
        assert response.status_code == status.HTTP_200_OK

        offers = await offer_repo.list_offers_for_cleaning(cleaning=test_cleaning_with_accepted_offer)
        for offer in offers:
            if offer.user_id == test_user3.id:
                assert offer.status == OfferStatus.cancelled
            else:
                assert offer.status == OfferStatus.pending
