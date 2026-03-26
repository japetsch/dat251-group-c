import httpx


class TestAppointment:
    async def test_can_get_appointments(self, olav_client: httpx.AsyncClient):
        response = await olav_client.get("/api/appointment")
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

    async def test_cannot_get_appointments_unauthenticated(
        self, client: httpx.AsyncClient
    ):
        response = await client.get("/api/appointment")
        assert response.status_code == 401

    async def test_update_appointment(self, olav_client: httpx.AsyncClient):
        request_body = {"bookingslot_id": 3, "cancelled": True}
        response = await olav_client.patch("/api/appointment/1", json=request_body)
        response_json = response.json()
        expected = {"id": 1, "bookingslot_id": 3, "cancelled": True, "donor_id": 1}
        assert response_json == expected

        # verify whole data
        response = await olav_client.get("/api/appointment")
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

        await self.assert_bookingslot_capacity(olav_client, 1, 11)
        await self.assert_bookingslot_capacity(olav_client, 3, 9)

    async def test_update_on_not_found_appointment(
        self, olav_client: httpx.AsyncClient
    ):
        request_body = {"bookingslot_id": 10, "cancelled": False}
        response = await olav_client.patch("/api/appointment/12", json=request_body)
        assert response.status_code == 404

    async def test_update_appointment_no_capacity(self, olav_client: httpx.AsyncClient):
        request_body = {"bookingslot_id": 4, "cancelled": False}
        response = await olav_client.patch("/api/appointment/1", json=request_body)
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Appointment not found or no capacity on booking slot"
        }

    async def test_cannot_update_other_users_appointment(
        self, peter_client: httpx.AsyncClient
    ):
        # Peter tries to update Olav's appointment (id=1)
        request_body = {"bookingslot_id": 3, "cancelled": True}
        response = await peter_client.patch("/api/appointment/1", json=request_body)
        assert response.status_code == 404

    async def test_donor_add_note(self, olav_client: httpx.AsyncClient):
        r = await olav_client.post(
            "/api/appointment/1/note",
            json={"message": "My heart aches for donating blood!"},
        )
        assert r.status_code == 204

        r2 = await olav_client.get("/api/appointment")
        appt = next(a for a in r2.json() if a["id"] == 1)
        assert any(
            n["message"] == "My heart aches for donating blood!" for n in appt["notes"]
        )

    async def test_donor_cannot_add_note_to_other_appointment(
        self, peter_client: httpx.AsyncClient
    ):
        r = await peter_client.post(
            "/api/appointment/1/note",  # (Olav's appointment)
            json={
                "message": "The definition of insanity is doing the same thing over and over again, and expecting different results"
            },
        )
        assert r.status_code == 404

    async def assert_bookingslot_capacity(
        self, client: httpx.AsyncClient, bookingslot_id: int, capacity: int
    ):
        response = await client.get("/api/bookingslot/available")
        response_json = response.json()

        bookingslot = next(
            (x for x in response_json if x["id"] == bookingslot_id), None
        )
        assert bookingslot is not None
        assert bookingslot["capacity"] == capacity
