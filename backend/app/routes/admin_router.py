from datetime import datetime, timedelta, timezone
from typing import final
from zoneinfo import ZoneInfo

from fastapi import HTTPException, status
from fastapi.routing import APIRouter
from pydantic import BaseModel, Field

from app.auth import AdminUserRequired

from ..db.db import DBConnection
from ..db.sqlc.admin import (
    AsyncQuerier as AdminQuerier,
    CreateBloodBankParams,
    GetAllBloodBanksRow,
    GetAppointmentsAtBloodBankRow,
)
from ..db.sqlc.auth import AsyncQuerier as AuthQuerier
from ..db.sqlc.models import BloodType


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
        )
        self.add_api_route(
            "/bloodbank/{bloodbank_id}/admin/remove",
            self.remove_admin_from_bloodbank,
            methods=["DELETE"],
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
        )
        self.add_api_route(
            "/donor/{donor_id}/form/donation-test",
            self.register_donation_test,
            methods=["POST"],
        )

    async def list_bloodbanks(
        self, user: AdminUserRequired, engine: DBConnection
    ) -> list[GetAllBloodBanksRow]:
        """
        Lists all blood banks in the system, even the ones the logged in user is not adminstrator for

        TODO:
        - make accessible to everyone, even non-admins?
        - enhance with opening hours information
        - allow admins to list which people are admins
        """
        aq = AdminQuerier(engine)
        blood_banks: list[GetAllBloodBanksRow] = []
        async for r in aq.get_all_blood_banks(admin_id=user.admin_id):
            blood_banks.append(r)
        return blood_banks

    class CreateBloodBankRequest(BaseModel):
        name: str
        street_name: str
        street_number: str
        postal_code: str
        city: str
        country: str = "NO"
        # TODO: make optional + use geocoding
        loc_lat: float
        loc_lon: float

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

        return {  # TODO: improve OpenAPI model
            "bloodbank_id": res,
        }

    async def _assert_access(
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

    class MutateBloodbankAdminsRequest(BaseModel):
        admin_id: int

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
        await self._assert_access(user.admin_id, bloodbank_id, engine)
        aq = AdminQuerier(engine)
        await aq.add_blood_bank_admin(bloodbank_id=bloodbank_id, admin_id=data.admin_id)
        # TODO: success feedback?

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
        await self._assert_access(user.admin_id, bloodbank_id, engine)
        aq = AdminQuerier(engine)
        await aq.remove_blood_bank_admin(
            bloodbank_id=bloodbank_id, admin_id=data.admin_id
        )
        # TODO: success feedback?

    class BookingSlotType(GetAppointmentsAtBloodBankRow):
        appointments: list[AdminRouter.AppointmentType]

    class AppointmentType(BaseModel):
        appointment_id: int
        appointment_cancelled: bool
        donor_id: int
        donor_blood_type: BloodType | None
        donor_name: str
        donor_email: str
        donor_phone: str

    async def bloodbank_appointments(
        self,
        user: AdminUserRequired,
        bloodbank_id: int,
        engine: DBConnection,
        after: datetime | None = None,
        before: datetime | None = None,
        show_cancelled: bool = False,
    ) -> list[AdminRouter.BookingSlotType]:
        """
        Show appointments for blood bank.

        By default only the ones scheduled after 00:00 in Oslo on the same day
        """
        await self._assert_access(user.admin_id, bloodbank_id, engine)

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

        slots: list[AdminRouter.BookingSlotType] = []
        async for a in appts:
            slots.append(AdminRouter.BookingSlotType.model_validate(a))
        return slots

    class AppointmentNote(BaseModel):
        message: str

    async def appointment_add_note(
        self,
        user: AdminUserRequired,
        appointment_id: int,
        data: AppointmentNote,
        engine: DBConnection,
    ):
        pass

    class DonationInfo(BaseModel):
        amount_ml: float
        is_blood_not_plasma: bool = True

    async def appointment_register_donation(
        self,
        user: AdminUserRequired,
        appointment_id: int,
        data: DonationInfo,
        engine: DBConnection,
    ):
        pass

    class TestResult(BaseModel):
        submitted_at: datetime = Field(
            default_factory=lambda: datetime.now(tz=timezone.utc)
        )
        ok_to_donate: bool
        validity_duration: timedelta

    class InterviewForm(TestResult):
        pass

    async def register_interview(
        self,
        user: AdminUserRequired,
        donor_id: int,
        data: InterviewForm,
        engine: DBConnection,
    ):
        # NOTE: no access asserted, interview can be performed by any admin
        pass

    class DonationTestForm(TestResult):
        donation_id: int

    async def register_donation_test(
        self,
        user: AdminUserRequired,
        donor_id: int,
        data: DonationTestForm,
        engine: DBConnection,
    ):
        # TODO: assert admin has access to the blood bank where the donation was given
        # TODO: check that donation was given by donor
        pass
