#!/usr/bin/env python3
"""Validate extracted leave values and print the required JSON object."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date


def optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def optional_iso_date(value: str | None, label: str) -> str | None:
    value = optional_text(value)
    if value is None:
        return None
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"{label} must use YYYY-MM-DD format")
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise ValueError(f"{label} is not a valid calendar date") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Format extracted leave values as JSON")
    parser.add_argument("--fullname")
    parser.add_argument("--department")
    parser.add_argument("--last-day-off")
    parser.add_argument("--first-day-off")
    args = parser.parse_args()

    try:
        first = optional_iso_date(args.first_day_off, "first day off")
        last = optional_iso_date(args.last_day_off, "last day off")
        if first is not None and last is not None and last < first:
            raise ValueError("last day off must not be earlier than first day off")
        result = {
            "Fullname": optional_text(args.fullname),
            "Department": optional_text(args.department),
            "LastDayOff": last,
            "FirstDayOff": first,
        }
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
