#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "openpyxl>=3.1,<4",
# ]
# ///
"""Create an XLSX workbook from a count-words Markdown table read from stdin."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.table import Table, TableStyleInfo

SEPARATOR_CELL = re.compile(r"^:?-{3,}:?$")


def split_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        raise ValueError(f"invalid Markdown table row: {line!r}")
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def parse_markdown_table(text: str) -> list[tuple[str, int]]:
    lines = [line for line in text.splitlines() if line.strip()]
    if len(lines) < 2:
        raise ValueError("input must contain a Markdown table with Word and Count columns")

    header = split_row(lines[0])
    if [cell.casefold() for cell in header] != ["word", "count"]:
        raise ValueError("table headers must be Word and Count")

    separator = split_row(lines[1])
    if len(separator) != 2 or not all(SEPARATOR_CELL.fullmatch(cell) for cell in separator):
        raise ValueError("the second row must be a Markdown table separator")

    rows: list[tuple[str, int]] = []
    seen: set[str] = set()
    for line_number, line in enumerate(lines[2:], start=3):
        cells = split_row(line)
        if len(cells) != 2:
            raise ValueError(f"row {line_number} must contain exactly two columns")
        word = cells[0].strip()
        if not word:
            raise ValueError(f"row {line_number} has an empty word")
        key = word.casefold()
        if key in seen:
            raise ValueError(f"row {line_number} contains duplicate word: {word!r}")
        seen.add(key)
        try:
            count = int(cells[1])
        except ValueError as exc:
            raise ValueError(f"row {line_number} count must be an integer") from exc
        if count < 0:
            raise ValueError(f"row {line_number} count must not be negative")
        rows.append((word, count))
    return rows


def create_workbook(rows: list[tuple[str, int]], output: Path) -> Path:
    output = output.expanduser().resolve()
    if output.suffix.lower() != ".xlsx":
        raise ValueError("output filename must end in .xlsx")

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Word Statistics"
    sheet.append(["Word", "Count"])
    for word, count in rows:
        sheet.append([word, count])

    header_fill = PatternFill(fill_type="solid", fgColor="4472C4")
    for cell in sheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center")

    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = f"A1:B{max(1, sheet.max_row)}"
    sheet.column_dimensions["A"].width = max(
        12, min(60, max((len(word) for word, _ in rows), default=4) + 2)
    )
    sheet.column_dimensions["B"].width = max(
        10, max((len(str(count)) for _, count in rows), default=5) + 2
    )
    for cell in sheet["B"][1:]:
        cell.number_format = "0"

    if rows:
        table = Table(displayName="WordStatistics", ref=f"A1:B{sheet.max_row}")
        table.tableStyleInfo = TableStyleInfo(
            name="TableStyleMedium2",
            showFirstColumn=False,
            showLastColumn=False,
            showRowStripes=True,
            showColumnStripes=False,
        )
        sheet.add_table(table)

    output.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(output)

    if not output.is_file() or output.stat().st_size == 0:
        raise RuntimeError("workbook output was not created")

    check = load_workbook(output, read_only=True, data_only=True)
    try:
        verified = check["Word Statistics"]
        values = list(verified.iter_rows(values_only=True))
        expected = [("Word", "Count"), *rows]
        if values != expected:
            raise RuntimeError("workbook verification failed: output data differs from input")
    finally:
        check.close()
    return output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create an XLSX workbook from a count-words Markdown table on stdin."
    )
    parser.add_argument("--output", required=True, type=Path, help="Output XLSX path")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        rows = parse_markdown_table(sys.stdin.read())
        output = create_workbook(rows, args.output)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": "success", "output": str(output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
