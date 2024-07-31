from __future__ import annotations
from typing import Optional, Union, List
from enum import Enum

from pydantic import Field

from app.models.core import IDModelMixin, CoreModel, DateTimeModelMixin
from app.models.users import UserPublic


class CleaningType(str, Enum):
    dust_up = "dust_up"
    spot_clean = "spot_clean"
    full_clean = "full_clean"


class CleaningBase(CoreModel):
    """
    Модель содержащая все поля нашей услуги
    """
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    cleaning_type: Optional[CleaningType] = "spot_clean"
    total_offers: int = Field(default=0)


class CleaningCreate(CleaningBase):
    name: str
    price: float


class CleaningUpdate(CleaningBase):
    cleaning_type: Optional[CleaningType] = None


class CleaningInDB(IDModelMixin, DateTimeModelMixin, CleaningBase):
    name: str
    price: float
    cleaning_type: CleaningType
    owner: int


class CleaningPublic(CleaningInDB):
    owner: Union[int, UserPublic]


# class ServicePageDetail(CleaningInDB):
#     owner: Union[int, UserPublic]
#     total_offers: Optional[int]
#     offers: List[OfferPublic]
#
#
# from app.models.offer import OfferPublic
#
# CleaningPublic.update_forward_refs()