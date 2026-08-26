#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "pypdf>=6.0,<7",
# ]
# ///
"""Fill and verify the bundled leave-request PDF without flattening it."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

from pypdf import PdfReader, PdfWriter

REQUIRED_FIELDS = {"Name", "Department", "FirstDay", "LastDay", "Duration", "State", "Manager" }


def nonempty(value: str, label: str) -> str:
    """Trim a required text value and reject an empty result."""
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{label} must not be empty")
    return cleaned


def parse_iso_date(value: str, label: str) -> date:
    """Parse a required date in unambiguous ISO format."""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"{label} must use YYYY-MM-DD format: {value!r}")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{label} is not a valid calendar date: {value!r}") from exc


def build_parser() -> argparse.ArgumentParser:
    skill_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description="Fill the bundled leave-request PDF and keep it editable."
    )
    parser.add_argument("--name", required=True, help="Full name")
    parser.add_argument("--department", required=True)
    parser.add_argument("--first-day", required=True, help="ISO date: YYYY-MM-DD")
    parser.add_argument("--last-day", required=True, help="ISO date: YYYY-MM-DD")
    parser.add_argument("--duration", required=True, help="Value for Duration field")
    parser.add_argument("--state", required=True)
    parser.add_argument("--manager", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the same planned output path on an explicit retry",
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=skill_root / "assets" / "leave_request_form.pdf",
        help=argparse.SUPPRESS,
    )
    return parser


def fill_pdf(
    template: Path,
    output: Path,
    values: dict[str, str],
    *,
    overwrite: bool,
) -> Path:
    """Fill the template, write a new PDF, and verify its field values."""
    template = template.expanduser().resolve()
    output = output.expanduser().resolve()

    if not template.is_file():
        raise FileNotFoundError(f"PDF template not found: {template}")
    if output.suffix.lower() != ".pdf":
        raise ValueError("output filename must end in .pdf")
    if output == template:
        raise ValueError("refusing to overwrite the PDF template")
    if output.exists() and not overwrite:
        raise FileExistsError(
            "output already exists; reuse this exact path with --overwrite only for "
            "an explicit retry"
        )

    reader = PdfReader(str(template))
    available = set((reader.get_fields() or {}).keys())
    missing = REQUIRED_FIELDS - available
    if missing:
        raise ValueError(
            "PDF template is missing required field(s): "
            + ", ".join(sorted(missing))
        )

    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    for page in writer.pages:
        writer.update_page_form_field_values(
            page,
            values,
            auto_regenerate=False,
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as handle:
        writer.write(handle)

    verification_reader = PdfReader(str(output))
    verification = verification_reader.get_fields() or {}
    for field_name, expected in values.items():
        actual = verification.get(field_name, {}).get("/V")
        if actual != expected:
            output.unlink(missing_ok=True)
            raise RuntimeError(
                f"verification failed for {field_name}: "
                f"expected {expected!r}, found {actual!r}"
            )

    if len(verification_reader.pages) != len(reader.pages):
        output.unlink(missing_ok=True)
        raise RuntimeError("verification failed: output page count changed")

    return output


def artifact_metadata(output: Path) -> dict[str, object]:
    """Describe the exact immutable PDF artifact for downstream binary upload."""
    digest = hashlib.sha256()
    with output.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return {
        "output": str(output),
        "media_type": "application/pdf",
        "size_bytes": output.stat().st_size,
        "sha256": digest.hexdigest(),
    }


def main() -> int:
    args = build_parser().parse_args()
    try:
        name = nonempty(args.name, "name")
        department = nonempty(args.department, "department")
        duration = nonempty(args.duration, "duration")
        first_day = parse_iso_date(args.first_day, "first day")
        last_day = parse_iso_date(args.last_day, "last day")        
        if last_day < first_day:
            raise ValueError("last day must be the same as or later than first day")
        state = nonempty(args.state, "state")
        manager = nonempty(args.manager, "manager")

        output = fill_pdf(
            template=args.template,
            output=args.output,
            values={
                "Name": name,
                "Department": department,
                "FirstDay": first_day.isoformat(),
                "LastDay": last_day.isoformat(),
                "Duration": duration,
                "State": state,
                "Manager": manager,
            },
            overwrite=args.overwrite,
        )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    result = {"status": "success", **artifact_metadata(output)}
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
