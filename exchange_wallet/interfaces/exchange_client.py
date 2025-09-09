from collections.abc import Sequence
from decimal import Decimal
from typing import Protocol

from exchange_wallet.entities.balance import AssetBalance


class IExchangeClient(Protocol):
    async def get_account_asset_balances(self) -> Sequence[AssetBalance]: ...
    async def get_last_symbol_price(self, symbol: str) -> Decimal: ...
