from fastapi.testclient import TestClient

from app.main import app


class TestAppointment:
    def test_can_get_appointment(self):
        with TestClient(app, root_path="") as client:
            response = client.get("/api/appointment")
            assert response.status_code == 200

    def test_get_list_on_get_appointment(self):
        with TestClient(app, root_path="") as client:
            response = client.get("/api/appointment")
            response_json = response.json()
            print(response_json)
            assert response_json[0]["username"] == "Olav"
            assert response_json[0]["locationname"] == "Stavanger"
            assert response_json[0]["time"] == "2026-02-20T16:00:00Z"
            assert response_json[1]["username"] == "Sigrid"
            assert response_json[1]["locationname"] == "Haukeland"
            assert response_json[1]["time"] == "2026-05-11T11:30:00Z"
            assert response_json[2]["username"] == "Peter"
            assert response_json[2]["locationname"] == "Oslo"
            assert response_json[2]["time"] == "2026-12-05T06:00:00Z"
