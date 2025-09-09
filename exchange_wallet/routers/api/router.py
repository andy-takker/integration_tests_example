from fastapi import APIRouter

from exchange_wallet.routers.api.ping import router as ping_router
from exchange_wallet.routers.api.wallet import router as wallet_router

router = APIRouter(
    prefix="/api",
)
router.include_router(ping_router)
router.include_router(wallet_router)
