from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from exchange_wallet.config import BingxConfig, Config
from exchange_wallet.exchanges.di import ExchangeProvider
from exchange_wallet.routers.api.router import router as api_router


def build_app(config: Config) -> FastAPI:
    container = make_async_container(
        ExchangeProvider(),
        context={
            BingxConfig: config.bingx,
        },
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        yield
        await container.close()

    app = FastAPI(
        title=config.http.title,
        description=config.http.description,
        version=config.http.version,
        docs_url="/docs/swagger",
        lifespan=lifespan,
    )
    app.include_router(api_router)

    setup_dishka(container=container, app=app)
    return app
