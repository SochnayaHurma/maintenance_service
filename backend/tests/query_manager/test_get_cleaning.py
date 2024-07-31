from typing import Callable, Optional, Dict

import pytest
import pytest_asyncio
from databases import Database

from app.models.cleaning import CleaningInDB

INSERT_CLEANING = "INSERT INTO cleanings( %(names)s ) VALUES ( %(values)s )"
SELECT_CLEANING = "SELECT %(names)s FROM cleanings"


@pytest_asyncio.fixture
async def insert_cleaning(db: Database) -> Callable:
    async def wrap(data: Optional[Dict]) -> CleaningInDB:
        done_sql = INSERT_CLEANING % {'names': ', '.join(data.keys()), 'values': ', '.join(data.values())}
        return await db.execute(done_sql)
    return wrap


@pytest_asyncio.fixture
async def select_all_cleaning(db: Database) -> Callable:
    async def wrap(data: Optional[Dict]) -> CleaningInDB:
        done_sql = SELECT_CLEANING % {'names': ', '.join(data.keys())}
        return await db.execute(done_sql)
    return wrap



class TestGetOneCleaning:
    """
    Набор тестов проверяющих корректность возвращаемых данных с базы данных
    """
    @pytest.mark.asyncio
    async def test_cleaning_create_returned_expected_result(self) -> None:
        data = {"name": "qwe",
                "description": "asd",
                "cleaning_type": "spot_clean",
                "price": 20.5,
                "user": 2}