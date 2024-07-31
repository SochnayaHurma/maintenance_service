import pytest, pytest_asyncio
import random
from databases import Database
from typing import List

from app.db.repositories.cleanings import CleaningRepository
from app.db.repositories.evaluations import EvaluationsRepository
from app.db.repositories.offers import OffersRepository
from app.models.cleaning import CleaningInDB, CleaningCreate
from app.models.offer import OfferCreate
from app.models.evaluations import EvaluationCreated
from app.models.users import UserInDB


@pytest.fixture(scope="session")
def new_evaluations_instance() -> EvaluationCreated:
    comment = random.choice(['good job', 'bad job', 'excellent job'])
    return EvaluationCreated(
        no_show=True,
        headline=comment,
        comment=f"lorem",
        professionalism=random.randint(0, 5),
        completeness=random.randint(0, 5),
        efficiency=random.randint(0, 5),
        overall_rating=random.randint(0, 5),
    )


async def create_cleaning_with_evaluated_offer_helper(
        *, db: Database,
        owner: UserInDB,
        cleaner: UserInDB,
        cleaning_create: CleaningCreate,
        evaluation_create: EvaluationCreated,
) -> CleaningInDB:
    cleaning_repo = CleaningRepository(db)
    offers_repo = OffersRepository(db)
    evals_repo = EvaluationsRepository(db)

    cleaning_created = await cleaning_repo.create_cleaning(new_cleaning=cleaning_create, current_user=owner)
    offer_created = await offers_repo.create_offer_for_cleaning(
        new_offer=OfferCreate(cleaning_id=cleaning_created.id, user_id=cleaner.id)
    )
    await offers_repo.accept_offer(offer=offer_created)
    await evals_repo.create_evaluation_for_cleaner(
        evaluation_create=evaluation_create, cleaner=cleaner, cleaning=cleaning_created
    )
    return cleaning_created


@pytest_asyncio.fixture
async def test_list_of_cleanings_with_evaluated_offer(
        db: Database,
        test_user2: UserInDB, test_user3: UserInDB,
        new_evaluations_instance: EvaluationCreated
) -> List[CleaningInDB]:
    return [
        await create_cleaning_with_evaluated_offer_helper(
            db=db,
            owner=test_user2,
            cleaner=test_user3,
            cleaning_create=CleaningCreate(
                name=f"test cleaning {num}",
                description=f"test description {num}",
                price=float(f"{num}9.99"),
                cleaning_type="full_clean",
            ),
            evaluation_create=new_evaluations_instance,
        )
        for num in range(5)
    ]
