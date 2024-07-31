import pytest_asyncio
from databases import Database
from typing import Callable, List

from app.models.users import UserInDB
from app.models.offer import CleaningOffersListPublic
from app.db.repositories.cleanings import CleaningRepository


@pytest_asyncio.fixture
async def get_all_detail_cleanings_from_user(
        db: Database
) -> Callable[[UserInDB, bool], List[CleaningOffersListPublic]]:
    clean_repo = CleaningRepository(db)

    async def wrap(user: UserInDB, populate=False) -> List[CleaningOffersListPublic]:
        return await clean_repo.get_all_cleanings(current_user=user, populate=populate)
    return wrap
