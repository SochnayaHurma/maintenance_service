from typing import List
from fastapi import status, Depends, HTTPException

from app.models.cleaning import CleaningInDB
from app.models.evaluations import EvaluationPublic
from app.models.offer import OfferStatus, OfferInDB
from app.models.users import UserInDB
from app.api.dependencies.offers import get_offer_for_cleaning_from_user_by_path
from app.api.dependencies.cleanings import get_cleaning_by_id_from_path, user_owns_cleaning
from app.api.dependencies.users import get_user_by_username_from_path
from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.database import get_repository
from app.db.repositories.evaluations import EvaluationsRepository


async def get_cleaner_evaluation_for_cleaning_from_path(
        cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
        cleaner: UserInDB = Depends(get_user_by_username_from_path),
        eval_repo: EvaluationsRepository = Depends(get_repository(EvaluationsRepository))
) -> EvaluationPublic:
    evaluation = await eval_repo.get_cleaner_evaluation_for_cleaning(cleaning=cleaning, cleaner=cleaner)
    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No evaluation not found for that cleaning.",
        )
    return evaluation


async def list_evaluations_for_cleaning_from_path(
        current_user: UserInDB = Depends(get_current_active_user),
        cleaner: UserInDB = Depends(get_user_by_username_from_path),
        eval_repo: EvaluationsRepository = Depends(get_repository(EvaluationsRepository))
) -> List[EvaluationPublic]:
    return await eval_repo.list_evaluations_for_cleaner(cleaner=cleaner)


def check_evaluation_create_permissions(
        current_user: UserInDB = Depends(get_current_active_user),
        cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
        cleaner: UserInDB = Depends(get_user_by_username_from_path),
        offer: OfferInDB = Depends(get_offer_for_cleaning_from_user_by_path),
        evals_repo: EvaluationsRepository = Depends(get_repository(EvaluationsRepository)),
) -> None:
    if not user_owns_cleaning(user=current_user, cleaning=cleaning):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to leave an evaluation for this user."
        )
    if offer.user_id != cleaner.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Users are unable to leave evaluations for cleaning jobs they do not own."
        )
    if offer.status != OfferStatus.accepted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only users with accepted offers can be evaluated."
        )
