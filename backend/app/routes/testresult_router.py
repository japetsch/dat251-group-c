from fastapi import HTTPException
from fastapi.routing import APIRouter

from app.auth import DonorUserRequired

from ..db.db import DBConnection
from ..db.sqlc.auth import AsyncQuerier as AuthQuerier
from ..db.sqlc.testresults import (
    AsyncQuerier as TestresultQuerier,
)
from ..schemas.testresult import (
    DonationTestDetailsDTO,
    DonationTestResultDTO,
    EntryFormDetailsDTO,
    EntryFormResultDTO,
    InterviewDetailsDTO,
    InterviewResponse,
    InterviewResultDTO,
)


class TestresultRouter(APIRouter):
    def __init__(self) -> None:
        super().__init__()

        self.add_api_route("", self.get_all_testresults, methods=["GET"])
        self.add_api_route("/{testresult_id}", self.get_testresult, methods=["GET"])

    async def get_all_testresults(
        self, user: DonorUserRequired, engine: DBConnection
    ) -> InterviewResponse:
        q = TestresultQuerier(engine)

        interviews: list[InterviewResultDTO] = []
        async for x in q.interview_result(donor_id=user.donor_id):
            interviews.append(InterviewResultDTO.map(x))

        entry_forms: list[EntryFormResultDTO] = []
        async for x in q.entry_form_result(donor_id=user.donor_id):
            entry_forms.append(EntryFormResultDTO.map(x))

        donation_tests: list[DonationTestResultDTO] = []
        async for x in q.donation_test_result(donor_id=user.donor_id):
            donation_tests.append(DonationTestResultDTO.map(x))

        return {
            "interviews": interviews,
            "entry_forms": entry_forms,
            "donation_tests": donation_tests,
        }

    async def get_testresult(
        self, testresult_id: int, user: DonorUserRequired, engine: DBConnection
    ) -> InterviewDetailsDTO | DonationTestDetailsDTO | EntryFormDetailsDTO:
        q = TestresultQuerier(engine)
        aq = AuthQuerier(engine)

        access = await aq.test_result_belongs_to(
            donor_id=user.donor_id, testresult_id=testresult_id
        )

        if not access:
            raise HTTPException(
                status_code=404,
                detail="Test result for diffenrent user",
            )

        if (
            interview_details := await q.interview_details(testresult_id=testresult_id)
        ) is not None:
            return InterviewDetailsDTO.map(interview_details)

        if (
            entry_form_details := await q.entry_form_details(
                testresult_id=testresult_id
            )
        ) is not None:
            return EntryFormDetailsDTO.map(entry_form_details)

        if (
            donation_test_details := await q.donation_test_details(
                testresult_id=testresult_id
            )
        ) is not None:
            return DonationTestDetailsDTO.map(donation_test_details)

        raise HTTPException(
            status_code=404,
            detail="Test result not found",
        )
