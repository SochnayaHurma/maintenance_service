from pydantic import BaseModel, validator

from typing import Optional
from datetime import datetime


class CoreModel(BaseModel):
    """ Содержит общую логику всех моделей """
    pass


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime):
        return value or datetime.now()


class IDModelMixin(BaseModel):
    id: int
    