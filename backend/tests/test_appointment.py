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
        expected_list = [
            {
                "id": 1,
                "username": "Olav",
                "time": "2026-12-05T06:00:00Z",
                "duration": "PT30M",
                "bloodbank_name": "Haukeland universitetssjukehus",
                "cancelled": True,
            }
        ]
        for elem in expected_list:
            assert elem in response_json
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

    def test_get_available_appointments(self, olav_client: TestClient):
        r = olav_client.get("/api/bookingslot/available")
        assert r.status_code == 200
        response_json = r.json()

        expected = [
            {
                "id": 1,
                "time": "2026-02-20T16:00:00Z",
                "duration": "PT30M",
                "capacity": 11,
                "bloodbank_id": 1,
                "bloodbank_name": "Haukeland universitetssjukehus",
                "location_id": 2,
            },
            {
                "id": 2,
                "time": "2026-05-11T11:30:00Z",
                "duration": "PT30M",
                "capacity": 10,
                "bloodbank_id": 1,
                "bloodbank_name": "Haukeland universitetssjukehus",
                "location_id": 2,
            },
            {
                "id": 3,
                "time": "2026-12-05T06:00:00Z",
                "duration": "PT30M",
                "capacity": 9,
                "bloodbank_id": 1,
                "bloodbank_name": "Haukeland universitetssjukehus",
                "location_id": 2,
            },
        ]

        assert isinstance(response_json, list)
        assert len(response_json) >= 1
        for elem in expected:
            assert elem in response_json

    def test_book_appointment_removes_free_slot(self, olav_client: TestClient):
        response = olav_client.post(
            "/api/bookingslot/book",
            json={"bookingslot_id": 1, "donor_id": 1},
        )
        assert response.status_code == 200

        self.assert_bookingslot_capacity(olav_client, 1, 10)

    def test_book_appointment_with_no_capacity(self, olav_client: TestClient):
        response = olav_client.post(
            "/api/bookingslot/book",
            json={"bookingslot_id": 4, "donor_id": 1},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Bookingslot not available"}
