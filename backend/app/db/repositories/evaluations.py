from typing import List, Optional
from databases import Database
from fastapi import HTTPException

from app.db.repositories.base import BaseRepository
from app.db.repositories.offers import OffersRepository
from app.models.evaluations import EvaluationInDB, EvaluationCreated, EvaluationAggregate, EvaluationPublic
from app.models.users import UserInDB
from app.models.cleaning import CleaningInDB


CREATE_OWNER_EVALUATION_FOR_CLEANER_QUERY = """
    INSERT INTO cleaning_to_cleaner_evaluations(
        cleaning_id,
        cleaner_id,
        no_show,
        headline,
        comment,
        completeness,
        professionalism,
        efficiency,
        overall_rating
    )
    VALUES
    (
        :cleaning_id,
        :cleaner_id,
        :no_show,
        :headline,
        :comment,
        :completeness,
        :professionalism,
        :efficiency,
        :overall_rating
    )
    RETURNING no_show,
        cleaning_id,
        cleaner_id,
        headline,
        comment,
        professionalism,
        completeness,
        efficiency,
        overall_rating,
        created_at,
        updated_at;
"""

GET_CLEANER_EVALUATION_FOR_CLEANING_QUERY = """
    SELECT no_show,
        cleaning_id,
        cleaner_id,
        headline,
        comment,
        professionalism,
        completeness,
        efficiency,
        overall_rating,
        created_at,
        updated_at
    FROM cleaning_to_cleaner_evaluations
    WHERE cleaner_id = :cleaner_id
        AND cleaning_id = :cleaning_id;
"""

LIST_EVALUATIONS_FOR_CLEANER_QUERY = """
    SELECT no_show,
        cleaning_id,
        cleaner_id,
        headline,
        comment,
        professionalism,
        completeness,
        efficiency,
        overall_rating,
        created_at,
        updated_at
    FROM cleaning_to_cleaner_evaluations
    WHERE cleaner_id = :cleaner_id;
"""

GET_CLEANER_AGGREGATE_RATING_QUERY = """
    SELECT 
        AVG(professionalism) AS avg_professionalism,
        AVG(completeness) AS avg_completeness,
        AVG(efficiency) AS avg_efficiency,
        AVG(overall_rating) AS avg_overall_rating,
        MIN(overall_rating) AS min_overall_rating,
        MAX(overall_rating) AS max_overall_rating,
        COUNT(cleaning_id) AS total_evaluations,
        SUM(no_show::int) AS total_no_show,
        COUNT(overall_rating) FILTER(WHERE overall_rating = 1) AS one_stars,
        COUNT(overall_rating) FILTER(WHERE overall_rating = 2) AS two_stars,
        COUNT(overall_rating) FILTER(WHERE overall_rating = 3) AS three_stars,
        COUNT(overall_rating) FILTER(WHERE overall_rating = 4) AS four_stars,
        COUNT(overall_rating) FILTER(WHERE overall_rating = 5) AS five_stars
    FROM cleaning_to_cleaner_evaluations
    WHERE cleaner_id = :cleaner_id;
"""


class EvaluationsRepository(BaseRepository):
    """
    Класс принимает экземпляр (Database) подключенрия к базе данных
    Содержит методы взаимодействия с таблицей Evaluations в базе данных
    """
    def __init__(self, db: Database) -> None:
        super().__init__(db)
        self.offers_repo = OffersRepository(db)

    async def create_evaluation_for_cleaner(
            self, *,
            evaluation_create: EvaluationCreated,
            cleaner: UserInDB,
            cleaning: CleaningInDB,
    ) -> EvaluationInDB:
        async with self.db.transaction():
            created_evaluation = await self.db.fetch_one(
                query=CREATE_OWNER_EVALUATION_FOR_CLEANER_QUERY,
                values={**evaluation_create.dict(), "cleaning_id": cleaning.id, "cleaner_id": cleaner.id}
            )
            await self.offers_repo.mark_offer_completed(
                cleaning=cleaning,
                cleaner=cleaner,
            )
            return EvaluationInDB(**created_evaluation)

    async def list_evaluations_for_cleaner(self, *, cleaner: UserInDB) -> List[EvaluationPublic]:
        evaluations = await self.db.fetch_all(
            query=LIST_EVALUATIONS_FOR_CLEANER_QUERY,
            values={"cleaner_id": cleaner.id}
        )
        return [EvaluationPublic(**evaluation) for evaluation in evaluations]

    async def get_cleaner_evaluation_for_cleaning(
            self, *, cleaning: CleaningInDB, cleaner: UserInDB
    ) -> Optional[EvaluationPublic]:
        evaluation = await self.db.fetch_one(
            query=GET_CLEANER_EVALUATION_FOR_CLEANING_QUERY,
            values={"cleaner_id": cleaner.id, "cleaning_id": cleaning.id}
        )
        if not evaluation:
            return None
        return EvaluationPublic(**evaluation)

    async def get_cleaner_aggregates(self, *, cleaner: UserInDB) -> EvaluationAggregate:
        stats = await self.db.fetch_one(
            query=GET_CLEANER_AGGREGATE_RATING_QUERY,
            values={"cleaner_id": cleaner.id}
        )
        return EvaluationAggregate(**stats)
