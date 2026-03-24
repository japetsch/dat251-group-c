from fastapi.testclient import TestClient


class TestTestresult:
    def test_cannot_get_testresults_unauthenticated(self, client: TestClient):
        response = client.get("/api/testresult")
        assert response.status_code == 401

    def test_cannot_get_testresult_unauthenticated(self, client: TestClient):
        response = client.get("/api/testresult/1")
        assert response.status_code == 401

    def test_can_get_testresults(self, olav_client: TestClient):
        response = olav_client.get("/api/testresult")
        assert response.status_code == 200

        response_json = response.json()
        expected = [
            {
                "id": 1,
                "donor_id": 1,
                "form_id": 1,
                "time": "2025-04-30T10:00:00Z",
                "validity_duration": "P180D",
                "invalidated": True,
            },
            {
                "id": 5,
                "donor_id": 1,
                "form_id": 5,
                "time": "2026-02-20T16:00:00Z",
                "validity_duration": "P180D",
                "invalidated": False,
            },
        ]
        for elem in expected:
            assert elem in response_json

    def test_can_get_testresults_empty_list(self, sigrid_client: TestClient):
        response = sigrid_client.get("/api/testresult")
        assert response.status_code == 200

        response_json = response.json()
        assert isinstance(response_json, list)
        assert len(response_json) == 0

    def test_can_get_testresult_interview(self, olav_client: TestClient):
        response = olav_client.get("/api/testresult/1")

        expected = {
            "id": 1,
            "donor_id": 1,
            "form_id": 1,
            "time": "2025-04-30T10:00:00Z",
            "validity_duration": "P180D",
            "invalidated": True,
            "ok_to_donate": False,
            "interview_id": 1,
            "entry_form_id": None,
            "donation_test_id": None,
            "interviewer_admin_id": 1,
            "donation_id": None,
            "appointment_id": None,
            "amount_ml": None,
            "is_blood_not_plasma": None,
        }

        response_json = response.json()

        assert response_json == expected

    def test_can_get_testresult_donation(self, olav_client: TestClient):
        response = olav_client.get("/api/testresult/5")

        expected = {
            "id": 5,
            "donor_id": 1,
            "form_id": 5,
            "time": "2026-02-20T16:00:00Z",
            "validity_duration": "P180D",
            "invalidated": False,
            "ok_to_donate": True,
            "interview_id": None,
            "entry_form_id": None,
            "donation_test_id": 1,
            "interviewer_admin_id": None,
            "donation_id": 1,
            "appointment_id": 1,
            "amount_ml": 20.0,
            "is_blood_not_plasma": True,
        }

        response_json = response.json()

        assert response_json == expected

    def test_cannot_get_testresult_of_other_user(self, olav_client: TestClient):
        response = olav_client.get("/api/testresult/2")

        assert response.status_code == 404
        assert response.json() == {"detail": "Test result for diffenrent user"}
