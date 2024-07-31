from typing import Optional

from app.db.repositories.base import BaseRepository
from app.models.profile import ProfileCreate, ProfileInDB, ProfileUpdate
from app.models.users import UserPublic

CREATE_PROFILE_FOR_USER_QUERY = """
    INSERT INTO profiles(full_name, phone_number, bio, image, user_id)
    VALUES (:full_name, :phone_number, :bio, :image, :user_id)
    RETURNING id, full_name, phone_number, bio, image, user_id, created_at, updated_at;
"""

GET_PROFILE_BY_USER_ID_QUERY = """
    SELECT id, full_name, phone_number, bio, image, user_id, created_at, updated_at
    FROM profiles
    WHERE user_id = :user_id;
"""

GET_PROFILE_BY_USERNAME_QUERY = """
    SELECT 
        p.id, p.full_name, p.phone_number, p.bio, p.image, p.user_id, p.created_at, p.updated_at,
        u.username, u.email
    FROM profiles AS p
    INNER JOIN users AS u ON p.user_id = u.id
    WHERE user_id = (SELECT id FROM users WHERE username = :username);
"""

UPDATE_PROFILE_QUERY = """
    UPDATE profiles
    SET full_name = :full_name,
        phone_number = :phone_number,
        bio = :bio,
        image = :image
    WHERE user_id = :user_id
    RETURNING id, full_name, phone_number, bio, image, user_id, created_at, updated_at;
"""


class ProfilesRepository(BaseRepository):
    async def create_profile_for_user(self, *, profile_create: ProfileCreate) -> ProfileInDB:
        """Делает sql запрос на создание профиля для зарегистрированного пользователя"""
        created_profile = await self.db.fetch_one(query=CREATE_PROFILE_FOR_USER_QUERY, values=profile_create.dict())
        return created_profile

    async def get_profile_by_user_id(self, *, user_id: int) -> Optional[ProfileInDB]:
        """Делает sql запрос по указанному в аргументе user_id опционально возвращает профиль пользователя"""
        profile_record = await self.db.fetch_one(query=GET_PROFILE_BY_USER_ID_QUERY, values={"user_id": user_id})

        if not profile_record:
            return None
        return ProfileInDB(**profile_record)

    async def get_profile_by_username(self, *, username: str) -> Optional[ProfileInDB]:
        profile_record = await self.db.fetch_one(query=GET_PROFILE_BY_USERNAME_QUERY, values={"username": username})
        if profile_record:
            return ProfileInDB(**profile_record)

    async def update_profile(
            self, *,
            profile_update: ProfileUpdate,
            current_user: UserPublic
    ) -> Optional[ProfileInDB]:
        profile = await self.get_profile_by_user_id(user_id=current_user.id)
        update_params = profile.copy(update=profile_update.dict(exclude_unset=True))
        updated_profile = await self.db.fetch_one(
            query=UPDATE_PROFILE_QUERY,
            values=update_params.dict(exclude={"id", "created_at", "updated_at", "username", "email"})
        )
        return ProfileInDB(**updated_profile)
