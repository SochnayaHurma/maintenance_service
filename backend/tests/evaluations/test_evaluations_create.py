import pytest
from typing import Callable
from httpx import AsyncClient
from fastapi import FastAPI, status

from app.models.cleaning import CleaningInDB
from app.models.evaluations import EvaluationCreated, EvaluationPublic
from app.models.offer import OfferStatus
from app.models.users import UserInDB


class TestCreateEvaluations:
    """Набор тестов проверяющих выполнения функций эндпойнта создания отзыва(CreateEvaluations)"""

    @pytest.mark.asyncio
    async def test_owner_can_leave_evaluation_for_cleaner_and_mark_offer_complete(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user2: UserInDB,
            test_user3: UserInDB,
            test_cleaning_with_accepted_offer: CleaningInDB,
            new_evaluations_instance: EvaluationCreated,
    ) -> None:
        """
        Тест: отправляет post запрос на создание отзыва и проверяет на
            - наличие всех видимых входных полей в ответе, которые мы передали в POST
            - статус заказа на который был сделан отзыв должен поменяться на Accepted
        """
        authorized_client = create_authorized_client(user=test_user2)
        response_post = await authorized_client.post(
            app.url_path_for("evaluations:create-evaluation-for-cleaning",
                             username=test_user3.username,
                             cleaning_id=test_cleaning_with_accepted_offer.id),
            json={"evaluation_create": new_evaluations_instance.dict()},
        )
        assert response_post.status_code == status.HTTP_201_CREATED
        evaluation = EvaluationPublic(**response_post.json())
        assert evaluation.no_show == new_evaluations_instance.no_show
        assert evaluation.headline == new_evaluations_instance.headline
        assert evaluation.comment == new_evaluations_instance.comment
        assert evaluation.overall_rating == new_evaluations_instance.overall_rating

        response_get = await authorized_client.get(
            app.url_path_for("offers:get-offer-from-user",
                             cleaning_id=test_cleaning_with_accepted_offer.id,
                             username=test_user3.username)
        )
        assert response_get.status_code == status.HTTP_200_OK
        assert response_get.json().get("status") == OfferStatus.completed.value

    @pytest.mark.asyncio
    async def test_non_owner_cant_leave_review(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user3: UserInDB,
            test_user4: UserInDB,
            test_cleaning_with_accepted_offer: CleaningInDB,
            new_evaluations_instance: EvaluationCreated,
    ) -> None:
        """Тест: Делает POST запрос на отзыв непринятой сделки
            и ожидает статус 403 Frbidden
        """
        authorized_client = create_authorized_client(user=test_user4)
        response = await authorized_client.post(
            app.url_path_for("evaluations:create-evaluation-for-cleaning",
                             username=test_user3.username,
                             cleaning_id=test_cleaning_with_accepted_offer.id
                             ),
            json={"evaluation_create": new_evaluations_instance.dict()},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_owner_cant_leave_review_for_wrong_user(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user2: UserInDB, test_user4: UserInDB,
            test_cleaning_with_accepted_offer: CleaningInDB,
            new_evaluations_instance: EvaluationCreated,
    ) -> None:
        """Тест: Делает POST запрос на несуществующий заказ ожидая статус 400"""
        authorized_client = create_authorized_client(user=test_user2)
        response = await authorized_client.post(
            app.url_path_for("evaluations:create-evaluation-for-cleaning",
                             username=test_user4.username,
                             cleaning_id=test_cleaning_with_accepted_offer.id),
            json={"evaluation_create": new_evaluations_instance.dict()}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_owner_cant_leave_multiple_reviews(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user2: UserInDB, test_user3: UserInDB,
            test_cleaning_with_accepted_offer: CleaningInDB,
            new_evaluations_instance: EvaluationCreated,
    ) -> None:
        """Тест: Делает два POST запроса ожидая на второй негативный код ответа"""
        authorized_client = create_authorized_client(user=test_user2)
        response_first = await authorized_client.post(
            app.url_path_for("evaluations:create-evaluation-for-cleaning",
                             username=test_user3.username,
                             cleaning_id=test_cleaning_with_accepted_offer.id),
            json={"evaluation_create": new_evaluations_instance.dict()}
        )
        assert response_first.status_code == status.HTTP_201_CREATED

        response_second = await authorized_client.post(
            app.url_path_for("evaluations:create-evaluation-for-cleaning",
                             username=test_user3.username,
                             cleaning_id=test_cleaning_with_accepted_offer.id),
            json={"evaluation_create": new_evaluations_instance.dict()}
        )
        assert response_second.status_code == status.HTTP_400_BAD_REQUEST
