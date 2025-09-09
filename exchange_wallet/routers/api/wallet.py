from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from exchange_wallet.entities.balance import AccountBalance
from exchange_wallet.wallet_calculator import WalletCalculator

router = APIRouter(
    prefix="/wallet",
    tags=["wallet"],
    route_class=DishkaRoute,
)


@router.get("/bingx")
async def get_bingx_wallet(
    wallet_calculator: FromDishka[WalletCalculator],
) -> AccountBalance:
    return await wallet_calculator.get_bingx_wallet()
