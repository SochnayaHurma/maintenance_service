from app.models.offer import OfferDetailsPublic
from app.models.cleaning import CleaningPublic
from app.models.users import UserPublic
from app.models.profile import ProfilePublic

from collections import namedtuple
from typing import Union, List

from databases.backends.postgres import Record

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
        profiles.id AS profiles_id, profiles.full_name AS profiles_full_name, 
        profiles.phone_number AS profiles_phone_number, profiles.bio AS profiles_bio, 
        profiles.image AS profiles_image, profiles.user_id AS profiles_user_id, 
        profiles.created_at AS profiles_created_at, profiles.updated_at AS profiles_updated_at

    FROM cleanings
    INNER JOIN users ON cleanings.owner = users.id
    WHERE owner = :owner;
"""

CleaningDetail = namedtuple('CleaningDetail', ('cleaning', 'offer'))


def cleaning_converter(record) -> CleaningPublic:
    return CleaningPublic(
        id=record['cleaning_id'],
        name=record['cleaning_name'],
        description=record['cleaning_description'],
        price=record['cleaning_price'],
        cleaning_type=record['cleaning_type'],
        created_at=record['cleaning_created_at'],
        updated_at=record['cleaning_updated_at'],
        owner=UserPublic(
            id=record['users_owner_id'],
            email=record['users_owner_email'],
            username=record['users_owner_username'],
            is_active=record['users_owner_is_active'],
            is_superuser=record['users_owner_is_superuser'],
            created_at=record['users_owner_created_at'],
            updated_at=record['users_owner_updated_at'],
        )
    )


def offer_converter(record) -> OfferDetailsPublic:
    return OfferDetailsPublic(
        executor=UserPublic(
            id=record['users_id'],
            email=record['users_email'],
            username=record['users_username'],
            is_active=record['users_is_active'],
            is_superuser=record['users_is_superuser'],
            created_at=record['users_created_at'],
            updated_at=record['users_updated_at'],
            profile=ProfilePublic(
                full_name=record['profiles_full_name'],
                phone_number=record['profiles_phone_number'],
                bio=record['profiles_bio'],
                image=record['profiles_image'],
                created_at=record['profiles_created_at'],
                updated_at=record['profiles_updated_at']
            )
        ),
        status=record['offers_status'],
        created_at=record['offers_created_at'],
        updated_at=record['offers_updated_at']
    )


def converter(records: List[Record]):
    d = {}
    for record in records:
        if record['offers_status']:
            offer = offer_converter(record=record)
        else:
            offer = None

        if not d.get(record['cleaning_id']):
            cleaning = cleaning_converter(record=record)
            d[record['cleaning_id']] = CleaningDetail(cleaning, [])
        if offer:
            d[record['cleaning_id']].offer.append(offer)
    return d
