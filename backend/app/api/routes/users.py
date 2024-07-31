from fastapi import Depends, APIRouter, Body, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException

from app.db.repositories.users import UsersRepository
from app.models.users import UserCreate, UserPublic, UserInDB
from app.models.token import AccessToken
from app.api.dependencies.database import get_repository
from app.api.dependencies.auth import get_current_active_user
from app.services.authentication import AuthService
from app.core.config import JWT_TOKEN_PREFIX

router = APIRouter()


@router.post(
    "/",
    response_model=UserPublic,
    name="users:register-new-user",
    status_code=status.HTTP_201_CREATED
)
async def register_new_user(
        new_user: UserCreate = Body(..., embed=True),
        user_repo: UsersRepository = Depends(get_repository(UsersRepository))
) -> UserPublic:
    created_user = await user_repo.register_new_user(new_user=new_user)
    access_token = AccessToken(
        access_token=AuthService.create_access_token_for_user(user=created_user),
        token_type=JWT_TOKEN_PREFIX
    )
    return created_user.copy(update={"access_token": access_token})


@router.post(
    "/login/token/",
    response_model=AccessToken,
    name="users:login-email-and-password",
)
async def user_login_with_email_and_password(
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> AccessToken:
    user = await user_repo.authenticate_user(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bad credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return AccessToken(
        access_token=AuthService.create_access_token_for_user(user=user),
        token_type=JWT_TOKEN_PREFIX
    )


@router.get(
    "/me/",
    response_model=UserPublic,
    name="users:get-current-user"
)
async def get_currently_authenticated_user(current_user: UserInDB = Depends(get_current_active_user)) -> UserPublic:
    """Эндпойнт отдает данные текущего пользователя (если он имеет валидный токен в заголовке)"""
    return current_user