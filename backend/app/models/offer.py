from typing import Optional, List
from enum import Enum
from pydantic import BaseModel
from uuid import uuid4

from pydantic import Field

from app.models.users import UserPublic
from app.models.cleaning import CleaningPublic
from app.models.core import CoreModel, DateTimeModelMixin


class OfferStatus(Enum):
    completed = "completed"
    accepted = "accepted"
    rejected = "rejected"
    pending = "pending"
    cancelled = "cancelled"


class OfferBase(CoreModel):
    """Схема содержит базовые поля описывающие заказ"""
    uid: Optional[str] = None
    user_id: Optional[int]
    cleaning_id: Optional[int]
    status: Optional[OfferStatus] = OfferStatus.pending.value


class OfferCreate(CoreModel):
    """Схема содержит поля необходимые для создания заказа"""
    user_id: int
    cleaning_id: int
    uid: str = Field(default_factory=lambda: uuid4().hex)


class OfferUpdate(CoreModel):
    """Схема содержит поля необходимые для обновления заказа"""
    status: OfferStatus


class OfferInDB(DateTimeModelMixin, OfferBase):
    """Схема содержит поля заказа для валидации вывода из базы данных"""
    user_id: int
    cleaning_id: int


class OfferPublic(OfferInDB):
    """Схема содержит поля заказа для вывода пользователю"""
    user: Optional[UserPublic]
    cleaning: Optional[CleaningPublic]


class OfferDetailsPublic(DateTimeModelMixin, CoreModel):
    executor: Optional[UserPublic]
    status: OfferStatus


class CleaningOffersListPublic(BaseModel):
    """
    Схема содержит поля необходимые для страницы просмотра детального списка заказов на услугу
    """
    cleaning: Optional[CleaningPublic]
    offers: Optional[List[OfferDetailsPublic]]
    total_offers: Optional[int]


class OfferListPublic(OfferInDB):
    """Схема: содержит поля списка заказов на конкретную услугу"""
    cleaning: CleaningPublic
    total_offers: Optional[int]
    offers: List[OfferPublic]
