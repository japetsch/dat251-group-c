"""
From https://no.wikipedia.org/wiki/Offentlig_fridag:

Offentlige fridager i Norge

I Norge er søndag en offentlig fridag. Det samme er de følgende ti dagene.
  - 1. januar, 1. nyttårsdag
  - Skjærtorsdag
  - Langfredag
  - 2. påskedag
  - 1. mai
  - 17. mai
  - Kristi himmelfartsdag
  - 2. pinsedag
  - 25. desember, 1. juledag
  - 26. desember, 2. juledag
"""

from datetime import date, datetime, time, timedelta

from app.lib.ical import Frequency, RecurrenceRule, RecurrentEvent


def _yearly(summary: str, month: int, day: int) -> RecurrentEvent:
    """An all-day, fixed-date holiday that recurs every year."""
    return RecurrentEvent(
        summary=summary,
        dtstart=datetime(1970, month, day),
        duration=timedelta(days=1),
        rrule=RecurrenceRule(
            freq=Frequency.YEARLY,
            bymonth=[month],
            bymonthday=[day],
        ),
    )


STANDARD_HOLIDAYS = (
    _yearly("1. nyttårsdag", 1, 1),
    _yearly("1. mai", 5, 1),
    _yearly("17. mai", 5, 17),
    _yearly("1. juledag", 12, 25),
    _yearly("2. juledag", 12, 26),
)


# Movable holidays cannot be expressed as a single iCalendar RRULE: Easter is
# computed from the lunar calendar (the "computus") rather than from any
# fixed-date or weekday rule. Three workable approaches:
#
#   1. Compute Easter for each year in some window and materialize the holiday
#      as a list of RDATEs (no RRULE). Simple and self-contained, but bounded
#      to the precomputed range. Implemented below.
#
#   2. Extend RecurrenceRule with a non-standard "easter_offset" part and
#      teach the expander to anchor each yearly period to Easter Sunday
#      instead of (BYMONTH, BYMONTHDAY). Cleanest for unbounded recurrence,
#      but requires changing the core class.
#
#   3. Skip the recurrence model entirely and just expose a function
#      `holidays_for_year(year) -> list[date]`. Most flexible if you only ever
#      query by year.
#
# We use approach (1) with a window of 1970..2100.


def easter_sunday(year: int) -> date:
    """Date of Easter Sunday in the given (Gregorian) year.

    Uses the anonymous Gregorian algorithm (Meeus / Jones / Butcher).
    """
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    L = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * L) // 451
    month = (h + L - 7 * m + 114) // 31
    day = ((h + L - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def _easter_relative(
    summary: str,
    offset_days: int,
    start_year: int = 1970,
    end_year: int = 2100,
) -> RecurrentEvent:
    """A holiday whose date each year is ``Easter Sunday + offset_days``.

    Materialized as explicit RDATEs over ``[start_year, end_year]``.
    """
    occurrences = [
        datetime.combine(
            easter_sunday(y) + timedelta(days=offset_days),
            time(0),
        )
        for y in range(start_year, end_year + 1)
    ]
    return RecurrentEvent(
        summary=summary,
        dtstart=occurrences[0],
        duration=timedelta(days=1),
        rdates=occurrences[1:],
    )


MOVABLE_HOLIDAYS = (
    _easter_relative("Skjærtorsdag", -3),
    _easter_relative("Langfredag", -2),
    _easter_relative("2. påskedag", 1),
    _easter_relative("Kristi himmelfartsdag", 39),
    _easter_relative("2. pinsedag", 50),
)
