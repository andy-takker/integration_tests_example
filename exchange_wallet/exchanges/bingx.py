import hashlib
import hmac
import time
import urllib
from collections.abc import Sequence
from decimal import Decimal
from http import HTTPStatus
from typing import Any

import httpx
from pydantic import BaseModel

from exchange_wallet.entities.balance import AssetBalance


class BingxClient:
    def __init__(
        self,
        client: httpx.AsyncClient,
        api_key: str,
        api_secret: str,
    ):
        self._api_key = api_key
        self._api_secret = api_secret
        self._client = client
        self._url = "https://open-api.bingx.com/openApi"

    async def get_account_asset_balances(self) -> Sequence[AssetBalance]:
        params = self._default_params()
        params["signature"] = self.get_sign(params)
        response = await self._client.get(
            f"{self._url}/spot/v1/account/balance",
            params=params,
            headers=self._default_headers(),
        )
        if response.status_code != HTTPStatus.OK:
            raise ValueError("Failed to get account info")
        bingx_account = BingxAccountResponse.model_validate_json(response.text)
        return [
            AssetBalance(
                asset=asset_balance.asset,
                balance=asset_balance.free,
            )
            for asset_balance in bingx_account.data.balances
        ]

    async def get_last_symbol_price(self, symbol: str) -> Decimal:
        response = await self._client.get(
            f"{self._url}/spot/v1/ticker/price",
            params={"symbol": symbol},
        )
        if response.status_code != HTTPStatus.OK:
            raise ValueError("Failed to get last symbol price")
        return Decimal(response.json()["data"][0]["trades"][0]["price"])

    def _default_params(self) -> dict[str, Any]:
        return {
            "recvWindow": "6000",
            "timestamp": str(int(time.time() * 1000)),
        }

    def _default_headers(self) -> dict[str, Any]:
        return {
            "X-BX-APIKEY": self._api_key,
        }

    def get_sign(self, params: dict[str, Any]) -> str:
        query_string = urllib.parse.urlencode(params)
        return hmac.new(
            self._api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()


class BingxAssetBalanceResponse(BaseModel):
    asset: str
    free: Decimal


class BingxAccountBalancesResponse(BaseModel):
    balances: Sequence[BingxAssetBalanceResponse]


class BingxAccountResponse(BaseModel):
    data: BingxAccountBalancesResponse
