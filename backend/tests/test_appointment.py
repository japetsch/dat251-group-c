from fastapi.testclient import TestClient

from app.main import app


class TestAppointment:
    def test_can_get_appointment(self):
        with TestClient(app, root_path="") as client:
            response = client.get("/api/appointment")
            assert response.status_code == 200
