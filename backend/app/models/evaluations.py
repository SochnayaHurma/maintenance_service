from typing import Optional, Union
from pydantic import conint
from pydantic.types import confloat

from app.models.cleaning import CleaningPublic
from app.models.core import CoreModel, DateTimeModelMixin
from app.models.users import UserPublic


class EvaluationBase(CoreModel):
    """Модель содержит базовые поля для отзыва (Evaluation) """
    no_show: bool = False
    headline: Optional[str]
    comment: Optional[str]
    professionalism: Optional[conint(ge=0, le=5)]
    completeness: Optional[conint(ge=0, le=5)]
    efficiency: Optional[conint(ge=0, le=5)]
    overall_rating: Optional[conint(ge=0, le=5)]


class EvaluationCreated(EvaluationBase):
    """Модель содержит обязательные поля необходимые при создании отзыва (Evaluations)"""
    overall_rating: conint(ge=0, le=5)


class EvaluationUpdated(EvaluationBase):
    """Содержит поля необходимые для обнолвнеия отзыва"""
    pass


class EvaluationInDB(DateTimeModelMixin, EvaluationBase):
    """Модель содержит поля для валидации вывода из базы данных"""
    cleaning_id: int
    cleaner_id: int


class EvaluationPublic(EvaluationInDB):
    """Модель содержит поля для валидации вывода пользователю"""
    customer: Optional[Union[int, UserPublic]]
    cleaner: Optional[UserPublic]
    cleaning: Optional[CleaningPublic]


class EvaluationAggregate(CoreModel):
    """Модель содержит поля общей оценки услуги"""
    avg_professionalism: confloat(ge=0, le=5)
    avg_completeness: confloat(ge=0, le=5)
    avg_efficiency: confloat(ge=0, le=5)
    avg_overall_rating: confloat(ge=0, le=5)
    max_overall_rating: conint(ge=0, le=5)
    min_overall_rating: conint(ge=0, le=5)
    one_stars: conint(ge=0)
    two_stars: conint(ge=0)
    three_stars: conint(ge=0)
    four_stars: conint(ge=0)
    five_stars: conint(ge=0)
    total_evaluations: conint(ge=0)
    total_no_show: conint(ge=0)
