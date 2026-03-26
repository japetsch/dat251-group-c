import httpx


class TestTestresult:
    async def test_cannot_get_testresults_unauthenticated(
        self, client: httpx.AsyncClient
    ):
        response = await client.get("/api/testresult")
        assert response.status_code == 401

    async def test_cannot_get_testresult_unauthenticated(
        self, client: httpx.AsyncClient
    ):
        response = await client.get("/api/testresult/1")
        assert response.status_code == 401

    async def test_can_get_testresults(self, olav_client: httpx.AsyncClient):
        response = await olav_client.get("/api/testresult")
        assert response.status_code == 200

        response_json = response.json()
        expected = {
            "interviews": [
                {
                    "id": 1,
                    "donor_id": 1,
                    "form_id": 1,
                    "time": "2025-04-30T10:00:00Z",
                    "validity_duration": "P180D",
                    "invalidated": True,
                    "interview_id": 1,
                    "admin_name": "AdminHaukeland",
                }
            ],
            "entry_forms": [],
            "donation_tests": [
                {
                    "id": 5,
                    "donor_id": 1,
                    "form_id": 5,
                    "time": "2026-02-20T16:00:00Z",
                    "validity_duration": "P180D",
                    "invalidated": False,
                    "donation_test_id": 1,
                    "admin_name": "AdminHaukeland",
                }
            ],
        }
        for elem in expected["interviews"]:
            assert elem in response_json["interviews"]
        for elem in expected["entry_forms"]:
            assert elem in response_json["entry_forms"]
        for elem in expected["donation_tests"]:
            assert elem in response_json["donation_tests"]

    async def test_can_get_testresults_empty_list(
        self, sigrid_client: httpx.AsyncClient
    ):
        response = await sigrid_client.get("/api/testresult")
        assert response.status_code == 200

        response_json = response.json()
        assert isinstance(response_json["interviews"], list)
        assert len(response_json["interviews"]) == 0
        assert isinstance(response_json["entry_forms"], list)
        assert len(response_json["entry_forms"]) == 0
        assert isinstance(response_json["donation_tests"], list)
        assert len(response_json["donation_tests"]) == 0

    async def test_can_get_testresult_interview(self, olav_client: httpx.AsyncClient):
        response = await olav_client.get("/api/testresult/1")

        expected = {
            "id": 1,
            "donor_id": 1,
            "form_id": 1,
            "time": "2025-04-30T10:00:00Z",
            "validity_duration": "P180D",
            "invalidated": True,
            "ok_to_donate": False,
            "interview_id": 1,
            "interviewer_admin_id": 1,
            "interviewer_admin_name": "AdminHaukeland",
        }

        response_json = response.json()

        assert response_json == expected

    async def test_can_get_testresult_donation(self, olav_client: httpx.AsyncClient):
        response = await olav_client.get("/api/testresult/5")

        expected = {
            "id": 5,
            "donor_id": 1,
            "form_id": 5,
            "time": "2026-02-20T16:00:00Z",
            "validity_duration": "P180D",
            "invalidated": False,
            "ok_to_donate": True,
            "donation_test_id": 1,
            "tester_admin_id": 1,
            "donation_id": 1,
            "appointment_id": 1,
            "amount_ml": 20.0,
            "is_blood_not_plasma": True,
            "tester_admin_name": "AdminHaukeland",
        }

        response_json = response.json()

        assert response_json == expected

    async def test_cannot_get_testresult_of_other_user(
        self, olav_client: httpx.AsyncClient
    ):
        response = await olav_client.get("/api/testresult/2")

        assert response.status_code == 404
        assert response.json() == {"detail": "Test result for diffenrent user"}
