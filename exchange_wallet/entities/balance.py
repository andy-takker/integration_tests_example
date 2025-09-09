from collections.abc import Sequence
from decimal import Decimal

from pydantic import BaseModel


class AssetBalance(BaseModel):
    asset: str
    balance: Decimal


class AccountBalance(BaseModel):
    total_asset_usd: Decimal
    asset_balances: Sequence[AssetBalance]
