from datetime import datetime, timedelta
from typing import List, Optional, TypedDict

from pydantic import BaseModel

from ..db.sqlc.testresults import (
    DonationTestDetailsRow,
    DonationTestResultRow,
    EntryFormDetailsRow,
    EntryFormResultRow,
    InterviewDetailsRow,
    InterviewResultRow,
)


class DonationTestDetailsDTO(BaseModel):
    id: int
    donor_id: int
    form_id: int
    time: datetime
    validity_duration: timedelta
    invalidated: bool
    ok_to_donate: bool
    donation_test_id: Optional[int]
    donation_id: int
    tester_admin_id: int
    appointment_id: int
    amount_ml: float
    is_blood_not_plasma: bool
    tester_admin_name: str

    @staticmethod
    def map(row: DonationTestDetailsRow) -> DonationTestDetailsDTO:
        return DonationTestDetailsDTO(
            id=row.id,
            donor_id=row.donor_id,
            form_id=row.form_id,
            time=row.time,
            validity_duration=row.validity_duration,
            invalidated=row.invalidated,
            ok_to_donate=row.ok_to_donate,
            donation_test_id=row.donation_test_id,
            donation_id=row.donation_id,
            tester_admin_id=row.tester_admin_id,
            appointment_id=row.appointment_id,
            amount_ml=row.amount_ml,
            is_blood_not_plasma=row.is_blood_not_plasma,
            tester_admin_name=row.tester_admin_name,
        )


class DonationTestResultDTO(BaseModel):
    id: int
    donor_id: int
    form_id: int
    time: datetime
    validity_duration: timedelta
    invalidated: bool
    donation_test_id: Optional[int]
    admin_name: str

    @staticmethod
    def map(row: DonationTestResultRow) -> DonationTestResultDTO:
        return DonationTestResultDTO(
            id=row.id,
            donor_id=row.donor_id,
            form_id=row.form_id,
            time=row.time,
            validity_duration=row.validity_duration,
            invalidated=row.invalidated,
            donation_test_id=row.donation_test_id,
            admin_name=row.admin_name,
        )


class EntryFormDetailsDTO(BaseModel):
    id: int
    donor_id: int
    form_id: int
    time: datetime
    validity_duration: timedelta
    invalidated: bool
    ok_to_donate: bool
    entry_form_id: Optional[int]

    @staticmethod
    def map(row: EntryFormDetailsRow) -> EntryFormDetailsDTO:
        return EntryFormDetailsDTO(
            id=row.id,
            donor_id=row.donor_id,
            form_id=row.form_id,
            time=row.time,
            validity_duration=row.validity_duration,
            invalidated=row.invalidated,
            ok_to_donate=row.ok_to_donate,
            entry_form_id=row.entry_form_id,
        )


class EntryFormResultDTO(BaseModel):
    id: int
    donor_id: int
    form_id: int
    time: datetime
    validity_duration: timedelta
    invalidated: bool
    entry_form_id: Optional[int]

    @staticmethod
    def map(row: EntryFormResultRow) -> EntryFormResultDTO:
        return EntryFormResultDTO(
            id=row.id,
            donor_id=row.donor_id,
            form_id=row.form_id,
            time=row.time,
            validity_duration=row.validity_duration,
            invalidated=row.invalidated,
            entry_form_id=row.entry_form_id,
        )


class InterviewDetailsDTO(BaseModel):
    id: int
    donor_id: int
    form_id: int
    time: datetime
    validity_duration: timedelta
    invalidated: bool
    ok_to_donate: bool
    interview_id: Optional[int]
    interviewer_admin_id: int
    interviewer_admin_name: str

    @staticmethod
    def map(row: InterviewDetailsRow) -> InterviewDetailsDTO:
        return InterviewDetailsDTO(
            id=row.id,
            donor_id=row.donor_id,
            form_id=row.form_id,
            time=row.time,
            validity_duration=row.validity_duration,
            invalidated=row.invalidated,
            ok_to_donate=row.ok_to_donate,
            interview_id=row.interview_id,
            interviewer_admin_id=row.interviewer_admin_id,
            interviewer_admin_name=row.interviewer_admin_name,
        )


class InterviewResultDTO(BaseModel):
    id: int
    donor_id: int
    form_id: int
    time: datetime
    validity_duration: timedelta
    invalidated: bool
    interview_id: Optional[int]
    admin_name: str

    @staticmethod
    def map(row: InterviewResultRow) -> InterviewResultDTO:
        return InterviewResultDTO(
            id=row.id,
            donor_id=row.donor_id,
            form_id=row.form_id,
            time=row.time,
            validity_duration=row.validity_duration,
            invalidated=row.invalidated,
            interview_id=row.interview_id,
            admin_name=row.admin_name,
        )


class InterviewResponse(TypedDict):
    interviews: List[InterviewResultDTO]
    entry_forms: List[EntryFormResultDTO]
    donation_tests: List[DonationTestResultDTO]
