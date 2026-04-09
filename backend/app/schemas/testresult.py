from typing import List, TypedDict

from ..db.sqlc.testresults import (
    DonationTestResultRow,
    EntryFormResultRow,
    InterviewResultRow,
)


class InterviewResponse(TypedDict):
    interviews: List[InterviewResultRow]
    entry_forms: List[EntryFormResultRow]
    donation_tests: List[DonationTestResultRow]
