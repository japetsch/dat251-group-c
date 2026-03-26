from fastapi.testclient import TestClient

from app.main import app


class TestAuth:
    def test_can_log_in_and_out(self):
        with TestClient(app, root_path="") as client:
            req_body = {
                "email": "olav@uib.no",
                "password": "correct horse battery staple",
            }
            response = client.post("/api/auth/login", json=req_body)
            assert response.status_code == 204

            response = client.get("/api/auth/me")
            assert response.status_code == 200
            assert response.json()["user_name"] == "Olav"

            response = client.get("/api/auth/logout")
            assert response.status_code == 204

    def test_reject_nonexistent_user(self):
        with TestClient(app, root_path="") as client:
            req_body = {
                "email": "anna@uib.no",
                "password": "correct horse battery staple",
            }
            response = client.post("/api/auth/login", json=req_body)
            assert response.status_code == 401

    def test_reject_incorrect_pass(self):
        with TestClient(app, root_path="") as client:
            req_body = {"email": "olav@uib.no", "password": "wrong cat fuel paperclip"}
            response = client.post("/api/auth/login", json=req_body)
            assert response.status_code == 401
