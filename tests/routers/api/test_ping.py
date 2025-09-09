from http import HTTPStatus

from httpx import AsyncClient


async def test_ping__status_code(client: AsyncClient) -> None:
    response = await client.get("/api/ping/")
    assert response.status_code == HTTPStatus.OK


async def test_ping__format(client: AsyncClient) -> None:
    response = await client.get("/api/ping/")
    assert response.json() == {"message": "pong"}
