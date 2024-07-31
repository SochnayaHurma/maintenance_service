from datetime import datetime
from typing import List, Dict

from databases import Database

from app.db.repositories.base import BaseRepository
from app.db.repositories.users import UsersRepository
from app.models.feed import CleaningFeedItem

# https://habr.com/ru/articles/268983/
# https://postgrespro.ru/docs/postgrespro/9.5/functions-conditional#functions-greatest-least
FETCH_CLEANING_JOBS_FOR_FEED_QUERY_ = """
    SELECT id, name, description, price, cleaning_type,
           owner, created_at, updated_at, 
           CASE
            WHEN created_at = updated_at THEN 'is_create'
            ELSE 'is_update'
           END AS event_type,
           GREATEST(created_at, updated_at) AS event_timestamp,
           ROW_NUMBER() OVER ( ORDER BY GREATEST(created_at, updated_at) DESC) AS row_number
    FROM cleanings
    WHERE updated_at < :starting_date
    ORDER BY GREATEST(created_at, updated_at) DESC
    LIMIT :page_chunk_size;
"""
FETCH_CLEANING_JOBS_FOR_FEED_QUERY = """
    SELECT id, name, description, price, cleaning_type,
        owner, created_at, updated_at,
        event_type, event_timestamp,
        ROW_NUMBER() OVER ( ORDER BY event_timestamp DESC ) AS row_number
    FROM (
        (
            SELECT id, name,description, price, cleaning_type,
                owner, created_at, updated_at, 
                updated_at AS event_timestamp, 'is_update' AS event_type
            FROM cleanings
            WHERE updated_at < :starting_date AND updated_at != created_at
            ORDER BY updated_at DESC
            LIMIT :page_chunk_size
        ) UNION (
            SELECT id, name, description, price, cleaning_type,
                owner, created_at, updated_at,
                created_at AS event_timestamp, 'is_create' AS event_type
            FROM cleanings
            WHERE created_at < :starting_date
            ORDER BY created_at DESC
            LIMIT :page_chunk_size
        )
    ) AS cleaning_feed
    ORDER BY event_timestamp DESC
    LIMIT :page_chunk_size;
"""


class FeedRepository(BaseRepository):
    """Содержит методы для излвлечения данных для feed-ленты"""

    def __init__(self, db: Database):
        super().__init__(db)
        self.users_repo = UsersRepository(db)

    async def fetch_cleaning_jobs_feed(self, *, page_chunk_size: int = 20,
                                       starting_date: datetime,
                                       populate: bool = True) -> List[CleaningFeedItem]:
        cleaning_feed_item_records = await self.db.fetch_all(
            query=FETCH_CLEANING_JOBS_FOR_FEED_QUERY,
            values={"page_chunk_size": page_chunk_size, "starting_date": starting_date}
        )
        if populate:
            return [
                await self.populate_cleaning_feed_item(feed_item=dict(feed_item))
                for feed_item in cleaning_feed_item_records
            ]
        return [CleaningFeedItem(**item) for item in cleaning_feed_item_records]

    async def populate_cleaning_feed_item(self, *, feed_item: Dict) -> CleaningFeedItem:
        user_id = feed_item.pop("owner")
        return CleaningFeedItem(
            **feed_item,
            owner=await self.users_repo.get_user_by_id(user_id=user_id)
        )
