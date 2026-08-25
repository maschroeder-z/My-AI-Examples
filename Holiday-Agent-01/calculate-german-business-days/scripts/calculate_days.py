#!/usr/bin/env python3
"""Calculate inclusive German business days and calendar days as JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta

STATE_NAMES = {
    "BB": "Brandenburg",
    "BE": "Berlin",
    "BW": "Baden-Württemberg",
    "BY": "Bayern",
    "HB": "Bremen",
    "HE": "Hessen",
    "HH": "Hamburg",
    "MV": "Mecklenburg-Vorpommern",
    "NI": "Niedersachsen",
    "NW": "Nordrhein-Westfalen",
    "RP": "Rheinland-Pfalz",
    "SH": "Schleswig-Holstein",
    "SL": "Saarland",
    "SN": "Sachsen",
    "ST": "Sachsen-Anhalt",
    "TH": "Thüringen",
}


def parse_iso_date(value: str, label: str) -> date:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"{label} must use YYYY-MM-DD format: {value!r}")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{label} is not a valid calendar date: {value!r}") from exc


def normalize_state(value: str | None) -> str | None:
    if value is None or not value.strip():
        return None
    code = value.strip().upper()
    if code not in STATE_NAMES:
        raise ValueError("state must be one of: " + ", ".join(sorted(STATE_NAMES)))
    return code


def easter_sunday(year: int) -> date:
    """Gregorian Easter Sunday (Meeus/Jones/Butcher algorithm)."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    ell = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * ell) // 451
    month = (h + ell - 7 * m + 114) // 31
    day = (h + ell - 7 * m + 114) % 31 + 1
    return date(year, month, day)


def nationwide_holidays(year: int) -> set[date]:
    easter = easter_sunday(year)
    days = {
        date(year, 1, 1),
        easter - timedelta(days=2),
        easter + timedelta(days=1),
        date(year, 5, 1),
        easter + timedelta(days=39),
        easter + timedelta(days=50),
        date(year, 10, 3),
        date(year, 12, 25),
        date(year, 12, 26),
    }
    if year == 2017:
        days.add(date(year, 10, 31))
    return days


def state_holidays(year: int, state: str) -> set[date]:
    easter = easter_sunday(year)
    days: set[date] = set()

    if state in {"BW", "BY", "ST"}:
        days.add(date(year, 1, 6))
    if (state == "BE" and year >= 2019) or (state == "MV" and year >= 2023):
        days.add(date(year, 3, 8))
    if state == "BB":
        days.update({easter, easter + timedelta(days=49)})
    if state in {"BW", "BY", "HE", "NW", "RP", "SL"}:
        days.add(easter + timedelta(days=60))
    if state == "SL":
        days.add(date(year, 8, 15))
    if state == "TH" and year >= 2019:
        days.add(date(year, 9, 20))
    if state in {"BB", "MV", "SN", "ST", "TH"} or (
        state in {"HB", "HH", "NI", "SH"} and year >= 2018
    ):
        days.add(date(year, 10, 31))
    if state in {"BW", "BY", "NW", "RP", "SL"}:
        days.add(date(year, 11, 1))
    if state == "SN":
        november_23 = date(year, 11, 23)
        days.add(
            november_23
            - timedelta(days=(november_23.weekday() - 2) % 7 or 7)
        )
    return days


def holiday_set(start: date, end: date, state: str | None) -> set[date]:
    result: set[date] = set()
    for year in range(start.year, end.year + 1):
        result.update(nationwide_holidays(year))
        if state is not None:
            result.update(state_holidays(year, state))
    return result


def count_business_days(start: date, end: date, state: str | None) -> int:
    excluded = holiday_set(start, end, state)
    count = 0
    current = start
    while current <= end:
        if current.weekday() < 5 and current not in excluded:
            count += 1
        current += timedelta(days=1)
    return count


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Calculate inclusive German business and calendar days as JSON."
    )
    parser.add_argument("--start-date", required=True, help="ISO date: YYYY-MM-DD")
    parser.add_argument("--end-date", required=True, help="ISO date: YYYY-MM-DD")
    parser.add_argument("--state", help="Optional German two-letter state code")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        start = parse_iso_date(args.start_date, "start date")
        end = parse_iso_date(args.end_date, "end date")
        if end < start:
            raise ValueError("end date must be the same as or later than start date")
        state = normalize_state(args.state)
        result = {
            "CalculateBusinessDays": count_business_days(start, end, None),
            "CalculateBusinessDaysWithState": (
                count_business_days(start, end, state) if state else None
            ),
            "State": STATE_NAMES[state] if state else None,
            "TotalDays": (end - start).days + 1,
        }
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
