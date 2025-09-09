from http import HTTPStatus

from httpx import AsyncClient

URL = "/api/ping/"


async def test_ping__status_code(client: AsyncClient) -> None:
    response = await client.get(URL)
    assert response.status_code == HTTPStatus.OK


async def test_ping__format(client: AsyncClient) -> None:
    response = await client.get(URL)
    assert response.json() == {"message": "pong"}
