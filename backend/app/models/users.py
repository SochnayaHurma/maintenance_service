import string
from typing import Optional

from pydantic import EmailStr, constr, validator

from app.models.core import IDModelMixin, CoreModel, DateTimeModelMixin
from app.models.token import AccessToken
from app.models.profile import ProfilePublic


def validate_username(username: str) -> str:
    """
    Принимает строку и проверяет её на допустимую длинну
    и наличие допустимых символов ASCII DIGITS

    """
    allowed = string.ascii_letters + string.digits + "-" + "_"
    assert all(char in allowed for char in username), "Invalid characters in username"
    assert len(username) >= 3, "Username must be 3 character or more."
    return username


class UserBase(CoreModel):
    """
    Базовая модель отображающая все поля, которые будут доступны для взаимодействия
    """
    email: Optional[EmailStr]
    username: Optional[str]
    email_verified: bool = False
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(CoreModel):
    """
    Описаны поля, доступные при создании пользователя
    """
    email: EmailStr
    password: constr(min_length=7, max_length=60)
    username: str

    @validator("username", pre=True)
    def username_is_valid(cls, username: str) -> str:
        return validate_username(username)


class UserUpdate(CoreModel):
    """
    Описаны поля, доступные при обновлении пользователя
    """
    email: Optional[EmailStr]
    username: Optional[str]

    @validator("username", pre=True)
    def username_is_valid(cls, username: str) -> str:
        return validate_username(username)


class UserPasswordUpdate(CoreModel):
    """
    Модель описывающая поля необходимые при смене пароля пользователя
    """
    password: constr(min_length=7, max_length=60)
    salt: str


class UserInDB(IDModelMixin, DateTimeModelMixin, UserBase):
    """
    Модель описывает поля, возвращаемые базой данных
    """
    password: constr(min_length=7, max_length=60)
    salt: str


class UserPublic(IDModelMixin, DateTimeModelMixin, UserBase):
    """
    Модель описывает поля,для вывода пользователю
    """
    access_token: Optional[AccessToken]
    profile: Optional[ProfilePublic]
