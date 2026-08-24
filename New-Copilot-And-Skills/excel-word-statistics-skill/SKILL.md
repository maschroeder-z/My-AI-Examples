---
name: excel-word-statistics
description: >-
  Generate a downloadable Excel workbook containing every Word and Count row from
  the Markdown table produced by the count-words skill. Use when asked to export,
  save, or convert word-frequency or word-count results to Excel or XLSX.
---

# Excel word statistics

Always run the bundled workbook-generation script. Do not manually construct the workbook and do not stop after describing the workflow.

## Required input

Accept the complete Markdown table returned by the `count-words` skill. The expected structure is:

```markdown
| Word | Count |
|---|---:|
| and | 5 |
| lorem | 3 |
```

The parser accepts surrounding whitespace and either column alignment. It rejects malformed rows, duplicate words, non-integer counts, negative counts, and tables without exactly the `Word` and `Count` headers. A header-only table is valid and produces a header-only workbook.

If the user supplies raw text rather than a word-count table, invoke `count-words` first and pass its complete Markdown table to this skill.

## Executable workflow

1. Pass the complete word-count Markdown table to `scripts/excel_word_statistics.py` through standard input.
2. Select a writable output path outside the skill directory ending in `.xlsx`.
3. Run the script from this skill's root directory in the skill script execution environment.
4. Pass the output path with `--output`.
5. Read the JSON success object printed to stdout.
6. Confirm that the file named by `output` exists and return that XLSX file as the deliverable.

Run the script with an invocation equivalent to:

```text
scripts/excel_word_statistics.py --output "/writable/output/word-statistics.xlsx"
```

Provide the complete table through stdin rather than placing untrusted content in a shell command argument. The script is non-interactive and supports `--help`. A nonzero exit status is an error; report stderr and do not return a partial workbook.

## Workbook behavior

- Create one worksheet named `Word Statistics`.
- Write the exact columns `Word` and `Count` and include every input data row without truncation.
- Preserve the incoming row order from the `count-words` table.
- Store every count as an integer.
- Freeze the header row, enable filtering, style the headers, and size columns for readability.
- Add an Excel table named `WordStatistics` when at least one data row exists.

## Response

On success, attach only the generated XLSX workbook. Do not return the input table, JSON status object, script, or intermediate files.
