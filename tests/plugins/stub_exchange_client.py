from collections.abc import Mapping, Sequence
from decimal import Decimal

from exchange_wallet.entities.balance import AssetBalance


class StubExchangeClient:
    def __init__(
        self,
        account_asset_balances: Sequence[AssetBalance],
        last_symbol_prices: Mapping[str, Decimal],
    ):
        self.account_asset_balances = account_asset_balances
        self.last_symbol_prices = last_symbol_prices

    async def get_account_asset_balances(self) -> Sequence[AssetBalance]:
        return self.account_asset_balances

    async def get_last_symbol_price(self, symbol: str) -> Decimal:
        return self.last_symbol_prices[symbol]
