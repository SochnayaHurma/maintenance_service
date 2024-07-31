from fastapi import status, HTTPException, Depends, Path

from app.models.users import UserInDB
from app.api.dependencies.database import get_repository
from app.db.repositories.users import UsersRepository


async def get_user_by_username_from_path(
        username: str = Path(..., min_length=3, regex="[a-zA-Z0-9_-]+$"),
        user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserInDB:

    user = await user_repo.get_user_by_username(username=username, populate=False)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user found with that username. {}".format(username)
        )
    return user
