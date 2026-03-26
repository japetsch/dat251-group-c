from typing import List, TypedDict

from fastapi import HTTPException
from fastapi.routing import APIRouter

from app.auth import DonorUserRequired
from app.db.sqlc import models

from ..db.db import DBConnection
from ..db.sqlc.auth import AsyncQuerier as AuthQuerier
from ..db.sqlc.testresults import (
    AsyncQuerier as TestresultQuerier,
    DonationTestDetailsRow,
    DonationTestResultRow,
    EntryFormDetailsRow,
    EntryFormResultRow,
    InterviewDetailsRow,
    InterviewResultRow,
)


class TestresultRouter(APIRouter):
    def __init__(self) -> None:
        super().__init__()

        self.add_api_route("", self.get_all_testresults, methods=["GET"])
        self.add_api_route("/{testresult_id}", self.get_testresult, methods=["GET"])

    class InterviewResponse(TypedDict):
        interviews: List[InterviewResultRow]
        entry_forms: List[EntryFormResultRow]
        donation_tests: List[DonationTestResultRow]

    async def get_all_testresults(
        self, user: DonorUserRequired, engine: DBConnection
    ) -> TestresultRouter.InterviewResponse:
        q = TestresultQuerier(engine)

        interviews: list[InterviewResultRow] = []
        async for x in q.interview_result(donor_id=user.donor_id):
            interviews.append(x)

        entry_forms: list[EntryFormResultRow] = []
        async for x in q.entry_form_result(donor_id=user.donor_id):
            entry_forms.append(x)

        donation_tests: list[DonationTestResultRow] = []
        async for x in q.donation_test_result(donor_id=user.donor_id):
            donation_tests.append(x)

        return {
            "interviews": interviews,
            "entry_forms": entry_forms,
            "donation_tests": donation_tests,
        }

    async def get_testresult(
        self, testresult_id: int, user: DonorUserRequired, engine: DBConnection
    ) -> InterviewDetailsRow | DonationTestDetailsRow | EntryFormDetailsRow:
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
            return interview_details

        if (
            entry_form_details := await q.entry_form_details(
                testresult_id=testresult_id
            )
        ) is not None:
            return entry_form_details

        if (
            donation_test_details := await q.donation_test_details(
                testresult_id=testresult_id
            )
        ) is not None:
            return donation_test_details

        raise HTTPException(
            status_code=404,
            detail="Test result not found",
        )
