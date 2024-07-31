from datetime import datetime
from typing import Literal, Optional

from app.models.core import BaseModel
from app.models.cleaning import CleaningPublic


class FeedItem(BaseModel):
    """Модель описывает поля элемента ленты(Feed)"""
    row_number: Optional[int]
    event_timestamp: Optional[datetime]


class CleaningFeedItem(CleaningPublic, FeedItem):
    """Модель описывает поля элемент услуги"""
    event_type: Optional[Literal["is_create", "is_update"]]
