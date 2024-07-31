from fastapi import APIRouter

from app.api.routes.cleanings import router as cleaning_router
from app.api.routes.users import router as user_router
from app.api.routes.profiles import router as profile_router
from app.api.routes.offers import router as offer_router
from app.api.routes.evaluations import router as evaluation_router
from app.api.routes.feed import router as feed_router

router = APIRouter()

router.include_router(
    cleaning_router,
    prefix="/cleanings",
    tags=["cleanings"]
)
router.include_router(
    user_router,
    prefix="/users",
    tags=["users"]
)
router.include_router(
    profile_router,
    prefix="/profile",
    tags=["profile"]
)
router.include_router(
    offer_router,
    prefix="/cleanings/{cleaning_id}/offer",
    tags=["offers"]
)
router.include_router(
    evaluation_router,
    prefix="/users/{username}/evaluations",
    tags=["evaluations"]
)
router.include_router(
    feed_router,
    prefix="/feed",
    tags=["feed"]
)
