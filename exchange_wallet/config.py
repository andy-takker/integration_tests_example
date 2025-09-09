from dataclasses import dataclass, field
from os import environ


@dataclass(frozen=True, slots=True, kw_only=True)
class HTTPConfig:
    host: str = field(default_factory=lambda: environ.get("APP_SERVER_HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: int(environ.get("APP_SERVER_PORT", 8000)))
    title: str = field(
        default_factory=lambda: environ.get(
            "APP_SERVER_TITLE", "Exchange Wallet Example"
        )
    )
    description: str = field(
        default_factory=lambda: environ.get(
            "APP_SERVER_DESCRIPTION", "Exchange Wallet Example"
        )
    )
    version: str = field(
        default_factory=lambda: environ.get("APP_SERVER_VERSION", "0.0.0")
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class BingxConfig:
    api_key: str = field(default_factory=lambda: environ["APP_BINGX_API_KEY"])
    api_secret: str = field(default_factory=lambda: environ["APP_BINGX_API_SECRET"])


@dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    http: HTTPConfig = field(default_factory=HTTPConfig)
    bingx: BingxConfig = field(default_factory=BingxConfig)
