from typing import List

from fastapi import APIRouter, Path, Depends, status

from app.models.offer import OfferPublic, OfferCreate, OfferUpdate, OfferInDB, OfferStatus, CleaningOffersListPublic
from app.models.cleaning import CleaningInDB
from app.models.users import UserInDB
from app.db.repositories.offers import OffersRepository
from app.api.dependencies.cleanings import get_cleaning_by_id_from_path
from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.database import get_repository
from app.api.dependencies.offers import (
    check_offer_create_permissions, check_offer_get_permission,
    check_offer_list_permissions, check_offer_acceptance_permissions,
    check_offer_cancel_permissions, check_offer_rescind_permissions,
    list_offers_for_cleaning_by_id_from_path, get_offer_for_cleaning_from_user_by_path,
    get_offer_for_cleaning_from_current_user, check_offer_complete_permissions
)

router = APIRouter()


@router.get(
    "/{username}/",
    response_model=OfferPublic,
    name="offers:get-offer-from-user"
)
async def get_one_offer(
        offer: OfferPublic = Depends(get_offer_for_cleaning_from_user_by_path),
         _=Depends(check_offer_get_permission),
) -> OfferPublic:
    return offer


@router.get(
    "/",
    response_model=CleaningOffersListPublic,
    name="offers:list-offers-for-cleaning",
)
async def get_list_offer(
        offers: List[OfferInDB] = Depends(list_offers_for_cleaning_by_id_from_path),
        _ = Depends(check_offer_list_permissions),
) -> List[OfferPublic]:
    return offers


@router.post(
    "/",
    response_model=OfferPublic,
    name="offers:create-offer",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(check_offer_create_permissions)]
)
async def create_offer(
        cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
        offer_repo: OffersRepository = Depends(get_repository(OffersRepository)),
        current_user: UserInDB = Depends(get_current_active_user),
) -> OfferPublic:
    new_offer = OfferCreate(cleaning_id=cleaning.id, user_id=current_user.id)
    return await offer_repo.create_offer_for_cleaning(new_offer=new_offer)


@router.put(
    "/complete/",
    response_model=OfferPublic,
    name="offers:complete-offer-from-user",
)
async def complete_offer_update(
        offer: OfferInDB = Depends(get_offer_for_cleaning_from_current_user),
        offer_repo: OffersRepository = Depends(get_repository(OffersRepository)),
        _=Depends(check_offer_complete_permissions)
) -> OfferPublic:
    return await offer_repo.complete_offer(offer=offer)


@router.put(
    "/{username}/",
    response_model=OfferPublic,
    name="offers:accept-offer-from-user",
)
async def accept_offer_update(
        offer: OfferPublic = Depends(get_offer_for_cleaning_from_user_by_path),
        offer_repo: OffersRepository = Depends(get_repository(OffersRepository)),
        _ = Depends(check_offer_acceptance_permissions),
) -> OfferPublic:
    return await offer_repo.accept_offer(
            offer=offer
    )


@router.put(
    "/",
    response_model=OfferPublic,
    name="offers:cancel-offer-from-user",
)
async def cancel_offer_update(
        offer: OfferInDB = Depends(get_offer_for_cleaning_from_current_user),
        offer_repo: OffersRepository = Depends(get_repository(OffersRepository)),
        _=Depends(check_offer_cancel_permissions)
) -> OfferPublic:
    # TODO: ACCPET/CANCEL/COMPLETE могут быть одним маршрутом с маркой action в теле
    return await offer_repo.cancel_offer(offer=offer)


@router.delete(
    "/",
    name="offers:rescind-offer-from-user",
)
async def rescind_offer(
        offer: OfferInDB = Depends(get_offer_for_cleaning_from_current_user),
        offers_repo: OffersRepository = Depends(get_repository(OffersRepository)),
        _=Depends(check_offer_rescind_permissions)
):
    return await offers_repo.rescind_offer(offer=offer)
