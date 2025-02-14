from typing import List
import datetime

from fastapi import APIRouter, Depends, Query

from app.models.feed import CleaningFeedItem
from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.database import get_repository
from app.db.repositories.feed import FeedRepository

router = APIRouter()


@router.get(
    "/cleanings/",
    response_model=List[CleaningFeedItem],
    name="feed:get-cleaning-feed-for-user",
    dependencies=[Depends(get_current_active_user)]
)
async def get_cleaning_feed_for_user(
        page_chunk_size: int = Query(
            default=20,
            ge=1,
            le=50,
            description="Used to determine how many cleaning feed item objects to return in the response."
        ),
        starting_date: datetime.datetime = Query(
            default=datetime.datetime.now() + datetime.timedelta(minutes=10),
            description="Used to determine the timestamp at which to begin querying for cleaning feed items."
        ),
        feed_repository: FeedRepository = Depends(get_repository(FeedRepository)),
) -> List[CleaningFeedItem]:
    return await feed_repository.fetch_cleaning_jobs_feed(
        page_chunk_size=page_chunk_size,
        starting_date=starting_date
    )
