"""
Implementation of iCalendar (RFC 5545) recurrent events. Supports:
  * RRULE with FREQ, INTERVAL, COUNT, UNTIL
  * BYMONTH, BYMONTHDAY, BYDAY (with ordinals like 1MO, -1FR),
    BYHOUR, BYMINUTE, BYSECOND, BYSETPOS, WKST
  * EXDATE  (exception dates)
  * RDATE   (additional one-off dates)
  * Timezone-aware datetimes via ``zoneinfo`` with wall-clock semantics:
    "Mondays at 08:00 in Europe/Oslo" stays at 08:00 local time year-round,
    so DST transitions are absorbed automatically.
  * Round-trip serialization via ``to_ical()`` / ``from_ical()``.
"""

import calendar
import heapq
import re
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from enum import Enum
from typing import Any, Self
from zoneinfo import ZoneInfo


class Frequency(Enum):
    SECONDLY = "SECONDLY"
    MINUTELY = "MINUTELY"
    HOURLY = "HOURLY"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"


_WEEKDAY_NAMES = ("MO", "TU", "WE", "TH", "FR", "SA", "SU")
_BYDAY_RE = re.compile(r"^(-?\d+)?(MO|TU|WE|TH|FR|SA|SU)$")


@dataclass(frozen=True)
class Weekday:
    """A weekday, optionally qualified by an ordinal (e.g. ``1MO``, ``-1FR``).

    Use the module-level constants ``MO, TU, WE, TH, FR, SA, SU``. Call them
    with an integer to get an ordinal: ``MO(1)`` -> 1MO, ``FR(-1)`` -> -1FR.
    """

    weekday: int  # 0 = Monday ... 6 = Sunday
    n: int | None = None  # 1, 2, ... or -1, -2, ... (BYDAY ordinal)

    def __call__(self, n: int) -> Self:
        return type(self)(self.weekday, n)

    def __str__(self) -> str:
        return f"{self.n if self.n else ''}{_WEEKDAY_NAMES[self.weekday]}"


MO, TU, WE, TH, FR, SA, SU = (Weekday(i) for i in range(7))


def _parse_byday(s: str) -> Weekday:
    m = _BYDAY_RE.match(s.strip().upper())
    if not m:
        raise ValueError(f"Invalid BYDAY value: {s!r}")
    n = int(m.group(1)) if m.group(1) else None
    return Weekday(_WEEKDAY_NAMES.index(m.group(2)), n)


def _parse_ical_datetime(s: str) -> datetime:
    """Parse an iCalendar DATE or DATE-TIME value (UTC if suffixed with ``Z``)."""
    s = s.strip()
    if s.endswith("Z"):
        return datetime.strptime(s, "%Y%m%dT%H%M%SZ").replace(tzinfo=ZoneInfo("UTC"))
    if "T" in s:
        return datetime.strptime(s, "%Y%m%dT%H%M%S")
    return datetime.strptime(s, "%Y%m%d")


@dataclass
class RecurrenceRule:
    """An iCalendar-style RRULE.

    The :meth:`occurrences` method takes a ``dtstart`` and yields the resulting
    occurrence datetimes (potentially infinite — bound with ``COUNT``,
    ``UNTIL``, or by slicing from the caller).
    """

    freq: Frequency
    interval: int = 1
    count: int | None = None
    until: datetime | None = None

    bysecond: list[int] | None = None
    byminute: list[int] | None = None
    byhour: list[int] | None = None
    byday: list[Weekday] | None = None
    bymonthday: list[int] | None = None
    byyearday: list[int] | None = None
    byweekno: list[int] | None = None
    bymonth: list[int] | None = None
    bysetpos: list[int] | None = None

    wkst: int = 0  # 0 = Monday (RFC 5545 default)

    def to_ical(self) -> str:
        """Serialize as the value-side of an RRULE: line."""
        parts = [f"FREQ={self.freq.value}"]
        if self.interval != 1:
            parts.append(f"INTERVAL={self.interval}")
        if self.count is not None:
            parts.append(f"COUNT={self.count}")
        if self.until is not None:
            u = (
                self.until.astimezone(ZoneInfo("UTC"))
                if self.until.tzinfo
                else self.until
            )
            parts.append(f"UNTIL={u.strftime('%Y%m%dT%H%M%SZ')}")
        if self.wkst != 0:
            parts.append(f"WKST={_WEEKDAY_NAMES[self.wkst]}")
        for name, value in (
            ("BYMONTH", self.bymonth),
            ("BYWEEKNO", self.byweekno),
            ("BYYEARDAY", self.byyearday),
            ("BYMONTHDAY", self.bymonthday),
            ("BYDAY", self.byday),
            ("BYHOUR", self.byhour),
            ("BYMINUTE", self.byminute),
            ("BYSECOND", self.bysecond),
            ("BYSETPOS", self.bysetpos),
        ):
            if value:
                parts.append(f"{name}=" + ",".join(str(v) for v in value))
        return ";".join(parts)

    @classmethod
    def from_ical(cls, s: str) -> Self:
        """Parse an RRULE value, with or without a leading ``RRULE:`` prefix."""
        s = s.strip()
        if s.upper().startswith("RRULE:"):
            s = s[6:]

        parsed: dict[str, str] = {}
        for part in s.split(";"):
            if not part:
                continue
            key, _, value = part.partition("=")
            parsed[key.strip().upper()] = value.strip()

        if "FREQ" not in parsed:
            raise ValueError("RRULE must contain FREQ")

        kwargs: dict[str, Any] = {"freq": Frequency(parsed["FREQ"])}
        if "INTERVAL" in parsed:
            kwargs["interval"] = int(parsed["INTERVAL"])
        if "COUNT" in parsed:
            kwargs["count"] = int(parsed["COUNT"])
        if "UNTIL" in parsed:
            kwargs["until"] = _parse_ical_datetime(parsed["UNTIL"])
        if "WKST" in parsed:
            kwargs["wkst"] = _WEEKDAY_NAMES.index(parsed["WKST"])

        for ical_key, attr in [
            ("BYSECOND", "bysecond"),
            ("BYMINUTE", "byminute"),
            ("BYHOUR", "byhour"),
            ("BYMONTHDAY", "bymonthday"),
            ("BYYEARDAY", "byyearday"),
            ("BYWEEKNO", "byweekno"),
            ("BYMONTH", "bymonth"),
            ("BYSETPOS", "bysetpos"),
        ]:
            if ical_key in parsed:
                kwargs[attr] = [int(v) for v in parsed[ical_key].split(",")]

        if "BYDAY" in parsed:
            kwargs["byday"] = [_parse_byday(d) for d in parsed["BYDAY"].split(",")]

        return cls(**kwargs)

    def occurrences(self, dtstart: datetime) -> Iterator[datetime]:
        """Yield occurrence datetimes generated by this rule from ``dtstart``.

        May be infinite if neither ``COUNT`` nor ``UNTIL`` is set; callers
        should impose their own bound.
        """
        if self.freq in (Frequency.HOURLY, Frequency.MINUTELY, Frequency.SECONDLY):
            yield from self._stepped(dtstart)
            return

        periods: Iterator[date]
        expand: Callable[[datetime, date], Iterator[datetime]]
        match self.freq:
            case Frequency.YEARLY:
                periods = self._yearly_periods(dtstart)
                expand = self._expand_year
            case Frequency.MONTHLY:
                periods = self._monthly_periods(dtstart)
                expand = self._expand_month
            case Frequency.WEEKLY:
                periods = self._weekly_periods(dtstart)
                expand = self._expand_week
            case Frequency.DAILY:
                periods = self._daily_periods(dtstart)
                expand = self._expand_day
            case _:
                return

        count = 0
        empty_streak = 0
        for period in periods:
            candidates = sorted(set(expand(dtstart, period)))

            if self.bysetpos:
                picked = []
                for pos in self.bysetpos:
                    idx = pos - 1 if pos > 0 else len(candidates) + pos
                    if 0 <= idx < len(candidates):
                        picked.append(candidates[idx])
                candidates = sorted(set(picked))

            if not candidates:
                empty_streak += 1
                if empty_streak > 10_000:
                    return
                continue
            empty_streak = 0

            for dt in candidates:
                if dt < dtstart:
                    continue
                if self.until is not None and dt > self.until:
                    return
                yield dt
                count += 1
                if self.count is not None and count >= self.count:
                    return

    def _daily_periods(self, dtstart: datetime) -> Iterator[date]:
        d = dtstart.date()
        while True:
            yield d
            d += timedelta(days=self.interval)

    def _weekly_periods(self, dtstart: datetime) -> Iterator[date]:
        d = dtstart.date()
        d -= timedelta(days=(d.weekday() - self.wkst) % 7)
        while True:
            yield d
            d += timedelta(weeks=self.interval)

    def _monthly_periods(self, dtstart: datetime) -> Iterator[date]:
        y, m = dtstart.year, dtstart.month
        while True:
            yield date(y, m, 1)
            m += self.interval
            while m > 12:
                m -= 12
                y += 1

    def _yearly_periods(self, dtstart: datetime) -> Iterator[date]:
        y = dtstart.year
        while True:
            yield date(y, 1, 1)
            y += self.interval

    def _times_for(self, dtstart: datetime) -> Iterator[time]:
        base = dtstart.time()
        hours = self.byhour or [base.hour]
        minutes = self.byminute or [base.minute]
        seconds = self.bysecond or [base.second]
        for h in hours:
            for mi in minutes:
                for s in seconds:
                    yield time(h, mi, s, base.microsecond)

    @staticmethod
    def _combine(d: date, t: time, dtstart: datetime) -> datetime:
        """Combine date + time, attaching dtstart's timezone with wall-clock
        semantics: the UTC offset is re-resolved per calendar date so DST
        transitions are handled correctly.
        """
        return datetime.combine(d, t, tzinfo=dtstart.tzinfo)

    @staticmethod
    def _resolve_monthday(d: int, days_in_month: int) -> int | None:
        real = d if d > 0 else days_in_month + d + 1
        return real if 1 <= real <= days_in_month else None

    def _expand_day(self, dtstart: datetime, day: date) -> Iterator[datetime]:
        if self.bymonth and day.month not in self.bymonth:
            return
        if self.bymonthday:
            dim = calendar.monthrange(day.year, day.month)[1]
            allowed = {self._resolve_monthday(d, dim) for d in self.bymonthday}
            if day.day not in allowed:
                return
        if self.byday and not any(w.weekday == day.weekday() for w in self.byday):
            return
        for t in self._times_for(dtstart):
            yield self._combine(day, t, dtstart)

    def _expand_week(self, dtstart: datetime, week_start: date) -> Iterator[datetime]:
        days = self.byday or [Weekday(dtstart.weekday())]
        for wd in days:
            offset = (wd.weekday - self.wkst) % 7
            day = week_start + timedelta(days=offset)
            if self.bymonth and day.month not in self.bymonth:
                continue
            for t in self._times_for(dtstart):
                yield self._combine(day, t, dtstart)

    def _days_in_month_matching(self, dtstart: datetime, y: int, m: int) -> set[int]:
        dim = calendar.monthrange(y, m)[1]
        selected: set[int] = set()

        if self.bymonthday:
            for d in self.bymonthday:
                real = self._resolve_monthday(d, dim)
                if real is not None:
                    selected.add(real)

        if self.byday:
            for wd in self.byday:
                matching = [
                    d
                    for d in range(1, dim + 1)
                    if date(y, m, d).weekday() == wd.weekday
                ]
                if wd.n is None:
                    selected.update(matching)
                else:
                    idx = wd.n - 1 if wd.n > 0 else len(matching) + wd.n
                    if 0 <= idx < len(matching):
                        selected.add(matching[idx])

        if not self.bymonthday and not self.byday:
            d = dtstart.day
            if d <= dim:
                selected.add(d)

        return selected

    def _expand_month(self, dtstart: datetime, month_start: date) -> Iterator[datetime]:
        y, m = month_start.year, month_start.month
        if self.bymonth and m not in self.bymonth:
            return
        for d in sorted(self._days_in_month_matching(dtstart, y, m)):
            day = date(y, m, d)
            for t in self._times_for(dtstart):
                yield self._combine(day, t, dtstart)

    def _expand_year(self, dtstart: datetime, year_start: date) -> Iterator[datetime]:
        y = year_start.year
        months = self.bymonth or [dtstart.month]
        for m in months:
            for d in sorted(self._days_in_month_matching(dtstart, y, m)):
                day = date(y, m, d)
                for t in self._times_for(dtstart):
                    yield self._combine(day, t, dtstart)

    def _stepped(self, dtstart: datetime) -> Iterator[datetime]:
        if self.freq == Frequency.HOURLY:
            step = timedelta(hours=self.interval)
        elif self.freq == Frequency.MINUTELY:
            step = timedelta(minutes=self.interval)
        else:
            step = timedelta(seconds=self.interval)

        current = dtstart
        count = 0
        while True:
            if self.until is not None and current > self.until:
                return
            if (
                (not self.bymonth or current.month in self.bymonth)
                and (not self.byhour or current.hour in self.byhour)
                and (not self.byminute or current.minute in self.byminute)
                and (not self.bysecond or current.second in self.bysecond)
                and (
                    not self.byday
                    or any(w.weekday == current.weekday() for w in self.byday)
                )
            ):
                yield current
                count += 1
                if self.count is not None and count >= self.count:
                    return
            current += step


@dataclass
class EventOccurrence:
    """A single materialized occurrence of a recurrent event."""

    start: datetime
    end: datetime
    summary: str = ""
    description: str = ""
    location: str = ""

    @property
    def duration(self) -> timedelta:
        return self.end - self.start

    def __repr__(self) -> str:
        return f"<EventOccurrence {self.summary!r} {self.start.isoformat()}>"


@dataclass
class RecurrentEvent:
    """An iCalendar-style VEVENT with optional recurrence.

    The event's length is given by ``duration`` (defaulting to zero); the
    :attr:`dtend` property is computed as ``dtstart + duration``. To construct
    from an end time instead, use :meth:`with_dtend`.

    Pass a timezone-aware ``dtstart`` (constructed with ``ZoneInfo``) to get
    wall-clock semantics: a "Mondays at 08:00 in Europe/Oslo" rule will sit at
    08:00 local time on every Monday whether DST is in force or not. With a
    naive ``dtstart`` you get floating time (no zone).
    """

    summary: str
    dtstart: datetime
    duration: timedelta = timedelta(0)
    description: str = ""
    location: str = ""
    rrule: RecurrenceRule | None = None
    exdates: list[datetime] = field(default_factory=list)
    rdates: list[datetime] = field(default_factory=list)

    @property
    def dtend(self) -> datetime:
        """Computed end time (``dtstart + duration``)."""
        return self.dtstart + self.duration

    @classmethod
    def with_dtend(
        cls,
        *,
        summary: str,
        dtstart: datetime,
        dtend: datetime,
        description: str = "",
        location: str = "",
        rrule: RecurrenceRule | None = None,
        exdates: list[datetime] | None = None,
        rdates: list[datetime] | None = None,
    ) -> Self:
        """Construct an event from an explicit end time instead of duration."""
        return cls(
            summary=summary,
            dtstart=dtstart,
            duration=dtend - dtstart,
            description=description,
            location=location,
            rrule=rrule,
            exdates=exdates if exdates is not None else [],
            rdates=rdates if rdates is not None else [],
        )

    def occurrences(
        self,
        start: datetime | None = None,
        end: datetime | None = None,
        max_count: int | None = None,
    ) -> Iterator[EventOccurrence]:
        """Yield occurrences in ``[start, end)``, optionally capped at
        ``max_count``. For an infinite RRULE you must pass at least one of
        ``end`` or ``max_count`` to avoid hanging.
        """
        emitted = 0
        for dt in self._raw_occurrences():
            if end is not None and dt >= end:
                break
            if start is not None and dt < start:
                continue
            yield EventOccurrence(
                start=dt,
                end=dt + self.duration,
                summary=self.summary,
                description=self.description,
                location=self.location,
            )
            emitted += 1
            if max_count is not None and emitted >= max_count:
                break

    def between(self, start: datetime, end: datetime) -> list[EventOccurrence]:
        """Materialize occurrences in a window."""
        return list(self.occurrences(start=start, end=end))

    def _raw_occurrences(self) -> Iterator[datetime]:
        if self.rrule is not None:
            rrule_stream: Iterator[datetime] = self.rrule.occurrences(self.dtstart)
        else:
            rrule_stream = iter([self.dtstart])
        rdate_stream = iter(sorted(self.rdates))
        exset = set(self.exdates)

        last: datetime | None = None
        for dt in heapq.merge(rrule_stream, rdate_stream):
            if dt == last:
                continue
            last = dt
            if dt in exset:
                continue
            yield dt
