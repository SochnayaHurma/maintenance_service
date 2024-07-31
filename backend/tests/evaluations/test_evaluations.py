import pytest
from typing import List
from fastapi import FastAPI, status
from httpx import AsyncClient

from app.models.cleaning import CleaningInDB
from app.models.evaluations import EvaluationCreated
from app.models.users import UserInDB


class TestEvaluationsRoutes:
    """Набор тестов проверяющих доступность маршрутов приложения отзывов(Evaluations)"""

    @pytest.mark.asyncio
    async def test_routes_exist(
            self, app: FastAPI,
            client: AsyncClient,
            new_evaluations_instance: EvaluationCreated,
            test_list_of_cleanings_with_evaluated_offer: List[CleaningInDB],
            test_user3: UserInDB, test_user2: UserInDB,
    ) -> None:
        response_create = await client.post(
            app.url_path_for(
                "evaluations:create-evaluation-for-cleaning",
                cleaning_id=test_list_of_cleanings_with_evaluated_offer[0].id,
                username=test_user2.username),
            json={"evaluation_create": new_evaluations_instance.dict()}
        )
        assert response_create.status_code != status.HTTP_404_NOT_FOUND

        response_get_one = await client.get(
            app.url_path_for("evaluations:get-evaluation-for-cleaner",
                             cleaning_id=test_list_of_cleanings_with_evaluated_offer[0].id,
                             username=test_user3.username)
        )
        assert response_get_one.status_code != status.HTTP_404_NOT_FOUND

        response_get_list = await client.get(
            app.url_path_for("evaluations:list-evaluations-for-cleaner", username=test_user3.username)
        )
        assert response_get_list.status_code != status.HTTP_404_NOT_FOUND

        response_get_stats = await client.get(
            app.url_path_for("evaluations:get-stats-for-cleaner", username=test_user3.username)
        )
        assert response_get_stats.status_code != status.HTTP_404_NOT_FOUND
        