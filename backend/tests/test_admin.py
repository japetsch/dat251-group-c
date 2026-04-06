import httpx


class TestAdminAccess:
    async def test_donor_cannot_access_admin_endpoints(
        self, olav_client: httpx.AsyncClient
    ):
        r = await olav_client.get("/api/admin/bloodbank")
        assert r.status_code == 403

    async def test_unauthenticated_cannot_access_admin_endpoints(
        self, client: httpx.AsyncClient
    ):
        r = await client.get("/api/admin/bloodbank")
        assert r.status_code == 401


class TestListBloodBanks:
    async def test_list_bloodbanks(self, admin_haukeland_client: httpx.AsyncClient):
        r = await admin_haukeland_client.get("/api/admin/bloodbank")
        assert r.status_code == 200
        data = r.json()

        assert len(data) == 2
        haukeland = next(
            b for b in data if b["name"] == "Haukeland universitetssjukehus"
        )
        blodbuss = next(b for b in data if b["name"] == "Blodbussen Nonneseter")

        assert haukeland["user_has_admin_access"] is True
        assert haukeland["bloodbank_id"] == 1
        assert blodbuss["user_has_admin_access"] is False
        assert blodbuss["bloodbank_id"] == 2

    async def test_list_bloodbanks_other_admin(
        self, admin_blodbuss_client: httpx.AsyncClient
    ):
        r = await admin_blodbuss_client.get("/api/admin/bloodbank")
        assert r.status_code == 200
        data = r.json()

        haukeland = next(
            b for b in data if b["name"] == "Haukeland universitetssjukehus"
        )
        blodbuss = next(b for b in data if b["name"] == "Blodbussen Nonneseter")

        assert haukeland["user_has_admin_access"] is False
        assert blodbuss["user_has_admin_access"] is True


class TestCreateBloodBank:
    async def test_create_bloodbank(self, admin_haukeland_client: httpx.AsyncClient):
        r = await admin_haukeland_client.post(
            "/api/admin/bloodbank/create",
            json={
                "name": "Testbanken",
                "street_name": "Testveien",
                "street_number": "1",
                "postal_code": "0000",
                "city": "Testby",
                "loc_lat": 60.0,
                "loc_lon": 5.0,
            },
        )
        assert r.status_code == 200
        assert "bloodbank_id" in r.json()

        r2 = await admin_haukeland_client.get("/api/admin/bloodbank")
        data = r2.json()
        testbank = next((b for b in data if b["name"] == "Testbanken"), None)
        assert testbank is not None
        assert testbank["user_has_admin_access"] is True


class TestBloodBankAppointments:
    async def test_get_appointments(self, admin_haukeland_client: httpx.AsyncClient):
        """AdminHaukeland sees non-cancelled appointments at bloodbank 1 after a given date"""
        r = await admin_haukeland_client.get(
            "/api/admin/bloodbank/1/appointment",
            params={"after": "2026-01-01T00:00:00Z"},
        )
        assert r.status_code == 200
        data = r.json()

        # 2 non-cancelled appointments: Olav (slot 1, Feb 20) and Sigrid (slot 3, Dec 5)
        assert len(data) == 2

        slot_1 = next((s for s in data if s["bookingslot_id"] == 1), None)
        slot_3 = next((s for s in data if s["bookingslot_id"] == 3), None)
        assert slot_1 is not None
        assert slot_3 is not None

        olav_appt = slot_1["appointments"][0]
        assert olav_appt["donor_name"] == "Olav"
        assert olav_appt["appointment_cancelled"] is False
        assert olav_appt["donor_blood_type"] == "O+"

        assert len(olav_appt["notes"]) == 2

        assert len(olav_appt["donations"]) == 1
        assert olav_appt["donations"][0]["amount_ml"] == 20.0

        sigrid_appt = slot_3["appointments"][0]
        assert sigrid_appt["donor_name"] == "Sigrid"
        assert len(sigrid_appt["notes"]) == 1

    async def test_get_appointments_with_cancelled(
        self, admin_haukeland_client: httpx.AsyncClient
    ):
        """With show_cancelled=true, Peter's cancelled appointment also appears"""
        r = await admin_haukeland_client.get(
            "/api/admin/bloodbank/1/appointment",
            params={
                "after": "2026-01-01T00:00:00Z",
                "show_cancelled": "true",
            },
        )
        assert r.status_code == 200
        data = r.json()

        # Now 3 slots: 1 (Olav), 2 (Peter cancelled), 3 (Sigrid)
        assert len(data) == 3
        slot_2 = next((s for s in data if s["bookingslot_id"] == 2), None)
        assert slot_2 is not None
        peter_appt = slot_2["appointments"][0]
        assert peter_appt["donor_name"] == "Peter"
        assert peter_appt["appointment_cancelled"] is True

    async def test_get_appointments_wrong_admin(
        self, admin_blodbuss_client: httpx.AsyncClient
    ):
        r = await admin_blodbuss_client.get(
            "/api/admin/bloodbank/1/appointment",
            params={"after": "2026-01-01T00:00:00Z"},
        )
        assert r.status_code == 403


class TestAdminNotes:
    async def test_admin_add_note(self, admin_haukeland_client: httpx.AsyncClient):
        r = await admin_haukeland_client.post(
            "/api/admin/appointment/1/note",
            json={"message": "We have donor cleared, donor cleared"},
        )
        assert r.status_code == 204

        r2 = await admin_haukeland_client.get(
            "/api/admin/bloodbank/1/appointment",
            params={"after": "2026-01-01T00:00:00Z"},
        )
        slot_1 = next(s for s in r2.json() if s["bookingslot_id"] == 1)
        notes = slot_1["appointments"][0]["notes"]

        # Originally 2 notes, now 3
        assert len(notes) == 3
        assert any(
            n["message"] == "We have donor cleared, donor cleared" for n in notes
        )

    async def test_admin_add_note_wrong_bloodbank(
        self, admin_blodbuss_client: httpx.AsyncClient
    ):
        r = await admin_blodbuss_client.post(
            "/api/admin/appointment/1/note",
            json={
                "message": "The definition of insanity is doing the same thing over and over again, and expecting different results"
            },
        )
        assert r.status_code == 403


class TestRegisterDonation:
    async def test_register_donation(self, admin_haukeland_client: httpx.AsyncClient):
        r = await admin_haukeland_client.post(
            "/api/admin/appointment/3/donation",
            json={"amount_ml": 450.0, "is_blood_not_plasma": True},
        )
        assert r.status_code == 200
        assert "donation_id" in r.json()

    async def test_register_donation_wrong_admin(
        self, admin_blodbuss_client: httpx.AsyncClient
    ):
        r = await admin_blodbuss_client.post(
            "/api/admin/appointment/1/donation",
            json={"amount_ml": 450.0},
        )
        assert r.status_code == 403


class TestRegisterInterview:
    async def test_register_interview(self, admin_haukeland_client: httpx.AsyncClient):
        r = await admin_haukeland_client.post(
            "/api/admin/donor/1/form/interview",
            json={
                "ok_to_donate": True,
                "validity_duration": "P180D",
            },
        )
        assert r.status_code == 204

    async def test_register_interview_other_admin(
        self, admin_blodbuss_client: httpx.AsyncClient
    ):
        r = await admin_blodbuss_client.post(
            "/api/admin/donor/1/form/interview",
            json={
                "ok_to_donate": False,
                "validity_duration": "P90D",
            },
        )
        assert r.status_code == 204


class TestRegisterDonationTest:
    async def test_register_donation_test(
        self, admin_haukeland_client: httpx.AsyncClient
    ):
        r = await admin_haukeland_client.post(
            "/api/admin/donor/1/form/donation-test",
            json={
                "donation_id": 1,
                "ok_to_donate": True,
                "validity_duration": "P180D",
            },
        )
        assert r.status_code == 204

    async def test_register_donation_test_wrong_donor(
        self, admin_haukeland_client: httpx.AsyncClient
    ):
        # Donation 1 belongs to donor 1 (Olav), not donor 2 (Peter)
        r = await admin_haukeland_client.post(
            "/api/admin/donor/2/form/donation-test",
            json={
                "donation_id": 1,
                "ok_to_donate": True,
                "validity_duration": "P180D",
            },
        )
        assert r.status_code == 400
        assert "not given by provided donor" in r.json()["detail"]

    async def test_register_donation_test_wrong_admin(
        self, admin_blodbuss_client: httpx.AsyncClient
    ):
        r = await admin_blodbuss_client.post(
            "/api/admin/donor/1/form/donation-test",
            json={
                "donation_id": 1,
                "ok_to_donate": True,
                "validity_duration": "P180D",
            },
        )
        assert r.status_code == 403


class TestManageAdmins:
    async def test_add_and_remove_admin(
        self, admin_haukeland_client: httpx.AsyncClient
    ):
        """Add and remove AdminBlodbuss (admin_id 2) to bloodbank 1 (haukeland)"""
        r = await admin_haukeland_client.post(
            "/api/admin/bloodbank/1/admin/add",
            json={"admin_id": 2},
        )
        assert r.status_code == 204

        # Verify AdminHaukeland still has access
        # TODO: admins see other admins, s.t. adding blodbuss admin can be verified
        r2 = await admin_haukeland_client.get("/api/admin/bloodbank")
        haukeland = next(b for b in r2.json() if b["bloodbank_id"] == 1)
        assert haukeland["user_has_admin_access"] is True

        r3 = await admin_haukeland_client.request(
            "DELETE",
            "/api/admin/bloodbank/1/admin/remove",
            json={"admin_id": 2},
        )
        assert r3.status_code == 204

    async def test_cannot_remove_last_admin(
        self, admin_haukeland_client: httpx.AsyncClient
    ):
        r = await admin_haukeland_client.request(
            "DELETE",
            "/api/admin/bloodbank/1/admin/remove",
            json={"admin_id": 1},
        )
        assert r.status_code == 409
        assert "last admin" in r.json()["detail"].lower()

        r2 = await admin_haukeland_client.get("/api/admin/bloodbank")
        haukeland = next(b for b in r2.json() if b["bloodbank_id"] == 1)
        assert haukeland["user_has_admin_access"] is True
