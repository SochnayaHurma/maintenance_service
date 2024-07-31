from typing import List
import pytest_asyncio
from databases import Database

from app.db.repositories.cleanings import CleaningRepository
from app.models.cleaning import CleaningInDB, CleaningCreate, CleaningUpdate
from app.models.users import UserInDB


@pytest_asyncio.fixture
async def test_list_of_new_and_updated_cleanings(
        db: Database,
        test_user_list: List[UserInDB]
) -> List[CleaningInDB]:
    cleanings_repo = CleaningRepository(db)
    new_cleaning = [
        await cleanings_repo.create_cleaning(
            current_user=test_user_list[i % len(test_user_list)],
            new_cleaning=CleaningCreate(
                name=f"feed item cleaning job - {i}",
                description=f"test description for feed item cleaning: {i}",
                price=float(f"{i}9.99"),
                cleaning_type=["full_clean", "spot_clean", "dust_up"][i % 3],
            )
        )
        for i in range(50)
    ]
    for i, cleaning in enumerate(new_cleaning):
        if i % 4 == 0:
            updated_cleaning = await cleanings_repo.update_cleaning(
                cleaning=cleaning,
                cleaning_update=CleaningUpdate(
                    description=f"Updated {cleaning.description}",
                    price=cleaning.price + 100.0
                ),
                current_user=cleaning.owner
            )
            new_cleaning[i] = updated_cleaning
    return new_cleaning
