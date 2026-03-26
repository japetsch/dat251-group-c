import httpx


class TestAuth:
    async def test_can_log_in_and_out(self, client: httpx.AsyncClient):
        req_body = {
            "email": "olav@uib.no",
            "password": "correct horse battery staple",
        }
        response = await client.post("/api/auth/login", json=req_body)
        assert response.status_code == 204

        response = await client.get("/api/auth/me")
        assert response.status_code == 200
        assert response.json()["user_name"] == "Olav"

        response = await client.get("/api/auth/logout")
        assert response.status_code == 204

    async def test_reject_nonexistent_user(self, client: httpx.AsyncClient):
        req_body = {
            "email": "anna@uib.no",
            "password": "correct horse battery staple",
        }
        response = await client.post("/api/auth/login", json=req_body)
        assert response.status_code == 401

    async def test_reject_incorrect_pass(self, client: httpx.AsyncClient):
        req_body = {"email": "olav@uib.no", "password": "wrong cat fuel paperclip"}
        response = await client.post("/api/auth/login", json=req_body)
        assert response.status_code == 401
