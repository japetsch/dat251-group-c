"""Pytest tests for icalendar_recurrence."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from app.lib.ical import (
    FR,
    MO,
    SA,
    SU,
    TH,
    TU,
    WE,
    EventOccurrence,
    Frequency,
    RecurrenceRule,
    RecurrentEvent,
    Weekday,
)

OSLO = ZoneInfo("Europe/Oslo")
UTC = ZoneInfo("UTC")


@pytest.fixture
def weekday_standup() -> RecurrentEvent:
    """A weekday standup, 14 occurrences from Mon May 4 2026."""
    return RecurrentEvent(
        summary="Standup",
        dtstart=datetime(2026, 5, 4, 9, 30),
        duration=timedelta(minutes=30),
        rrule=RecurrenceRule(
            freq=Frequency.DAILY,
            byday=[MO, TU, WE, TH, FR],
            count=14,
        ),
    )


class TestBasicRecurrence:
    def test_no_rrule_yields_single_occurrence(self) -> None:
        e = RecurrentEvent(
            summary="One-off",
            dtstart=datetime(2026, 5, 4, 9, 0),
            duration=timedelta(hours=1),
        )
        occs = list(e.occurrences())
        assert len(occs) == 1
        assert occs[0].start == datetime(2026, 5, 4, 9, 0)
        assert occs[0].end == datetime(2026, 5, 4, 10, 0)

    def test_daily_with_count(self) -> None:
        e = RecurrentEvent(
            summary="Daily",
            dtstart=datetime(2026, 5, 4, 8, 0),
            rrule=RecurrenceRule(freq=Frequency.DAILY, count=5),
        )
        occs = list(e.occurrences())
        assert len(occs) == 5
        assert [o.start.day for o in occs] == [4, 5, 6, 7, 8]

    def test_daily_with_until(self) -> None:
        e = RecurrentEvent(
            summary="Daily",
            dtstart=datetime(2026, 5, 4, 8, 0),
            rrule=RecurrenceRule(
                freq=Frequency.DAILY,
                until=datetime(2026, 5, 7, 23, 59),
            ),
        )
        occs = list(e.occurrences())
        assert [o.start.day for o in occs] == [4, 5, 6, 7]

    def test_daily_with_interval(self) -> None:
        e = RecurrentEvent(
            summary="Every 3 days",
            dtstart=datetime(2026, 5, 4, 8, 0),
            rrule=RecurrenceRule(freq=Frequency.DAILY, interval=3, count=5),
        )
        occs = list(e.occurrences())
        assert [o.start.day for o in occs] == [4, 7, 10, 13, 16]

    def test_weekly(self) -> None:
        e = RecurrentEvent(
            summary="Weekly",
            dtstart=datetime(2026, 5, 4, 8, 0),
            rrule=RecurrenceRule(freq=Frequency.WEEKLY, count=4),
        )
        occs = list(e.occurrences())
        assert [o.start for o in occs] == [
            datetime(2026, 5, 4, 8, 0),
            datetime(2026, 5, 11, 8, 0),
            datetime(2026, 5, 18, 8, 0),
            datetime(2026, 5, 25, 8, 0),
        ]

    def test_monthly_default_picks_dtstart_day(self) -> None:
        e = RecurrentEvent(
            summary="Monthly",
            dtstart=datetime(2026, 1, 15, 12, 0),
            rrule=RecurrenceRule(freq=Frequency.MONTHLY, count=4),
        )
        occs = list(e.occurrences())
        assert [(o.start.year, o.start.month, o.start.day) for o in occs] == [
            (2026, 1, 15),
            (2026, 2, 15),
            (2026, 3, 15),
            (2026, 4, 15),
        ]

    def test_yearly_default_picks_dtstart_month_day(self) -> None:
        e = RecurrentEvent(
            summary="Birthday",
            dtstart=datetime(2026, 6, 15, 0, 0),
            rrule=RecurrenceRule(freq=Frequency.YEARLY, count=3),
        )
        occs = list(e.occurrences())
        assert [(o.start.year, o.start.month, o.start.day) for o in occs] == [
            (2026, 6, 15),
            (2027, 6, 15),
            (2028, 6, 15),
        ]

    def test_hourly(self) -> None:
        e = RecurrentEvent(
            summary="Hourly check",
            dtstart=datetime(2026, 5, 4, 8, 0),
            rrule=RecurrenceRule(freq=Frequency.HOURLY, count=4),
        )
        occs = list(e.occurrences())
        assert [o.start.hour for o in occs] == [8, 9, 10, 11]


class TestByDay:
    def test_weekly_byday_count(self, weekday_standup: RecurrentEvent) -> None:
        occs = list(weekday_standup.occurrences())
        assert len(occs) == 14
        assert all(o.start.weekday() < 5 for o in occs)

    def test_weekly_byday_skips_weekends(self) -> None:
        e = RecurrentEvent(
            summary="Tu/Th",
            dtstart=datetime(2026, 5, 5, 14, 0),  # Tuesday
            rrule=RecurrenceRule(
                freq=Frequency.WEEKLY,
                byday=[TU, TH],
                count=4,
            ),
        )
        occs = list(e.occurrences())
        assert [(o.start.day, o.start.weekday()) for o in occs] == [
            (5, 1),
            (7, 3),
            (12, 1),
            (14, 3),
        ]

    def test_monthly_first_monday(self) -> None:
        e = RecurrentEvent(
            summary="Town hall",
            dtstart=datetime(2026, 1, 5, 16, 0),
            rrule=RecurrenceRule(freq=Frequency.MONTHLY, byday=[MO(1)], count=6),
        )
        occs = list(e.occurrences())
        assert [o.start.day for o in occs] == [5, 2, 2, 6, 4, 1]
        assert all(o.start.weekday() == 0 for o in occs)

    def test_monthly_last_friday(self) -> None:
        e = RecurrentEvent(
            summary="Demos",
            dtstart=datetime(2026, 1, 30, 15, 0),
            rrule=RecurrenceRule(freq=Frequency.MONTHLY, byday=[FR(-1)], count=6),
        )
        occs = list(e.occurrences())
        assert [o.start.day for o in occs] == [30, 27, 27, 24, 29, 26]
        assert all(o.start.weekday() == 4 for o in occs)


class TestBySetPos:
    def test_last_weekday_of_month(self) -> None:
        e = RecurrentEvent(
            summary="Month-end",
            dtstart=datetime(2026, 1, 30, 17, 0),
            rrule=RecurrenceRule(
                freq=Frequency.MONTHLY,
                byday=[MO, TU, WE, TH, FR],
                bysetpos=[-1],
                count=6,
            ),
        )
        occs = list(e.occurrences())
        assert [(o.start.month, o.start.day) for o in occs] == [
            (1, 30),
            (2, 27),
            (3, 31),
            (4, 30),
            (5, 29),
            (6, 30),
        ]


class TestByMonthDay:
    def test_last_day_of_each_month(self) -> None:
        e = RecurrentEvent(
            summary="Payroll",
            dtstart=datetime(2026, 1, 31),
            rrule=RecurrenceRule(
                freq=Frequency.MONTHLY,
                bymonthday=[-1],
                count=6,
            ),
        )
        occs = list(e.occurrences())
        # 2026 is not a leap year — Feb has 28 days.
        assert [o.start.day for o in occs] == [31, 28, 31, 30, 31, 30]

    def test_quarterly_on_15th(self) -> None:
        e = RecurrentEvent(
            summary="Quarterly",
            dtstart=datetime(2026, 1, 15, 12, 0),
            rrule=RecurrenceRule(
                freq=Frequency.MONTHLY,
                interval=3,
                bymonthday=[15],
                count=4,
            ),
        )
        occs = list(e.occurrences())
        assert [(o.start.month, o.start.day) for o in occs] == [
            (1, 15),
            (4, 15),
            (7, 15),
            (10, 15),
        ]


class TestByHour:
    def test_three_times_a_day(self) -> None:
        e = RecurrentEvent(
            summary="Medication",
            dtstart=datetime(2026, 5, 4, 8, 0),
            rrule=RecurrenceRule(
                freq=Frequency.DAILY,
                byhour=[8, 14, 20],
                count=9,
            ),
        )
        occs = list(e.occurrences())
        assert [(o.start.day, o.start.hour) for o in occs] == [
            (4, 8),
            (4, 14),
            (4, 20),
            (5, 8),
            (5, 14),
            (5, 20),
            (6, 8),
            (6, 14),
            (6, 20),
        ]


class TestExDateRDate:
    def test_exdate_skips_occurrence(self) -> None:
        e = RecurrentEvent(
            summary="Daily",
            dtstart=datetime(2026, 5, 4, 8, 0),
            rrule=RecurrenceRule(freq=Frequency.DAILY, count=5),
            exdates=[datetime(2026, 5, 6, 8, 0)],
        )
        starts = [o.start for o in e.occurrences()]
        assert datetime(2026, 5, 6, 8, 0) not in starts
        assert len(starts) == 4

    def test_rdate_adds_occurrence(self) -> None:
        e = RecurrentEvent(
            summary="Yearly",
            dtstart=datetime(2024, 12, 25, 0, 0),
            rrule=RecurrenceRule(freq=Frequency.YEARLY, count=3),
            rdates=[datetime(2025, 6, 15, 0, 0)],
        )
        starts = [o.start for o in e.occurrences()]
        assert datetime(2025, 6, 15, 0, 0) in starts
        assert datetime(2025, 12, 25, 0, 0) in starts

    def test_combined_exdate_rdate(self) -> None:
        e = RecurrentEvent(
            summary="Christmas",
            dtstart=datetime(2024, 12, 25, 0, 0),
            rrule=RecurrenceRule(freq=Frequency.YEARLY, count=4),
            exdates=[datetime(2026, 12, 25, 0, 0)],
            rdates=[datetime(2026, 6, 15, 0, 0)],
        )
        starts = [o.start for o in e.occurrences()]
        assert datetime(2026, 12, 25, 0, 0) not in starts
        assert datetime(2026, 6, 15, 0, 0) in starts


class TestTimezone:
    def test_oslo_dst_spring_forward(self) -> None:
        """Across the Mar 29 spring-forward boundary, 08:00 local stays 08:00."""
        e = RecurrentEvent(
            summary="Standup",
            dtstart=datetime(2026, 3, 23, 8, 0, tzinfo=OSLO),
            rrule=RecurrenceRule(freq=Frequency.WEEKLY, byday=[MO], count=4),
        )
        occs = list(e.occurrences())
        assert all(o.start.hour == 8 for o in occs)
        assert occs[0].start.utcoffset() == timedelta(hours=1)  # CET
        assert occs[1].start.utcoffset() == timedelta(hours=2)  # CEST
        assert occs[1].start.astimezone(UTC).hour == 6  # 08:00 +02:00 = 06:00Z

    def test_oslo_dst_fall_back(self) -> None:
        e = RecurrentEvent(
            summary="Standup",
            dtstart=datetime(2026, 10, 19, 8, 0, tzinfo=OSLO),
            rrule=RecurrenceRule(freq=Frequency.WEEKLY, byday=[MO], count=4),
        )
        occs = list(e.occurrences())
        assert all(o.start.hour == 8 for o in occs)
        assert occs[0].start.utcoffset() == timedelta(hours=2)  # CEST
        assert occs[1].start.utcoffset() == timedelta(hours=1)  # CET

    def test_until_in_utc_against_local_dtstart(self) -> None:
        rule = RecurrenceRule.from_ical("FREQ=WEEKLY;BYDAY=MO;UNTIL=20260601T000000Z")
        e = RecurrentEvent(
            summary="Standup",
            dtstart=datetime(2026, 5, 4, 8, 0, tzinfo=OSLO),
            rrule=rule,
        )
        occs = list(e.occurrences())
        # Mondays May 4, 11, 18, 25; Jun 1 at 08:00 Oslo = 06:00 UTC > UNTIL.
        assert [o.start.day for o in occs] == [4, 11, 18, 25]

    def test_naive_datetimes_remain_floating(self) -> None:
        e = RecurrentEvent(
            summary="Floating",
            dtstart=datetime(2026, 5, 4, 9, 30),
            rrule=RecurrenceRule(freq=Frequency.DAILY, count=3),
        )
        assert all(o.start.tzinfo is None for o in e.occurrences())


class TestSerialization:
    @pytest.mark.parametrize(
        "ical_string",
        [
            "FREQ=DAILY;COUNT=14;BYDAY=MO,TU,WE,TH,FR",
            "FREQ=WEEKLY;INTERVAL=2;BYDAY=TU,TH;UNTIL=20260630T235900Z",
            "FREQ=MONTHLY;COUNT=12;BYDAY=1MO",
            "FREQ=MONTHLY;COUNT=12;BYDAY=MO,TU,WE,TH,FR;BYSETPOS=-1",
            "FREQ=MONTHLY;COUNT=12;BYMONTHDAY=-1",
            "FREQ=YEARLY;BYMONTH=12;BYMONTHDAY=25",
            "FREQ=DAILY;COUNT=9;BYHOUR=8,14,20",
        ],
    )
    def test_round_trip(self, ical_string: str) -> None:
        rule = RecurrenceRule.from_ical(ical_string)
        again = RecurrenceRule.from_ical(rule.to_ical())
        assert rule == again

    def test_strips_rrule_prefix(self) -> None:
        rule = RecurrenceRule.from_ical("RRULE:FREQ=DAILY;COUNT=5")
        assert rule.freq == Frequency.DAILY
        assert rule.count == 5

    def test_requires_freq(self) -> None:
        with pytest.raises(ValueError, match="FREQ"):
            RecurrenceRule.from_ical("COUNT=5")

    def test_invalid_byday_token(self) -> None:
        with pytest.raises(ValueError, match="BYDAY"):
            RecurrenceRule.from_ical("FREQ=WEEKLY;BYDAY=XX")

    def test_byday_ordinals_parse(self) -> None:
        rule = RecurrenceRule.from_ical("FREQ=MONTHLY;BYDAY=1MO,-1FR")
        assert rule.byday == [MO(1), FR(-1)]

    def test_to_ical_omits_default_interval(self) -> None:
        rule = RecurrenceRule(freq=Frequency.DAILY, count=3)
        assert "INTERVAL" not in rule.to_ical()


class TestApi:
    def test_dtend_property_computed_from_duration(self) -> None:
        e = RecurrentEvent(
            summary="Hour",
            dtstart=datetime(2026, 5, 4, 9, 0),
            duration=timedelta(hours=1),
        )
        assert e.dtend == datetime(2026, 5, 4, 10, 0)

    def test_with_dtend_classmethod(self) -> None:
        e = RecurrentEvent.with_dtend(
            summary="Meeting",
            dtstart=datetime(2026, 5, 4, 9, 0),
            dtend=datetime(2026, 5, 4, 10, 30),
        )
        assert e.duration == timedelta(hours=1, minutes=30)
        assert e.dtend == datetime(2026, 5, 4, 10, 30)

    def test_default_duration_is_zero(self) -> None:
        e = RecurrentEvent(
            summary="Instant",
            dtstart=datetime(2026, 5, 4, 9, 0),
        )
        assert e.duration == timedelta(0)
        assert e.dtend == e.dtstart

    def test_between_window(self, weekday_standup: RecurrentEvent) -> None:
        occs = weekday_standup.between(
            datetime(2026, 5, 11),
            datetime(2026, 5, 18),
        )
        assert all(
            datetime(2026, 5, 11) <= o.start < datetime(2026, 5, 18) for o in occs
        )
        assert [o.start.day for o in occs] == [11, 12, 13, 14, 15]

    def test_max_count_caps_results(self, weekday_standup: RecurrentEvent) -> None:
        assert len(list(weekday_standup.occurrences(max_count=3))) == 3

    def test_occurrence_carries_event_metadata(self) -> None:
        e = RecurrentEvent(
            summary="Standup",
            description="Daily team sync",
            location="Zoom",
            dtstart=datetime(2026, 5, 4, 9, 30),
            rrule=RecurrenceRule(freq=Frequency.DAILY, count=2),
        )
        occ = next(iter(e.occurrences()))
        assert occ.summary == "Standup"
        assert occ.description == "Daily team sync"
        assert occ.location == "Zoom"

    def test_occurrence_duration(self) -> None:
        e = RecurrentEvent(
            summary="Hour-long",
            dtstart=datetime(2026, 5, 4, 9, 0),
            duration=timedelta(hours=1),
            rrule=RecurrenceRule(freq=Frequency.DAILY, count=1),
        )
        occ = next(iter(e.occurrences()))
        assert occ.duration == timedelta(hours=1)


class TestRecurrenceRuleDirect:
    """RecurrenceRule.occurrences works standalone, without an event wrapper."""

    def test_direct_daily(self) -> None:
        rule = RecurrenceRule(freq=Frequency.DAILY, count=3)
        dts = list(rule.occurrences(datetime(2026, 5, 4, 9, 0)))
        assert dts == [
            datetime(2026, 5, 4, 9, 0),
            datetime(2026, 5, 5, 9, 0),
            datetime(2026, 5, 6, 9, 0),
        ]

    def test_direct_weekly_byday(self) -> None:
        rule = RecurrenceRule(freq=Frequency.WEEKLY, byday=[WE, FR], count=4)
        dts = list(rule.occurrences(datetime(2026, 5, 6, 9, 0)))  # Wed
        assert [(d.day, d.weekday()) for d in dts] == [
            (6, 2),
            (8, 4),
            (13, 2),
            (15, 4),
        ]


class TestWeekday:
    def test_str_no_ordinal(self) -> None:
        assert str(MO) == "MO"
        assert str(FR) == "FR"

    def test_str_with_ordinal(self) -> None:
        assert str(MO(1)) == "1MO"
        assert str(FR(-1)) == "-1FR"

    def test_call_creates_new_instance(self) -> None:
        wd = MO(2)
        assert wd.weekday == 0
        assert wd.n == 2
        assert wd is not MO  # didn't mutate
