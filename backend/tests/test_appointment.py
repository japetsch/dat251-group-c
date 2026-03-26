from fastapi.testclient import TestClient


class TestAppointment:
    def test_can_get_appointments(self, olav_client: TestClient):
        response = olav_client.get("/api/appointment")
        assert response.status_code == 200

        response_json = response.json()
        expected = [
            {
                "id": 1,
                "username": "Olav",
                "time": "2026-02-20T16:00:00Z",
                "duration": "PT30M",
                "bloodbank_name": "Haukeland universitetssjukehus",
                "cancelled": False,
                "notes": [
                    {
                        "author_user_id": 4,
                        "author_name": "AdminHaukeland",
                        "message": "Hi, I am AdminHaukeland!",
                        "time": "2026-02-18T15:30:00+01:00",
                    },
                    {
                        "author_user_id": 1,
                        "author_name": "Olav",
                        "message": "Hi my name is Olav!",
                        "time": "2026-02-18T11:00:00+01:00",
                    },
                ],
            }
        ]
        for elem in expected:
            assert elem in response_json

    def test_cannot_get_appointments_unauthenticated(self, client: TestClient):
        response = client.get("/api/appointment")
        assert response.status_code == 401

    def test_update_appointment(self, olav_client: TestClient):
        request_body = {"bookingslot_id": 3, "cancelled": True}
        response = olav_client.patch("/api/appointment/1", json=request_body)
        response_json = response.json()
        expected = {"id": 1, "bookingslot_id": 3, "cancelled": True, "donor_id": 1}
        assert response_json == expected

        # verify whole data
        response = olav_client.get("/api/appointment")
        response_json = response.json()
        assert len(response_json) == 1, "More than one appointment for Olav returned"
        response_data = response_json[0]

        # Appointment notes are ignored here
        expected_data = {
            "id": 1,
            "username": "Olav",
            "time": "2026-12-05T06:00:00Z",
            "duration": "PT30M",
            "bloodbank_name": "Haukeland universitetssjukehus",
            "cancelled": True,
        }
        for k, v in expected_data.items():
            assert k in response_data
            assert response_data[k] == v

        self.assert_bookingslot_capacity(olav_client, 1, 11)
        self.assert_bookingslot_capacity(olav_client, 3, 9)

    def test_update_on_not_found_appointment(self, olav_client: TestClient):
        request_body = {"bookingslot_id": 10, "cancelled": False}
        response = olav_client.patch("/api/appointment/12", json=request_body)
        assert response.status_code == 404

    def test_update_appointment_no_capacity(self, olav_client: TestClient):
        request_body = {"bookingslot_id": 4, "cancelled": False}
        response = olav_client.patch("/api/appointment/1", json=request_body)
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Appointment not found or no capacity on booking slot"
        }

    def test_cannot_update_other_users_appointment(self, peter_client: TestClient):
        # Peter tries to update Olav's appointment (id=1)
        request_body = {"bookingslot_id": 3, "cancelled": True}
        response = peter_client.patch("/api/appointment/1", json=request_body)
        assert response.status_code == 404

    def assert_bookingslot_capacity(
        self, client: TestClient, bookingslot_id: int, capacity: int
    ):
        response = client.get("/api/bookingslot/available")
        response_json = response.json()

        bookingslot = next(
            (x for x in response_json if x["id"] == bookingslot_id), None
        )
        assert bookingslot is not None
        assert bookingslot["capacity"] == capacity
