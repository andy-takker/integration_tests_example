from collections.abc import AsyncIterator

import httpx
from dishka import Provider, Scope, provide

from exchange_wallet.config import BingxConfig
from exchange_wallet.exchanges.bingx import BingxClient
from exchange_wallet.wallet_calculator import WalletCalculator


class ExchangeProvider(Provider):
    scope = Scope.APP

    @provide()
    async def httpx_client(self) -> AsyncIterator[httpx.AsyncClient]:
        async with httpx.AsyncClient() as client:
            yield client

    @provide()
    def bingx_client(
        self,
        httpx_client: httpx.AsyncClient,
        bingx_config: BingxConfig,
    ) -> BingxClient:
        return BingxClient(
            client=httpx_client,
            api_key=bingx_config.api_key,
            api_secret=bingx_config.api_secret,
        )

    @provide()
    def wallet_calculator(self, bingx_client: BingxClient) -> WalletCalculator:
        return WalletCalculator(bingx_client=bingx_client)
