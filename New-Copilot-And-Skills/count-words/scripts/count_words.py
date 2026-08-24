#!/usr/bin/env python3
"""Count Unicode words from stdin and print a frequency table."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter

# Unicode letters/numbers with optional internal straight or curly apostrophes.
WORD_RE = re.compile(r"[^\W_]+(?:['’][^\W_]+)*", re.UNICODE)


def count_words(text: str) -> list[tuple[str, int]]:
    """Return case-insensitive word counts ordered by count then word."""
    counts = Counter(match.group(0).casefold() for match in WORD_RE.finditer(text))
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))


def markdown_table(rows: list[tuple[str, int]]) -> str:
    lines = ["| Word | Count |", "|---|---:|"]
    for word, count in rows:
        safe_word = word.replace("|", "\\|")
        lines.append(f"| {safe_word} | {count} |")
    return "\n".join(lines)


def json_output(rows: list[tuple[str, int]]) -> str:
    return json.dumps(
        [{"Word": word, "Count": count} for word, count in rows],
        ensure_ascii=False,
        separators=(",", ":"),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Count words read from standard input and print a frequency table."
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format (default: markdown)",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    text = sys.stdin.read()
    rows = count_words(text)
    if args.format == "json":
        print(json_output(rows))
    else:
        print(markdown_table(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
