import httpx


class TestIndex:
    async def test_openapi_docs_available(self, client: httpx.AsyncClient):
        response = await client.get("/docs")
        assert response.status_code == 200
