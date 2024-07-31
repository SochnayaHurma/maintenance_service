from app.db.repositories.base import BaseRepository
from app.db.repositories.users import UsersRepository
from app.models.cleaning import CleaningCreate, CleaningUpdate, CleaningInDB, CleaningPublic
from app.models.offer import CleaningOffersListPublic
from app.db.repositories.converter import (
    converter as cleaning_get_all_converter,
)

from typing import Optional, List, Union

from fastapi import status
from fastapi.exceptions import HTTPException
from databases import Database

from app.models.users import UserInDB

CREATE_CLEANING_QUERY = """
    INSERT INTO cleanings(name, description, price, cleaning_type, owner)
    VALUES (:name, :description, :price, :cleaning_type, :owner)
    RETURNING id, name, description, price, cleaning_type, owner, created_at, updated_at;
"""

GET_CLEANING_QUERY = """
    SELECT id, name, description, price, cleaning_type, owner, created_at, updated_at
    FROM cleanings
    WHERE id = :id;
"""

GET_CLEANING_JOINED_OWNER_USER_QUERY3 = """
    SELECT 
        cleanings.id AS cleaning_id, cleanings.name AS cleaning_name,
        cleanings.description AS cleaning_description, 
        cleanings.price AS cleaning_price, cleanings.cleaning_type AS cleaning_type, 
        cleanings.owner AS cleaning_owner, 
        cleanings.created_at AS cleaning_created_at, cleanings.updated_at AS cleaning_updated_at,
        users.id AS users_id, users.username AS users_username, 
        users.email AS users_email, users.email_verified AS users_email_verified,
        users.password AS users_password, users.salt AS users_salt, 
        users.is_active AS users_is_active, users.is_superuser AS users_is_superuser, 
        users.created_at AS users_created_at, users.updated_at AS users_updated_at
    FROM cleanings
    INNER JOIN users ON cleanings.owner = users.id
    WHERE cleanings.id = :id;
"""

GET_ALL_CLEANING_QUERY = """
    SELECT id, name, description, price, cleaning_type, owner, created_at, updated_at
    FROM cleanings
    WHERE owner = :owner;
"""

GET_CLEANING_AND_HIM_OFFERS2 = """
    SELECT 
        user_offers_for_cleanings.status AS offers_status,
        user_offers_for_cleanings.created_at AS offers_created_at,
        user_offers_for_cleanings.updated_at AS offers_updated_at,
        users.id AS users_id, users.username AS users_username, 
        users.email AS users_email, users.email_verified AS users_email_verified,
        users.password AS users_password, users.salt AS users_salt, 
        users.is_active AS users_is_active, users.is_superuser AS users_is_superuser, 
        users.created_at AS users_created_at, users.updated_at AS users_updated_at,
        profiles.id AS profiles_id, profiles.full_name AS profiles_full_name, 
        profiles.phone_number AS profiles_phone_number, profiles.bio AS profiles_bio, 
        profiles.image AS profiles_image, profiles.user_id AS profiles_user_id, 
        profiles.created_at AS profiles_created_at, profiles.updated_at AS profiles_updated_at
    FROM user_offers_for_cleanings
    INNER JOIN users ON user_offers_for_cleanings.user_id = users.id
    INNER JOIN profiles ON profiles.user_id = users.id
    WHERE user_offers_for_cleanings.cleaning_id = :cleaning_id;
"""

GET_CLEANING_JOINED_OWNER_USER_QUERY = """
    SELECT 
            cleanings.id AS cleaning_id, cleanings.name AS cleaning_name,
            cleanings.description AS cleaning_description, 
            cleanings.price AS cleaning_price, cleanings.cleaning_type AS cleaning_type, 
            cleanings.owner AS cleaning_owner, 
            cleanings.created_at AS cleaning_created_at, cleanings.updated_at AS cleaning_updated_at,
            users_owner.id AS users_owner_id, users_owner.username AS users_owner_username, 
            users_owner.email AS users_owner_email, users_owner.email_verified AS users_owner_email_verified,
            users_owner.is_active AS users_owner_is_active, users_owner.is_superuser AS users_owner_is_superuser, 
            users_owner.created_at AS users_owner_created_at, users_owner.updated_at AS users_owner_updated_at,
            offer.status AS offers_status, offer.created_at AS offers_created_at,
            offer.updated_at AS offers_updated_at,
            users_offer.id AS users_id, users_offer.username AS users_username, 
            users_offer.email AS users_email, users_offer.email_verified AS users_email_verified,
            users_offer.is_active AS users_is_active, users_offer.is_superuser AS users_is_superuser, 
            users_offer.created_at AS users_created_at, users_offer.updated_at AS users_updated_at,
            profiles_offer.id AS profiles_id, profiles_offer.full_name AS profiles_full_name, 
            profiles_offer.phone_number AS profiles_phone_number, profiles_offer.bio AS profiles_bio, 
            profiles_offer.image AS profiles_image, profiles_offer.user_id AS profiles_user_id, 
            profiles_offer.created_at AS profiles_created_at, profiles_offer.updated_at AS profiles_updated_at
    FROM cleanings
    LEFT JOIN users AS "users_owner" ON cleanings.owner = users_owner.id
    LEFT JOIN user_offers_for_cleanings AS "offer" ON offer.cleaning_id = cleanings.id
    LEFT JOIN users AS "users_offer" ON users_offer.id = offer.user_id
    LEFT JOIN profiles AS "profiles_offer" ON users_offer.id = profiles_offer.user_id
    WHERE cleanings.id = :cleaning_id;
"""
GET_ALL_CLEANING_JOINED_OWNER_USER_QUERY = """
    SELECT 
            cleanings.id AS cleaning_id, cleanings.name AS cleaning_name,
            cleanings.description AS cleaning_description, 
            cleanings.price AS cleaning_price, cleanings.cleaning_type AS cleaning_type, 
            cleanings.owner AS cleaning_owner, 
            cleanings.created_at AS cleaning_created_at, cleanings.updated_at AS cleaning_updated_at,
            users_owner.id AS users_owner_id, users_owner.username AS users_owner_username, 
            users_owner.email AS users_owner_email, users_owner.email_verified AS users_owner_email_verified,
            users_owner.is_active AS users_owner_is_active, users_owner.is_superuser AS users_owner_is_superuser, 
            users_owner.created_at AS users_owner_created_at, users_owner.updated_at AS users_owner_updated_at,
            offer.status AS offers_status, offer.created_at AS offers_created_at,
            offer.updated_at AS offers_updated_at,
            users_offer.id AS users_id, users_offer.username AS users_username, 
            users_offer.email AS users_email, users_offer.email_verified AS users_email_verified,
            users_offer.is_active AS users_is_active, users_offer.is_superuser AS users_is_superuser, 
            users_offer.created_at AS users_created_at, users_offer.updated_at AS users_updated_at,
            profiles_offer.id AS profiles_id, profiles_offer.full_name AS profiles_full_name, 
            profiles_offer.phone_number AS profiles_phone_number, profiles_offer.bio AS profiles_bio, 
            profiles_offer.image AS profiles_image, profiles_offer.user_id AS profiles_user_id, 
            profiles_offer.created_at AS profiles_created_at, profiles_offer.updated_at AS profiles_updated_at
    FROM cleanings
    LEFT JOIN users AS "users_owner" ON cleanings.owner = users_owner.id
    LEFT JOIN user_offers_for_cleanings AS "offer" ON offer.cleaning_id = cleanings.id
    LEFT JOIN users AS "users_offer" ON users_offer.id = offer.user_id
    LEFT JOIN profiles AS "profiles_offer" ON users_offer.id = profiles_offer.user_id
    WHERE cleanings.owner = :owner;
"""


UPDATE_CLEANING_BY_ID_QUERY = """
    UPDATE cleanings
    SET name = :name,
        description = :description,
        price = :price,
        cleaning_type = :cleaning_type
    WHERE id = :id
    RETURNING id, name, description, price, cleaning_type, owner, created_at, updated_at;
"""


DELETE_CLEANING_BY_ID_QUERY = """
    DELETE FROM cleanings
    WHERE id = :id
    RETURNING id; 
"""


class CleaningRepository(BaseRepository):
    """
    Содержите методы взаимодействия с моделью услуги очистки
    """

    def __init__(self, db: Database):
        super().__init__(db)
        self.users_repo = UsersRepository(db)

    async def get_all_cleanings(self, current_user: UserInDB, populate=False
                                ) -> Union[List[CleaningInDB], List[CleaningOffersListPublic]]:
        if populate:
            cleanings_records = await self.db.fetch_all(
                query=GET_ALL_CLEANING_JOINED_OWNER_USER_QUERY,
                values={"owner": current_user.id}
            )
            if not cleanings_records:
                return []
            converted_record = cleaning_get_all_converter(cleanings_records)
            return [
                CleaningOffersListPublic(cleaning=v.cleaning, offers=v.offer, total_offers=len(v.offer))
                for _, v in converted_record.items()
            ]
        else:
            cleanings_records = await self.db.fetch_all(
                query=GET_ALL_CLEANING_QUERY,
                values={"owner": current_user.id}
        )
            if not cleanings_records:
                return None
            return [CleaningInDB(**clean) for clean in cleanings_records]

    async def get_cleaning_by_id(self, *,
                                 cleaning_id: int,
                                 current_user: UserInDB, populate: bool = False
                                 ) -> Union[CleaningInDB, CleaningPublic, CleaningOffersListPublic]:
        if populate:
            cleaning_record = await self.db.fetch_all(
                query=GET_CLEANING_JOINED_OWNER_USER_QUERY,
                values={"cleaning_id": cleaning_id}
            )
            if not cleaning_record:
                return None
            converted_data = cleaning_get_all_converter(cleaning_record)[cleaning_id]
            return CleaningOffersListPublic(cleaning=converted_data.cleaning,
                                            offers=converted_data.offer,
                                            total_offers=len(converted_data.offer))
        else:
            cleaning_record = await self.db.fetch_one(
                query=GET_CLEANING_QUERY,
                values={"id": cleaning_id}
            )
            if not cleaning_record:
                return None
            return CleaningInDB(**cleaning_record)

    async def create_cleaning(self, *, new_cleaning: CleaningCreate, current_user: UserInDB) -> CleaningPublic:
        cleaning = await self.db.fetch_one(
            query=CREATE_CLEANING_QUERY,
            values={
                "name": new_cleaning.name,
                "description": new_cleaning.description,
                "price": new_cleaning.price,
                "cleaning_type": new_cleaning.cleaning_type,
                "owner": current_user.id
            }
        )
        return CleaningPublic(**cleaning)

    async def update_cleaning(
            self,
            *,
            cleaning: CleaningInDB,
            cleaning_update: CleaningUpdate,
            current_user: UserInDB
    ) -> Optional[CleaningPublic]:
        cleaning_update_params = cleaning.copy(
            update=cleaning_update.dict(exclude_unset=True)
        )
        if cleaning_update_params.cleaning_type is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid cleaning type. Cannot be None."
            )

        updated_cleaning = await self.db.fetch_one(
            query=UPDATE_CLEANING_BY_ID_QUERY,
            values={
                "id": cleaning_update_params.id,
                "name": cleaning_update_params.name,
                "description": cleaning_update_params.description,
                "price": cleaning_update_params.price,
                "cleaning_type": cleaning_update_params.cleaning_type
            }
        )
        return CleaningPublic(**updated_cleaning)

    async def delete_cleaning_by_id(self, *, cleaning: CleaningInDB) -> int:
        deleted_id = await self.db.execute(
            query=DELETE_CLEANING_BY_ID_QUERY,
            values={"id": cleaning.id}
        )
        return deleted_id


