from typing import List, Tuple, Dict, Callable, Coroutine
import pytest_asyncio
from databases import Database
from collections import namedtuple

from app.db.repositories.cleanings import CleaningRepository
from app.db.repositories.offers import OffersRepository
from app.models.cleaning import CleaningInDB, CleaningCreate, CleaningType
from app.models.offer import OfferCreate, OfferInDB, CleaningOffersListPublic
from app.models.users import UserInDB


@pytest_asyncio.fixture
async def test_list_of_cleanings_with_pending_offers(
    db: Database,
    test_user: UserInDB,
    test_user_list: List[UserInDB]
) -> Dict[int, Tuple[CleaningInDB, List[OfferInDB]]]:

    cleaning_repo = CleaningRepository(db)
    offers_repo = OffersRepository(db)
    offers = {}
    CleaningOffers = namedtuple('CleaningOffers', ('cleaning', 'offer'))

    for num in range(5):
        created_cleaning = await cleaning_repo.create_cleaning(
            new_cleaning=CleaningCreate(
                name=f"test cleaning with offers - {num}",
                description=f"test desc for cleaning with offers - {num}",
                price=float(f"{num}9.99"),
                cleaning_type=CleaningType.spot_clean.value
            ),
            current_user=test_user
        )
        offers[created_cleaning.id] = CleaningOffers(created_cleaning, [])
        for user in test_user_list:
            offer = await offers_repo.create_offer_for_cleaning(
                new_offer=OfferCreate(
                    cleaning_id=created_cleaning.id,
                    user_id=user.id
                )
            )
            offers[created_cleaning.id].offer.append(offer)
    return offers


@pytest_asyncio.fixture
async def get_all_detail_cleanings_from_user(
        db: Database
) -> Callable[[UserInDB, bool], List[CleaningOffersListPublic]]:
    clean_repo = CleaningRepository(db)

    async def wrap(user: UserInDB, populate=False) -> List[CleaningOffersListPublic]:
        return await clean_repo.get_all_cleanings(current_user=user, populate=populate)
    return wrap

