from fastapi import Depends, Path, status
from fastapi.exceptions import HTTPException

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.database import get_repository
from app.db.repositories.cleanings import CleaningRepository
from app.models.cleaning import CleaningInDB, CleaningPublic
from app.models.offer import CleaningOffersListPublic
from app.models.users import UserInDB


async def get_cleaning_by_id_from_path(
        cleaning_id: int = Path(..., ge=1),
        current_user: UserInDB = Depends(get_current_active_user),
        clean_repo: CleaningRepository = Depends(get_repository(CleaningRepository)),
) -> CleaningOffersListPublic:
    cleaning = await clean_repo.get_cleaning_by_id(cleaning_id=cleaning_id,
                                                   current_user=current_user,
                                                   populate=False)
    if not cleaning:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cleaning found with that id."
        )
    return cleaning


async def get_cleaning_detail_by_id_from_path(
        cleaning_id: int = Path(..., ge=1),
        current_user: UserInDB = Depends(get_current_active_user),
        clean_repo: CleaningRepository = Depends(get_repository(CleaningRepository)),
) -> CleaningOffersListPublic:
    cleaning = await clean_repo.get_cleaning_by_id(cleaning_id=cleaning_id,
                                                   current_user=current_user,
                                                   populate=True)
    if not cleaning:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cleaning found with that id."
        )
    return cleaning


async def check_cleaning_modification_permissions(
    current_user: UserInDB = Depends(get_current_active_user),
    cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
) -> None:
    if not user_owns_cleaning(user=current_user, cleaning=cleaning):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Action forbidden. Users are only able to modify cleaning they own."
        )


def user_owns_cleaning(*, user: UserInDB, cleaning: CleaningInDB) -> bool:
    if isinstance(cleaning.owner, int):
        return cleaning.owner == user.id
    return cleaning.owner.id == user.id