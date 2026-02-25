from fastapi.testclient import TestClient

from app.main import app


class TestIndex:
    def test_openapi_docs_available(self):
        with TestClient(app, root_path="") as client:
            response = client.get("/docs")
            assert response.status_code == 200
