from typing import List

from fastapi import Depends, status
from fastapi.exceptions import HTTPException

from app.api.dependencies.cleanings import get_cleaning_by_id_from_path, user_owns_cleaning
from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.users import get_user_by_username_from_path
from app.api.dependencies.database import get_repository
from app.db.repositories.offers import OffersRepository
from app.models.offer import OfferInDB, OfferStatus, CleaningOffersListPublic
from app.models.users import UserInDB
from app.models.cleaning import CleaningInDB


async def get_offer_for_cleaning_from_user(
        *, user_from_path: UserInDB,
        cleaning: CleaningInDB,
        offer_repo: OffersRepository,
) -> OfferInDB:
    offer = await offer_repo.get_offer_for_cleaning_from_user(cleaning=cleaning, user=user_from_path)
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer not found."
        )
    return offer


async def get_offer_for_cleaning_from_user_by_path(
        user_from_path: UserInDB = Depends(get_user_by_username_from_path),
        cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
        offer_repo: OffersRepository = Depends(get_repository(OffersRepository)),
) -> OfferInDB:
    return await get_offer_for_cleaning_from_user(
        user_from_path=user_from_path,
        cleaning=cleaning,
        offer_repo=offer_repo
    )


async def get_offer_for_cleaning_from_current_user(
        current_user: UserInDB = Depends(get_current_active_user),
        cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
        offer_repo: OffersRepository = Depends(get_repository(OffersRepository))
) -> OfferInDB:
    return await get_offer_for_cleaning_from_user(
        user_from_path=current_user, cleaning=cleaning,
        offer_repo=offer_repo
    )


async def list_offers_for_cleaning_by_id_from_path(
        cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
        offers_repo: OffersRepository = Depends(get_repository(OffersRepository)),
) -> List[OfferInDB]:
    return await offers_repo.list_offers_for_cleaning(cleaning=cleaning, populate=True)


async def check_offer_create_permissions(
        current_user: UserInDB = Depends(get_current_active_user),
        cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
        offers_repo: OffersRepository = Depends(get_repository(OffersRepository))
) -> None:
    if user_owns_cleaning(user=current_user, cleaning=cleaning):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Users are unable to create offers for cleaning jobs they own."
        )
    if await offers_repo.get_offer_for_cleaning_from_user(cleaning=cleaning, user=current_user, exclude_complete=True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Users aren`t allowed create more than one offer for a cleaning job."
        )


async def check_offer_list_permissions(
        current_user: UserInDB = Depends(get_current_active_user),
        cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path)
) -> None:
    if not user_owns_cleaning(user=current_user, cleaning=cleaning):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unable to access offers."
        )


async def check_offer_get_permission(
        current_user: UserInDB = Depends(get_current_active_user),
        cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
        offer: OfferInDB = Depends(get_offer_for_cleaning_from_user_by_path),
) -> None:
    if not user_owns_cleaning(user=current_user, cleaning=cleaning) and offer.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unable to access offer."
        )


async def check_offer_acceptance_permissions(
        current_user: UserInDB = Depends(get_current_active_user),
        cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
        offer: OfferInDB = Depends(get_offer_for_cleaning_from_user_by_path),
        existing_offers: CleaningOffersListPublic = Depends(list_offers_for_cleaning_by_id_from_path),
) -> None:
    if not user_owns_cleaning(user=current_user, cleaning=cleaning):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the owner of the cleaning may accept offers."
        )
    if offer.status != OfferStatus.pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only accept offers that are currently pending."
        )

    if OfferStatus.accepted in [offer.status for offer in existing_offers.offers]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="That cleaning job already has an accepted offer."
        )


def check_offer_cancel_permissions(offer: OfferInDB = Depends(get_offer_for_cleaning_from_current_user)) -> None:
    if offer.status != OfferStatus.accepted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only cancel offers that have been accepted."
        )


def check_offer_complete_permissions(
        offer: OfferInDB = Depends(get_offer_for_cleaning_from_current_user)
) -> None:
    if offer.status != OfferStatus.accepted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неподтвержденная сделка не может быть отмечена как завершенная"
        )


def check_offer_rescind_permissions(offer: OfferInDB = Depends(get_offer_for_cleaning_from_current_user)) -> None:
    if offer.status != OfferStatus.pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only rescind currently pending offers."
        )

