from typing import List
from fastapi import APIRouter, Depends, Body, status

from app.models.users import UserInDB
from app.models.cleaning import CleaningInDB
from app.models.evaluations import EvaluationPublic, EvaluationAggregate, EvaluationCreated, EvaluationInDB
from app.api.dependencies.evaluations import (
    get_cleaner_evaluation_for_cleaning_from_path, list_evaluations_for_cleaning_from_path,
    check_evaluation_create_permissions)
from app.api.dependencies.cleanings import get_cleaning_by_id_from_path
from app.api.dependencies.offers import get_user_by_username_from_path
from app.api.dependencies.database import get_repository
from app.db.repositories.evaluations import EvaluationsRepository

router = APIRouter()


@router.post(
    "/{cleaning_id}/",
    response_model=EvaluationPublic,
    status_code=status.HTTP_201_CREATED,
    name="evaluations:create-evaluation-for-cleaning",
)
async def create_evaluation_for_cleaner(
        evaluation_create: EvaluationCreated = Body(..., embed=True),
        cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
        cleaner: UserInDB = Depends(get_user_by_username_from_path),
        evals_repo: EvaluationsRepository = Depends(get_repository(EvaluationsRepository)),
        _=Depends(check_evaluation_create_permissions),
) -> EvaluationPublic:
    return await evals_repo.create_evaluation_for_cleaner(
        evaluation_create=evaluation_create,
        cleaner=cleaner,
        cleaning=cleaning,
    )


@router.get(
    "/",
    response_model=List[EvaluationPublic],
    name="evaluations:list-evaluations-for-cleaner",
)
async def list_evaluations_for_cleaner(
        evaluations: List[EvaluationInDB] = Depends(list_evaluations_for_cleaning_from_path)
) -> List[EvaluationPublic]:
    return evaluations


@router.get(
    "/stats/",
    response_model=EvaluationAggregate,
    name="evaluations:get-stats-for-cleaner",
)
async def get_stats_for_cleaner(
        cleaner: UserInDB = Depends(get_user_by_username_from_path),
        eval_repo: EvaluationsRepository = Depends(get_repository(EvaluationsRepository)),
) -> EvaluationAggregate:
    return await eval_repo.get_cleaner_aggregates(cleaner=cleaner)


@router.get(
    "/{cleaning_id}/",
    response_model=EvaluationPublic,
    name="evaluations:get-evaluation-for-cleaner",
)
async def get_evaluation_for_cleaner(
    evaluation: EvaluationPublic = Depends(get_cleaner_evaluation_for_cleaning_from_path)
) -> EvaluationPublic:
    return evaluation
