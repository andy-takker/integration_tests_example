import uvicorn

from exchange_wallet.app import build_app
from exchange_wallet.config import Config


def main() -> None:
    config = Config()
    fastapi_app = build_app(config)

    uvicorn.run(
        fastapi_app,
        host=config.http.host,
        port=config.http.port,
        forwarded_allow_ips="*",
    )


if __name__ == "__main__":
    main()
