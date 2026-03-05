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
            expected = [
                {
                    "id": 1,
                    "username": "Olav",
                    "locationname": "Stavanger",
                    "time": "2026-02-20T16:00:00Z",
                },
                {
                    "id": 2,
                    "username": "Sigrid",
                    "locationname": "Haukeland",
                    "time": "2026-05-11T11:30:00Z",
                },
                {
                    "id": 3,
                    "username": "Peter",
                    "locationname": "Oslo",
                    "time": "2026-12-05T06:00:00Z",
                },
            ]
            for elem in expected:
                assert elem in response_json

    def test_update_appointment(self):
        with TestClient(app, root_path="") as client:
            request_body = {"id": 1, "time": "2029-05-11T11:30:00Z"}
            response = client.patch("/api/appointment", json=request_body)
            response_json = response.json()
            expected = {
                "id": 1,
                "user_id": 1,
                "time": "2029-05-11T11:30:00Z",
                "location_id": 2,
            }
            assert response_json == expected

            # verify whole data
            response = client.get("/api/appointment")
            response_json = response.json()
            expected = [
                {
                    "id": 2,
                    "username": "Sigrid",
                    "locationname": "Haukeland",
                    "time": "2026-05-11T11:30:00Z",
                },
                {
                    "id": 3,
                    "username": "Peter",
                    "locationname": "Oslo",
                    "time": "2026-12-05T06:00:00Z",
                },
                {
                    "id": 1,
                    "username": "Olav",
                    "locationname": "Stavanger",
                    "time": "2029-05-11T11:30:00Z",
                },
            ]
            for elem in expected:
                assert elem in response_json

    def test_update_on_not_found_appointment(self):
        with TestClient(app, root_path="") as client:
            request_body = {"id": 10, "time": "2029-05-11T11:30:00Z"}
            response = client.patch("/api/appointment", json=request_body)
            assert response.status_code == 404

    def test_delete_appointment(self):
        with TestClient(app, root_path="") as client:
            response = client.delete("/api/appointment/1")
            response_json = response.json()
            expected = {
                "id": 1,
                "user_id": 1,
                "time": "2029-05-11T11:30:00Z",
                "location_id": 2,
            }
            assert response_json == expected

            # verify whole data
            response = client.get("/api/appointment")
            response_json = response.json()
            expected = [
                {
                    "id": 2,
                    "username": "Sigrid",
                    "locationname": "Haukeland",
                    "time": "2026-05-11T11:30:00Z",
                },
                {
                    "id": 3,
                    "username": "Peter",
                    "locationname": "Oslo",
                    "time": "2026-12-05T06:00:00Z",
                },
            ]
            for elem in expected:
                assert elem in response_json

    def test_delete_on_not_found_appointment(self):
        with TestClient(app, root_path="") as client:
            response = client.delete("/api/appointment/10")
            assert response.status_code == 404

    def test_get_available_appointments(self):
        with TestClient(app, root_path="") as client:
            r = client.get("/api/appointment/available")
            assert r.status_code == 200
            data = r.json()
            assert isinstance(data, list)
            assert len(data) >= 1
            assert "id" in data[0]
            assert "time" in data[0]
            assert "location_id" in data[0]
            assert "locationname" in data[0]

    def test_book_appointment_removes_free_slot(self):
        with TestClient(app, root_path="") as client:
            r = client.get("/api/appointment/available")
            assert r.status_code == 200
            slot = r.json()[0]

            book = client.post(
                "/api/appointment/book",
                json={"free_appointment_id": slot["id"], "user_id": 1},
            )
            assert book.status_code == 200

            r2 = client.get("api/appointment/available")
            ids = [x["id"] for x in r2.json()]
            assert slot["id"] not in ids