from pydantic import EmailStr
from datetime import datetime, timedelta

from app.models.core import CoreModel
from app.core.config import JWT_AUDIENCE, ACCESS_TOKEN_EXPIRE_MINUTES


class JWTMeta(CoreModel):
    """
    Содержит служебные поля описывающие jwt-token
    """
    iss: str = "phresh.io"
    aud: str = JWT_AUDIENCE
    iat: float = datetime.timestamp(datetime.utcnow())
    exp: float = datetime.timestamp(datetime.utcnow() - timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))


class JWTCred(CoreModel):
    """
    Содержит поля для идентицикации пользователя
    """
    sub: EmailStr
    username: str


class JWTPayload(JWTMeta, JWTCred):
    """
    Содержит поля, необходимые перед кодированием токена
    """
    ...


class AccessToken(CoreModel):
    """
    Содержит поля необходимые перед декодированием токена
    """
    access_token: str
    token_type: str
