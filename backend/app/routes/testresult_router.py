from fastapi import HTTPException
from fastapi.routing import APIRouter

from app.auth import DonorUserRequired
from app.db.sqlc import models

from ..db.db import DBConnection
from ..db.sqlc.auth import AsyncQuerier as AuthQuerier
from ..db.sqlc.testresults import (
    AsyncQuerier as TestresultQuerier,
    TestResultRow,
)


class TestresultRouter(APIRouter):
    def __init__(self) -> None:
        super().__init__()

        self.add_api_route("", self.get_all_testresults, methods=["GET"])
        self.add_api_route("/{testresult_id}", self.get_testresult, methods=["GET"])

    async def get_all_testresults(
        self, user: DonorUserRequired, engine: DBConnection
    ) -> list[models.TestResult]:
        q = TestresultQuerier(engine)
        rows: list[models.TestResult] = []
        async for x in q.test_results(donor_id=user.donor_id):
            rows.append(x)

        return rows

    async def get_testresult(
        self, testresult_id: int, user: DonorUserRequired, engine: DBConnection
    ) -> TestResultRow:
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

        test_result: TestResultRow | None = await q.test_result(
            testresult_id=testresult_id
        )

        if not test_result:
            raise HTTPException(
                status_code=404,
                detail="Test result not found",
            )

        return test_result
