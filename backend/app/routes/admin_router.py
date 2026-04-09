from datetime import datetime
from typing import final
from zoneinfo import ZoneInfo

from fastapi import HTTPException, status
from fastapi.routing import APIRouter

from app.auth import AdminUserRequired

from ..db.db import DBConnection
from ..db.sqlc.admin import (
    AsyncQuerier as AdminQuerier,
    CreateBloodBankParams,
    RegisterDonationTestParams,
    RegisterInterviewParams,
)
from ..db.sqlc.appointment import AsyncQuerier as AppointmentQuerier
from ..db.sqlc.auth import AsyncQuerier as AuthQuerier
from ..db.sqlc.bloodbank import AsyncQuerier as BloodbankQuerier, GetAllBloodBanksRow
from ..db.sqlc.models import Donation
from ..db.sqlc.testresults import (
    AsyncQuerier as TestresultQuerier,
)
from ..schemas.admin import (
    BookingSlotType,
    CreateBloodBankRequest,
    CreateBloodBankResponse,
    MutateBloodbankAdminsRequest,
    RegisterDonationRequest,
    RegisterDonationResponse,
    RegisterDonationTestRequest,
    RegisterInterviewRequest,
)
from ..schemas.appointment import (
    AddNoteRequest,
)


@final
class AdminRouter(APIRouter):
    def __init__(self) -> None:
        super().__init__(
            tags=["admin"],
        )

        # Register the routes here. Dependencies are request-scoped
        self.add_api_route("/bloodbank", self.list_bloodbanks, methods=["GET"])
        self.add_api_route("/bloodbank/create", self.create_bloodbank, methods=["POST"])
        self.add_api_route(
            "/bloodbank/{bloodbank_id}/admin/add",
            self.add_admin_to_bloodbank,
            methods=["POST"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self.add_api_route(
            "/bloodbank/{bloodbank_id}/admin/remove",
            self.remove_admin_from_bloodbank,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self.add_api_route(
            "/bloodbank/{bloodbank_id}/appointment",
            self.bloodbank_appointments,
            methods=["GET"],
        )
        self.add_api_route(
            "/appointment/{appointment_id}/note",
            self.appointment_add_note,
            methods=["POST"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self.add_api_route(
            "/appointment/{appointment_id}/donation",
            self.appointment_register_donation,
            methods=["POST"],
        )
        self.add_api_route(
            "/donor/{donor_id}/form/interview",
            self.register_interview,
            methods=["POST"],
            status_code=status.HTTP_204_NO_CONTENT,
        )
        self.add_api_route(
            "/appointment/{appointment_id}/result",
            self.get_testresult_for_appointment_admin,
            methods=["GET"],
        )
        self.add_api_route(
            "/donor/{donor_id}/form/donation-test",
            self.register_donation_test,
            methods=["POST"],
            status_code=status.HTTP_204_NO_CONTENT,
        )

    async def list_bloodbanks(
        self, user: AdminUserRequired, engine: DBConnection
    ) -> list[GetAllBloodBanksRow]:
        """
        Lists all blood banks in the system, even the ones the logged in user is not adminstrator for

        TODO:
        - enhance with opening hours information
        - allow admins to list which people are admins
        """
        aq = BloodbankQuerier(engine)
        blood_banks: list[GetAllBloodBanksRow] = []
        async for r in aq.get_all_blood_banks(admin_id=user.admin_id):
            blood_banks.append(r)
        return blood_banks

    async def create_bloodbank(
        self,
        user: AdminUserRequired,
        data: CreateBloodBankRequest,
        engine: DBConnection,
    ):
        """
        Creates a new bloodbank with the logged in admin user as an administrator
        """
        aq = AdminQuerier(engine)
        res = await aq.create_blood_bank(
            CreateBloodBankParams(
                name=data.name,
                admin_id=user.admin_id,
                latitude=data.loc_lat,
                longitude=data.loc_lon,
                street_name=data.street_name,
                street_number=data.street_number,
                postal_code=data.postal_code,
                city=data.city,
                country=data.country,
            )
        )

        assert res is not None, "blood bank creation success but no id returned???"
        return CreateBloodBankResponse(bloodbank_id=res)

    async def _assert_bb_access(
        self, admin_id: int, bloodbank_id: int, engine: DBConnection
    ):
        a = AuthQuerier(engine)
        access = await a.has_admin_at_blood_bank(
            admin_id=admin_id, bloodbank_id=bloodbank_id
        )
        if not access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not admin for this blood bank",
            )

    async def _assert_appt_access(
        self, admin_id: int, appointment_id: int, engine: DBConnection
    ):
        a = AuthQuerier(engine)
        access = await a.has_admin_where_appointment_is(
            admin_id=admin_id, appointment_id=appointment_id
        )
        if not access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not admin for this appointment",
            )

    async def add_admin_to_bloodbank(
        self,
        bloodbank_id: int,
        data: MutateBloodbankAdminsRequest,
        user: AdminUserRequired,
        engine: DBConnection,
    ):
        """
        Add another admin to a blood bank the logged in user is administrator for
        """
        await self._assert_bb_access(user.admin_id, bloodbank_id, engine)
        aq = AdminQuerier(engine)
        await aq.add_blood_bank_admin(bloodbank_id=bloodbank_id, admin_id=data.admin_id)

    async def remove_admin_from_bloodbank(
        self,
        bloodbank_id: int,
        data: MutateBloodbankAdminsRequest,
        user: AdminUserRequired,
        engine: DBConnection,
    ):
        """
        Remove an admin from a blood bank the logged in user is administrator for

        The user can remove themselves.
        The user can't remove the last admin of a blood bank.
        """
        await self._assert_bb_access(user.admin_id, bloodbank_id, engine)
        aq = AdminQuerier(engine)
        removed_admin_id = await aq.remove_blood_bank_admin(
            bloodbank_id=bloodbank_id, admin_id=data.admin_id
        )
        if removed_admin_id is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot remove the last admin of a blood bank",
            )

    async def bloodbank_appointments(
        self,
        user: AdminUserRequired,
        bloodbank_id: int,
        engine: DBConnection,
        after: datetime | None = None,
        before: datetime | None = None,
        show_cancelled: bool = False,
    ) -> list[BookingSlotType]:
        """
        Show appointments for blood bank.

        By default only the ones scheduled after 00:00 in Oslo on the same day
        """
        await self._assert_bb_access(user.admin_id, bloodbank_id, engine)

        if after is None:
            tz_oslo = ZoneInfo("Europe/Oslo")
            after = datetime.now(tz=tz_oslo).replace(
                hour=0, minute=0, second=0, microsecond=0
            )

        aq = AdminQuerier(engine)
        appts = aq.get_appointments_at_blood_bank(
            bloodbank_id=bloodbank_id,
            after=after,
            before=before,
            show_cancelled=show_cancelled,
        )

        slots: list[BookingSlotType] = []
        async for a in appts:
            slots.append(BookingSlotType.model_validate(a, from_attributes=True))
        return slots

    async def appointment_add_note(
        self,
        user: AdminUserRequired,
        appointment_id: int,
        data: AddNoteRequest,
        engine: DBConnection,
    ):
        await self._assert_appt_access(user.admin_id, appointment_id, engine)
        aq = AppointmentQuerier(engine)
        await aq.add_note(
            appointment_id=appointment_id,
            author_id=user.user_id,  # NOTE: this is the user_id, not admin_id
            message=data.message,
        )

    async def appointment_register_donation(
        self,
        user: AdminUserRequired,
        appointment_id: int,
        data: RegisterDonationRequest,
        engine: DBConnection,
    ):
        await self._assert_appt_access(user.admin_id, appointment_id, engine)
        aq = AdminQuerier(engine)
        res = await aq.register_donation(
            appointment_id=appointment_id,
            amount_ml=data.amount_ml,
            is_blood_not_plasma=data.is_blood_not_plasma,
        )

        assert res is not None, "donation registration success but no id returned???"
        return RegisterDonationResponse(donation_id=res)

    async def register_interview(
        self,
        user: AdminUserRequired,
        donor_id: int,
        data: RegisterInterviewRequest,
        engine: DBConnection,
    ):
        # NOTE: no access asserted, interview can be performed by any admin
        aq = AdminQuerier(engine)
        await aq.register_interview(
            RegisterInterviewParams(
                interviewer_admin_id=user.admin_id,
                donor_id=donor_id,
                ok_to_donate=data.ok_to_donate,
                time=data.submitted_at,
                validity_duration=data.validity_duration,
            )
        )

    async def register_donation_test(
        self,
        user: AdminUserRequired,
        donor_id: int,
        data: RegisterDonationTestRequest,
        engine: DBConnection,
    ):
        aq = AdminQuerier(engine)

        # check that donation was given by donor
        info = await aq.get_donation_info(donation_id=data.donation_id)
        if info is None or info.donor_id != donor_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Provided donation was not given by provided donor",
            )

        # admin has access to the blood bank where the donation was given
        await self._assert_bb_access(user.admin_id, info.bloodbank_id, engine)
        await aq.register_donation_test(
            RegisterDonationTestParams(
                donation_id=data.donation_id,
                tester_admin_id=user.admin_id,
                donor_id=donor_id,
                ok_to_donate=data.ok_to_donate,
                time=data.submitted_at,
                validity_duration=data.validity_duration,
            )
        )

    async def get_testresult_for_appointment_admin(
        self, appointment_id: int, user: AdminUserRequired, engine: DBConnection
    ) -> Donation:
        q = TestresultQuerier(engine)
        a = AuthQuerier(engine)

        access = await a.has_admin_where_appointment_is(
            admin_id=user.admin_id, appointment_id=appointment_id
        )

        if not access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not admin for this appointment",
            )

        donation: Donation | None = await q.donation_test_for_appointment(
            appointment_id=appointment_id
        )

        if donation is None:
            raise HTTPException(
                status_code=404,
                detail="No test results found for appointment",
            )

        return donation
