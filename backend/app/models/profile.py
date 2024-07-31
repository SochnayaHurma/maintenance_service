from typing import Optional
from pydantic import HttpUrl, EmailStr

from app.models.core import CoreModel, IDModelMixin, DateTimeModelMixin


class ProfileBase(CoreModel):
    """Содердит базовые атрибуты модели профиля пользователя"""
    full_name: Optional[str]
    phone_number: Optional[str]
    bio: Optional[str]
    image: Optional[HttpUrl]


class ProfileCreate(ProfileBase):
    """Содержит атрибуты необходимые для создания профиля"""
    user_id: int


class ProfileUpdate(ProfileBase):
    """Содержит атрибуты необходимые для обновления профиля"""


class ProfileInDB(DateTimeModelMixin, ProfileUpdate):
    """Содержит атрибуты для валидации вывода из базы данных"""
    user_id: Optional[int] = None
    username: Optional[str]
    email: Optional[EmailStr]


class ProfilePublic(ProfileInDB):
    """Содержит атрибуты для валидации вывода пользователю"""
    pass
