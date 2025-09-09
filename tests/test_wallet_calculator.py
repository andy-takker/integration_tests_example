from collections.abc import Mapping, Sequence
from decimal import Decimal

import pytest

from exchange_wallet.entities.balance import AssetBalance
from exchange_wallet.wallet_calculator import WalletCalculator
from tests.plugins.stub_exchange_client import StubExchangeClient


@pytest.mark.parametrize(
    "account_asset_balances, last_symbol_prices, expected_total_asset_usd",
    [
        (
            [
                AssetBalance(asset="BTC", balance=Decimal("1.0")),
                AssetBalance(asset="ETH", balance=Decimal("2.0")),
                AssetBalance(asset="USDT", balance=Decimal("3.0")),
            ],
            {
                "BTC_USDT": Decimal("100.0"),
                "ETH_USDT": Decimal("200.0"),
            },
            Decimal("503.0"),
        ),
        (
            [
                AssetBalance(asset="USDT", balance=Decimal("31234.0")),
            ],
            {},
            Decimal("31234.0"),
        ),
    ],
)
async def test_wallet_calculator(
    account_asset_balances: Sequence[AssetBalance],
    last_symbol_prices: Mapping[str, Decimal],
    expected_total_asset_usd: Decimal,
):
    wallet_calculator = _get_wallet_calculator(
        account_asset_balances=account_asset_balances,
        last_symbol_prices=last_symbol_prices,
    )
    bingx_wallet = await wallet_calculator.get_bingx_wallet()
    assert bingx_wallet.total_asset_usd == expected_total_asset_usd


def _get_wallet_calculator(
    account_asset_balances: Sequence[AssetBalance],
    last_symbol_prices: Mapping[str, Decimal],
) -> WalletCalculator:
    stub_client = StubExchangeClient(
        account_asset_balances=account_asset_balances,
        last_symbol_prices=last_symbol_prices,
    )
    return WalletCalculator(bingx_client=stub_client)
