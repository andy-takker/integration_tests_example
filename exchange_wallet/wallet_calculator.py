from decimal import Decimal
from typing import Final

from exchange_wallet.entities.balance import AccountBalance
from exchange_wallet.interfaces.exchange_client import IExchangeClient

BASE_ASSET: Final = "USDT"


class WalletCalculator:
    def __init__(self, bingx_client: IExchangeClient):
        self._bingx_client = bingx_client

    async def get_bingx_wallet(self) -> AccountBalance:
        asset_balances = await self._bingx_client.get_account_asset_balances()
        total_asset_usd = Decimal(0)
        for asset_balance in asset_balances:
            if asset_balance.asset == BASE_ASSET:
                total_asset_usd += asset_balance.balance
                continue
            price = await self._bingx_client.get_last_symbol_price(
                f"{asset_balance.asset}_{BASE_ASSET}"
            )
            total_asset_usd += asset_balance.balance * price
        return AccountBalance(
            total_asset_usd=total_asset_usd,
            asset_balances=asset_balances,
        )
