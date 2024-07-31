from typing import List

from fastapi import APIRouter, Body, Depends, status, Path
from fastapi.exceptions import HTTPException

from app.api.dependencies.auth import get_current_active_user
from app.models.cleaning import CleaningCreate, CleaningInDB, CleaningPublic, CleaningUpdate
from app.models.offer import CleaningOffersListPublic
from app.db.repositories.cleanings import CleaningRepository
from app.api.dependencies.database import get_repository
from app.api.dependencies.cleanings import (
    get_cleaning_by_id_from_path, check_cleaning_modification_permissions,
    get_cleaning_detail_by_id_from_path
)
from app.models.users import UserInDB

router = APIRouter()


@router.get(
    "/",
    response_model=List[CleaningOffersListPublic],
    name="cleanings:get-all-user-cleanings"
)
async def get_all_cleanings(
        cleanings_repo: CleaningRepository = Depends(get_repository(CleaningRepository)),
        current_user: UserInDB = Depends(get_current_active_user),
) -> List[CleaningInDB]:
    return await cleanings_repo.get_all_cleanings(current_user=current_user, populate=True)


@router.get(
    "/{cleaning_id}/",
    response_model=CleaningOffersListPublic,
    name="cleanings:get-cleaning-by-id"
)
async def get_cleaning_by_id(
        cleaning: CleaningPublic = Depends(get_cleaning_detail_by_id_from_path)
) -> CleaningInDB:
    return cleaning


@router.post(
    "/",
    response_model=CleaningPublic,
    status_code=status.HTTP_201_CREATED,
    name="cleanings:create-cleaning"
)
async def create_new_cleaning(
        new_cleaning: CleaningCreate = Body(..., embed=True),
        current_user: UserInDB = Depends(get_current_active_user),
        cleanings_repo: CleaningRepository = Depends(get_repository(CleaningRepository)),
) -> CleaningPublic:
    return await cleanings_repo.create_cleaning(new_cleaning=new_cleaning, current_user=current_user)


@router.put(
    "/{cleaning_id}/",
    response_model=CleaningPublic,
    name="cleanings:update-cleaning-by-id"
)
async def update_cleaning_by_id(
        cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
        cleaning_update: CleaningUpdate = Body(..., embed=True),
        cleanings_repo: CleaningRepository = Depends(get_repository(CleaningRepository)),
        current_user: UserInDB = Depends(get_current_active_user),
        _ = Depends(check_cleaning_modification_permissions)
) -> CleaningPublic:
    updated_cleaning = await cleanings_repo.update_cleaning(
        cleaning=cleaning, cleaning_update=cleaning_update,
        current_user=current_user
    )
    return updated_cleaning


@router.delete(
    "/{cleaning_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    name="cleanings:delete-cleaning-by-id"
)
async def delete_cleaning_by_id(
        cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
        cleaning_repo: CleaningRepository = Depends(get_repository(CleaningRepository)),
        _ = Depends(check_cleaning_modification_permissions)
) -> None:
    await cleaning_repo.delete_cleaning_by_id(cleaning=cleaning)
