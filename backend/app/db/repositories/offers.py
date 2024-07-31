from typing import List, Optional, Union
from databases import Database

from app.db.repositories.base import BaseRepository
from app.db.repositories.users import UsersRepository
from app.models.cleaning import CleaningInDB
from app.models.offer import OfferStatus, OfferCreate, OfferPublic, OfferDetailsPublic, OfferInDB, CleaningOffersListPublic
from app.models.users import UserInDB, UserPublic
from app.models.profile import ProfilePublic

CREATE_OFFER_FOR_CLEANING_QUERY = """
    INSERT INTO user_offers_for_cleanings(uid, cleaning_id, user_id, status)
    VALUES (:uid, :cleaning_id, :user_id, :status)
    RETURNING uid, cleaning_id, user_id, status, created_at, updated_at
"""

LIST_OFFERS_FOR_CLEANING_QUERY = """
    SELECT uid, user_id, cleaning_id, status, created_at, updated_at
    FROM user_offers_for_cleanings
    WHERE cleaning_id = :cleaning_id;
"""

LIST_OFFERS_FOR_CLEANING_QUERY_AND_JOIN_USER = """
    SELECT uid, user_id, cleaning_id, status, created_at, updated_at
    FROM user_offers_for_cleanings
    WHERE cleaning_id = :cleaning_id;
"""

GET_OFFER_FOR_CLEANING_QUERY = """
    SELECT uid, user_id, cleaning_id, status, created_at, updated_at
    FROM user_offers_for_cleanings
    WHERE user_id = :user_id AND cleaning_id = :cleaning_id;
"""

GET_OFFER_FOR_CLEANING_QUERY_EXCLUDE_COMPLETED = """
    SELECT uid, user_id, cleaning_id, status, created_at, updated_at
    FROM user_offers_for_cleanings
    WHERE user_id = :user_id AND cleaning_id = :cleaning_id AND status != 'completed';
"""

UPDATE_OFFER_QUERY = """
    UPDATE user_offers_for_cleanings
    SET status = :status
    WHERE cleaning_id = :cleaning_id AND uid = :uid
    RETURNING uid, user_id, cleaning_id, status, created_at, updated_at;
"""

REJECTED_ALL_OTHER_QUERY = """
    UPDATE user_offers_for_cleanings
    SET status = :rejected
    WHERE cleaning_id = :cleaning_id 
        AND user_id != :user_id
        AND status = :pending;
"""

SET_ALL_OTHER_OFFERS_AS_STATUS_QUERY = """
    UPDATE user_offers_for_cleanings
    SET status = :status
    WHERE cleaning_id = :cleaning_id
        AND user_id != :user_id
        AND status = :with_status;
"""

RESCIND_OFFER_QUERY = """
    DELETE FROM user_offers_for_cleanings
    WHERE cleaning_id = :cleaning_id
        AND user_id = :user_id;
"""

MARK_OFFER_COMPLETED_QUERY = """
    UPDATE user_offers_for_cleanings
    SET status = :status
    WHERE cleaning_id = :cleaning_id
        AND user_id = :user_id
    RETURNING uid, user_id, cleaning_id, status, created_at, updated_at;
"""

GET_CLEANING_AND_HIM_OFFERS = """
    SELECT 
        user_offers_for_cleanings.uid AS offers_uid,
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


class OffersRepository(BaseRepository):
    """Содержит методы для взаимодействия с таблицей заказов в базе данных"""

    def __init__(self, db: Database) -> None:
        super().__init__(db)
        self.users_repo = UsersRepository(db)

    async def my_method(self, cleaning):
        offer_records = await self.db.fetch_all(
            query=GET_CLEANING_AND_HIM_OFFERS,
            values={"cleaning_id": cleaning.id}
        )
        if not offer_records:
            return None
        offers = [OfferDetailsPublic(
                    executor=UserPublic(
                        id=offer['users_id'],
                        email=offer['users_email'],
                        username=offer['users_username'],
                        is_active=offer['users_is_active'],
                        is_superuser=offer['users_is_superuser'],
                        created_at=offer['users_created_at'],
                        updated_at=offer['users_updated_at'],
                        profile=ProfilePublic(
                            full_name=offer['profiles_full_name'],
                            phone_number=offer['profiles_phone_number'],
                            bio=offer['profiles_bio'],
                            image=offer['profiles_image'],
                            created_at=offer['profiles_created_at'],
                            updated_at=offer['profiles_updated_at']
                        )
                    ),
                    status=offer['offers_status'],
                    created_at=offer['offers_created_at'],
                    updated_at=offer['offers_updated_at']
            ) for offer in offer_records]

        return CleaningOffersListPublic(cleaning=cleaning, offers=offers)

    async def get_offer_for_cleaning_from_user(self, *,
                                               cleaning: CleaningInDB,
                                               user: UserInDB,
                                               exclude_complete: bool = False) -> OfferPublic:
        if exclude_complete:
            offer = await self.db.fetch_one(
                query=GET_OFFER_FOR_CLEANING_QUERY_EXCLUDE_COMPLETED, values={"cleaning_id": cleaning.id, "user_id": user.id}
            )
        else:
            offer = await self.db.fetch_one(
                query=GET_OFFER_FOR_CLEANING_QUERY, values={"cleaning_id": cleaning.id, "user_id": user.id}
            )
        if not offer:
            return
        return OfferPublic(**offer)

    async def list_offers_for_cleaning(self, *,
                                       cleaning: CleaningInDB,
                                       populate: bool = False
                                       ):
        if populate:
            return await self.my_method(cleaning)
        else:
            offer_records = await self.db.fetch_all(
                query=LIST_OFFERS_FOR_CLEANING_QUERY, values={"cleaning_id": cleaning.id}
            )
            offers = [OfferPublic(**offer) for offer in offer_records]

            return offers

    async def create_offer_for_cleaning(self, *, new_offer: OfferCreate) -> OfferInDB:
        created_offer = await self.db.fetch_one(
            query=CREATE_OFFER_FOR_CLEANING_QUERY,
            values={**new_offer.dict(), "status": OfferStatus.pending.value},
        )
        return OfferInDB(**created_offer)

    async def accept_offer(self, *, offer: OfferInDB) -> OfferPublic:
        async with self.db.transaction():
            accepted_offer = await self.db.fetch_one(
                query=UPDATE_OFFER_QUERY,
                values={
                    "status": OfferStatus.accepted.value,
                    "uid": offer.uid,
                    "cleaning_id": offer.cleaning_id,
                }
            )
            await self.db.execute(
                query=REJECTED_ALL_OTHER_QUERY,
                values={"cleaning_id": offer.cleaning_id, "user_id": offer.user_id,
                        "rejected": OfferStatus.rejected.value, "pending": OfferStatus.pending.value}
            )
            return OfferInDB(**accepted_offer)

    async def cancel_offer(self, *, offer: OfferInDB) -> OfferPublic:
        async with self.db.transaction():
            updated_offer = await self.db.fetch_one(
                query=UPDATE_OFFER_QUERY,
                values={
                    "uid": offer.uid,
                    "cleaning_id": offer.cleaning_id,
                    "status": OfferStatus.cancelled.value,
                }
            )
            await self.db.execute(
                query=SET_ALL_OTHER_OFFERS_AS_STATUS_QUERY,
                values={
                    "user_id": offer.user_id,
                    "cleaning_id": offer.cleaning_id,
                    "status": OfferStatus.pending.value,
                    "with_status": OfferStatus.rejected.value
                }
            )
            return OfferPublic(**updated_offer)

    async def complete_offer(self, *, offer: OfferInDB) -> OfferPublic:
        async with self.db.transaction():
            updated_offer = await self.db.fetch_one(
                query=UPDATE_OFFER_QUERY,
                values={"uid": offer.uid, "cleaning_id": offer.cleaning_id, "status": OfferStatus.completed.value}
            )
            await self.db.execute(
                query=SET_ALL_OTHER_OFFERS_AS_STATUS_QUERY,
                values={
                    "user_id": offer.user_id,
                    "cleaning_id": offer.cleaning_id,
                    "status": OfferStatus.pending.value,
                    "with_status": OfferStatus.rejected.value
                }
            )
            return OfferPublic(**updated_offer)

    async def rescind_offer(self, *, offer: OfferInDB) -> int:
        return await self.db.execute(
            query=RESCIND_OFFER_QUERY,
            values={"cleaning_id": offer.cleaning_id, "user_id": offer.user_id}
        )

    async def mark_offer_completed(self, *, cleaning: CleaningInDB, cleaner: UserInDB) -> OfferInDB:
        offer = await self.db.fetch_one(
            query=MARK_OFFER_COMPLETED_QUERY,
            values={"status": OfferStatus.completed.value, "cleaning_id": cleaning.id, "user_id": cleaner.id},
        )
        return OfferInDB(**offer)

    async def populate_offer(self, *, offer: OfferInDB) -> OfferPublic:
        return OfferPublic(
            **offer.dict(exclude={"user"}),
            user=await self.users_repo.get_user_by_id(user_id=offer.user_id)
        )
