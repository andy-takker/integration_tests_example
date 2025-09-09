from decimal import Decimal

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from exchange_wallet.entities.balance import AccountBalance
from exchange_wallet.exchanges.bingx import BingxClient

router = APIRouter(
    prefix="/wallet",
    tags=["wallet"],
    route_class=DishkaRoute,
)


@router.get("/bingx")
async def get_bingx_wallet(
    bingx_client: FromDishka[BingxClient],
) -> AccountBalance:
    asset_balances = await bingx_client.get_account_asset_balances()
    total_asset_usd = Decimal(0)
    for asset_balance in asset_balances:
        if asset_balance.asset == "USDT":
            total_asset_usd += asset_balance.balance
            continue
        price = await bingx_client.get_last_symbol_price(f"{asset_balance.asset}_USDT")
        total_asset_usd += asset_balance.balance * price
    return AccountBalance(
        total_asset_usd=total_asset_usd,
        asset_balances=asset_balances,
    )
