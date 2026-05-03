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

    async def test_reject_unauthenticated_user_info(self, client: httpx.AsyncClient):
        response = await client.get("/api/auth/me")
        assert response.status_code == 401

    async def test_can_sign_up_donor(self, client: httpx.AsyncClient):
        req_body = {
            "email": "new_donor@example.com",
            "password": "strongpassword123",
            "name": "New Donor",
            "phone_number": "12345678",
            "street_name": "Testgaten",
            "street_number": "1",
            "apt_number": None,
            "postal_code": "5000",
            "city": "Bergen",
            "country": "Norway",
            "preferred_bloodbank_id": 1,
            "blood_type": "A+",
        }
        response = await client.post("/api/auth/signup-donor", json=req_body)
        assert response.status_code == 204

    async def test_reject_signup_with_duplicate_email(self, client: httpx.AsyncClient):
        req_body = {
            "email": "olav@uib.no",
            "password": "somepassword",
            "name": "Another Olav",
            "phone_number": "98765432",
            "street_name": "Testgaten",
            "street_number": "2",
            "apt_number": None,
            "postal_code": "5000",
            "city": "Bergen",
            "country": "Norway",
            "preferred_bloodbank_id": 1,
            "blood_type": None,
        }
        response = await client.post("/api/auth/signup-donor", json=req_body)
        assert response.status_code >= 400
