import httpx


class TestBookingslot:
    async def test_cannot_get_bookingslots_unauthenticated(
        self, client: httpx.AsyncClient
    ):
        response = await client.get("/api/bookingslot/available")
        assert response.status_code == 401

    async def test_get_available_bookingslots_olav(
        self, olav_client: httpx.AsyncClient
    ):
        r = await olav_client.get("/api/bookingslot/available")
        assert r.status_code == 200
        response_json = r.json()

        # Only has cancelled appointments at this point so all but capacity 0 valid
        expected = [
            {
                "id": 1,
                "time": "2026-02-20T16:00:00Z",
                "duration": "PT30M",
                "capacity": 11,
                "bloodbank_id": 1,
                "bloodbank_name": "Haukeland universitetssjukehus",
                "location_id": 2,
                "valid": True,
            },
            {
                "id": 2,
                "time": "2026-05-11T11:30:00Z",
                "duration": "PT30M",
                "capacity": 10,
                "bloodbank_id": 1,
                "bloodbank_name": "Haukeland universitetssjukehus",
                "location_id": 2,
                "valid": True,
            },
            {
                "id": 3,
                "time": "2026-12-05T06:00:00Z",
                "duration": "PT30M",
                "capacity": 9,
                "bloodbank_id": 1,
                "bloodbank_name": "Haukeland universitetssjukehus",
                "location_id": 2,
                "valid": True,
            },
            {
                "id": 4,
                "time": "2026-12-05T06:00:00Z",
                "duration": "PT30M",
                "capacity": 0,
                "bloodbank_id": 1,
                "bloodbank_name": "Haukeland universitetssjukehus",
                "location_id": 2,
                "valid": False,
            },
            {
                "id": 5,
                "time": "2026-06-21T06:00:00Z",
                "duration": "PT30M",
                "capacity": 10,
                "bloodbank_id": 1,
                "bloodbank_name": "Haukeland universitetssjukehus",
                "location_id": 2,
                "valid": True,
            },
        ]

        assert isinstance(response_json, list)
        assert len(response_json) >= 1
        for elem in expected:
            assert elem in response_json

    async def test_get_available_bookingslots_peter(
        self, peter_client: httpx.AsyncClient
    ):
        r = await peter_client.get("/api/bookingslot/available")
        assert r.status_code == 200
        response_json = r.json()
        for elem in response_json:
            if elem["id"] == 4:
                assert elem["valid"] == False
            else:
                assert elem["valid"] == True

    async def test_get_available_bookingslots_sigrid(
        self, sigrid_client: httpx.AsyncClient
    ):
        r = await sigrid_client.get("/api/bookingslot/available")
        assert r.status_code == 200
        response_json = r.json()
        for elem in response_json:
            if elem["id"] == 4 or elem["id"] == 3:
                assert elem["valid"] == False
            else:
                assert elem["valid"] == True

    async def test_book_slot_removes_free_slot(self, olav_client: httpx.AsyncClient):
        response = await olav_client.post(
            "/api/bookingslot/book",
            json={"bookingslot_id": 1, "donor_id": 1},
        )
        assert response.status_code == 200

        await self.assert_bookingslot_capacity(olav_client, 1, 10)

    async def test_book_slot_with_no_capacity(self, olav_client: httpx.AsyncClient):
        response = await olav_client.post(
            "/api/bookingslot/book",
            json={"bookingslot_id": 4, "donor_id": 1},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Bookingslot not available"}

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
