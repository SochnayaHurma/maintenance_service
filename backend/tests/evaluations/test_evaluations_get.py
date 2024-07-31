from typing import Callable, List
from statistics import mean
import pytest
from fastapi import status, FastAPI
from httpx import AsyncClient

from app.models.cleaning import CleaningInDB
from app.models.evaluations import EvaluationPublic, EvaluationAggregate
from app.models.users import UserInDB


class TestGetEvaluations:
    """Набор тестов проверяющих выполнение функций эндпойнта выдачи отзывов"""

    @pytest.mark.asyncio
    async def test_authenticated_user_can_get_evaluation_for_cleaning(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user3: UserInDB, test_user4: UserInDB,
            test_list_of_cleanings_with_evaluated_offer: List[CleaningInDB],
    ) -> None:
        authorized_client = create_authorized_client(user=test_user4)
        response = await authorized_client.get(
            app.url_path_for("evaluations:get-evaluation-for-cleaner",
                             username=test_user3.username,
                             cleaning_id=test_list_of_cleanings_with_evaluated_offer[0].id),
        )
        assert response.status_code == status.HTTP_200_OK
        evaluation = EvaluationPublic(**response.json())
        assert evaluation.cleaning_id == test_list_of_cleanings_with_evaluated_offer[0].id
        assert evaluation.cleaner_id == test_user3.id
        assert "lorem" in evaluation.comment
        assert list(filter(lambda headline: headline in evaluation.headline, ['good job', 'bad job', 'excellent job']))
        assert (evaluation.professionalism >= 0) and (evaluation.professionalism <= 5)
        assert (evaluation.completeness >= 0) and (evaluation.completeness <= 5)
        assert (evaluation.efficiency >= 0) and (evaluation.efficiency <= 5)
        assert (evaluation.overall_rating >= 0) and (evaluation.overall_rating <= 5)

    @pytest.mark.asyncio
    async def test_authenticated_user_can_get_list_of_evaluations_for_cleaner(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user4: UserInDB, test_user3: UserInDB,
            test_list_of_cleanings_with_evaluated_offer: List[CleaningInDB],
    ) -> None:
        authorized_client = create_authorized_client(user=test_user4)
        response = await authorized_client.get(
            app.url_path_for("evaluations:list-evaluations-for-cleaner",
                             username=test_user3.username)
        )
        assert response.status_code == status.HTTP_200_OK
        evaluations = [EvaluationPublic(**evaluation) for evaluation in response.json()]
        assert len(evaluations) > 0
        for evaluation in evaluations:
            assert evaluation.cleaner_id == test_user3.id
            assert (evaluation.overall_rating >= 0) and (evaluation.overall_rating <= 5)

    @pytest.mark.asyncio
    async def test_authenticated_user_can_get_aggregate_stats_for_cleaner(
            self, app: FastAPI,
            create_authorized_client: Callable[..., AsyncClient],
            test_user4: UserInDB, test_user3: UserInDB,
            test_list_of_cleanings_with_evaluated_offer: List[CleaningInDB],
    ) -> None:
        authorized_client = create_authorized_client(user=test_user4)
        response_get_list = await authorized_client.get(
            app.url_path_for("evaluations:list-evaluations-for-cleaner",
                             username=test_user3.username)
        )
        assert response_get_list.status_code == status.HTTP_200_OK
        evaluations = [EvaluationPublic(**evaluation) for evaluation in response_get_list.json()]

        response_get_one = await authorized_client.get(
            app.url_path_for("evaluations:get-stats-for-cleaner",
                             username=test_user3.username)
        )
        assert response_get_one.status_code == status.HTTP_200_OK
        stats = EvaluationAggregate(**response_get_one.json())

        assert stats.total_evaluations == len(evaluations)
        assert max([evaluation.overall_rating for evaluation in evaluations]) == stats.max_overall_rating
        assert min([evaluation.overall_rating for evaluation in evaluations]) == stats.min_overall_rating
        assert mean([evaluation.overall_rating for evaluation in evaluations]) == stats.avg_overall_rating
        assert mean(
            [evaluation.professionalism for evaluation in evaluations if evaluation is not None]
        ) == stats.avg_professionalism
        assert mean(
            [evaluation.efficiency for evaluation in evaluations if evaluation is not None]
        ) == stats.avg_efficiency
        assert mean(
            [evaluation.completeness for evaluation in evaluations if evaluation is not None]
        ) == stats.avg_completeness
        assert len(
            [evaluation for evaluation in evaluations if evaluation.overall_rating == 1]
        ) == stats.one_stars
        assert len(
            [evaluation for evaluation in evaluations if evaluation.overall_rating == 2]
        ) == stats.two_stars
        assert len(
            [evaluation for evaluation in evaluations if evaluation.overall_rating == 3]
        ) == stats.three_stars
        assert len(
            [evaluation for evaluation in evaluations if evaluation.overall_rating == 4]
        ) == stats.four_stars
        assert len(
            [evaluation for evaluation in evaluations if evaluation.overall_rating == 5]
        ) == stats.five_stars

    @pytest.mark.asyncio
    async def test_unauthenticated_user_forbidden_from_get_evaluation(
            self, app: FastAPI,
            client: AsyncClient,
            test_user3: UserInDB,
            test_list_of_cleanings_with_evaluated_offer: List[CleaningInDB],
    ) -> None:
        response_get_one = await client.get(
            app.url_path_for("evaluations:get-evaluation-for-cleaner",
                             username=test_user3.username,
                             cleaning_id=test_list_of_cleanings_with_evaluated_offer[0].id)
        )
        assert response_get_one.status_code == status.HTTP_401_UNAUTHORIZED
        response_get_list = await client.get(
            app.url_path_for("evaluations:list-evaluations-for-cleaner",
                             username=test_user3.username)
        )
        assert response_get_list.status_code == status.HTTP_401_UNAUTHORIZED
