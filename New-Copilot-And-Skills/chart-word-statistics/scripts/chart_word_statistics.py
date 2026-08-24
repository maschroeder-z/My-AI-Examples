#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "matplotlib>=3.8,<4",
# ]
# ///
"""Create a PNG bar chart from a count-words Markdown table read from stdin."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

SEPARATOR_CELL = re.compile(r"^:?-{3,}:?$")


def split_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        raise ValueError(f"invalid Markdown table row: {line!r}")
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def parse_markdown_table(text: str) -> list[tuple[str, int]]:
    lines = [line for line in text.splitlines() if line.strip()]
    if len(lines) < 3:
        raise ValueError("input must contain a Markdown table with Word and Count columns")

    header = split_row(lines[0])
    if [cell.casefold() for cell in header] != ["word", "count"]:
        raise ValueError("table headers must be Word and Count")

    separator = split_row(lines[1])
    if len(separator) != 2 or not all(SEPARATOR_CELL.fullmatch(c) for c in separator):
        raise ValueError("the second row must be a Markdown table separator")

    rows: list[tuple[str, int]] = []
    seen: set[str] = set()
    for line_number, line in enumerate(lines[2:], start=3):
        cells = split_row(line)
        if len(cells) != 2:
            raise ValueError(f"row {line_number} must contain exactly two columns")
        word = cells[0].replace("\\|", "|").strip()
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

    if not rows:
        raise ValueError("the word-count table has no data rows")
    return rows


def create_chart(rows: list[tuple[str, int]], output: Path) -> Path:
    output = output.expanduser().resolve()
    if output.suffix.lower() != ".png":
        raise ValueError("output filename must end in .png")

    words = [word for word, _ in rows]
    counts = [count for _, count in rows]
    height = max(4.0, min(50.0, 0.42 * len(rows) + 1.8))
    width = 10.0

    fig, ax = plt.subplots(figsize=(width, height))
    positions = list(range(len(rows)))
    bars = ax.barh(positions, counts, color="#4472C4")
    ax.set_yticks(positions, labels=words)
    ax.invert_yaxis()
    ax.set_xlabel("Count")
    ax.set_ylabel("Word")
    ax.set_title("Word Frequency")
    ax.xaxis.get_major_locator().set_params(integer=True)
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)

    maximum = max(counts, default=0)
    offset = max(maximum * 0.01, 0.05)
    ax.set_xlim(0, max(1.0, maximum + max(offset * 6, 0.5)))
    for bar, count in zip(bars, counts):
        ax.text(
            bar.get_width() + offset,
            bar.get_y() + bar.get_height() / 2,
            str(count),
            va="center",
            ha="left",
        )

    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(fig)

    if not output.is_file() or output.stat().st_size == 0:
        raise RuntimeError("chart output was not created")
    return output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a PNG bar chart from a count-words Markdown table on stdin."
    )
    parser.add_argument("--output", required=True, type=Path, help="Output PNG path")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        rows = parse_markdown_table(sys.stdin.read())
        output = create_chart(rows, args.output)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": "success", "output": str(output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
