import bcrypt
import jwt
from datetime import datetime
import datetime
from passlib.context import CryptContext
from typing import Optional
from fastapi import status
from fastapi.exceptions import ValidationError, HTTPException

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, JWT_AUDIENCE, SECRET_KEY
from app.models.users import UserPasswordUpdate, UserBase
from app.models.token import JWTMeta, JWTCred, JWTPayload, AccessToken

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


class AuthException(BaseException):
    """
    Custom auth exception
    """
    pass


class AuthService:
    @classmethod
    def create_salt_and_hashed_password(cls, plaintext_password: str) -> UserPasswordUpdate:
        """
        Метод генерирует хэш(salt) и хэширует указанную в аргументе строку(password)
        Возвращает объект pydantic из двух атрибутов (salt, password)
        """
        salt = cls.generate_salt()
        hashed_password = cls.hash_password(password=plaintext_password, salt=salt)
        return UserPasswordUpdate(salt=salt, password=hashed_password)

    @staticmethod
    def generate_salt() -> str:
        """Метод генерирует рандомный хэш"""
        return bcrypt.gensalt().decode()

    @staticmethod
    def hash_password(*, password: str, salt: str) -> str:
        """Метод возврвщает хэш версию указанной в аргументе строки"""
        return pwd_context.hash(password + salt)

    @staticmethod
    def verify_password(*, password: str, salt: str, hashed_pw: str) -> bool:
        """Метод валидирует хэш версию пароля, если пароли совпадут вернет true"""
        return pwd_context.verify(password + salt, hashed_pw)

    @staticmethod
    def create_access_token_for_user(
            *,
            user: UserBase,
            secret_key: str = str(SECRET_KEY),
            audience: str = JWT_AUDIENCE,
            expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES
    ) -> Optional[str]:
        """
        Метод кодирует jwt-token из указанных входных данных
        """
        if not user or not isinstance(user, UserBase):
            return None
        jwt_meta = JWTMeta(
            aud=audience,
            iat=datetime.datetime.timestamp(datetime.datetime.utcnow()),
            exp=datetime.datetime.timestamp(datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_in)),
        )
        jwt_cred = JWTCred(sub=user.email, username=user.username)
        jwt_payload = JWTPayload(
            **jwt_meta.dict(),
            **jwt_cred.dict()
        )
        access_token = jwt.encode(
            payload=jwt_payload.dict(),
            key=secret_key,
            algorithm=JWT_ALGORITHM
        )
        return access_token

    @staticmethod
    def get_username_from_token(*, token: str, secret_key: str = str(SECRET_KEY)) -> str:
        """
        Метод декодирует jwt-token и извлекает из него username
        """
        try:
            decoded_token = jwt.decode(token, str(secret_key), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM])
            payload = JWTPayload(**decoded_token)
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate token credentials.",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return payload.username
