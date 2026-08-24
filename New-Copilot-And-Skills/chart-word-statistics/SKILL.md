---
name: chart-word-statistics
description: >-
  Create a downloadable horizontal bar-chart PNG from the Markdown table produced
  by the count-words skill. Use when given Word and Count columns and asked to
  visualize word frequencies, word statistics, or word-count results.
---

# Chart word statistics

Always run the bundled chart-generation script. Do not manually draw the chart and do not stop after describing the workflow.

## Required input

Accept the complete Markdown table returned by the `count-words` skill. The expected structure is:

```markdown
| Word | Count |
|---|---:|
| and | 5 |
| lorem | 3 |
```

The parser accepts surrounding whitespace and either column alignment. It rejects malformed rows, duplicate words, non-integer counts, negative counts, and tables without the `Word` and `Count` headers.

If no valid data rows are present, ask the user to provide a non-empty word-count table.

## Executable workflow

1. Save or pass the complete word-count table to `scripts/chart_word_statistics.py` through standard input.
2. Select a writable output path outside the skill directory ending in `.png`.
3. Run the script from this skill's root directory in the skill script execution environment.
4. Pass the output path with `--output`.
5. Read the JSON success object printed to stdout.
6. Confirm that the file named by `output` exists and return that PNG as the deliverable.

Run the script with an invocation equivalent to:

```text
scripts/chart_word_statistics.py --output "/writable/output/word-statistics.png"
```

Provide the Markdown table through stdin rather than placing it in a shell command argument. The script is non-interactive and supports `--help`. A nonzero exit status is an error; report stderr and do not return a partial chart.

## Chart behavior

- Produce a horizontal bar chart so words remain readable.
- Display the most frequent word at the top.
- Preserve the incoming row order from the count-words table.
- Label every bar with its exact integer count.
- Set the title to `Word Frequency` and the axes to `Count` and `Word`.
- Scale chart height to the number of words.
- Include every input word; do not truncate the table.

## Response

On success, attach only the generated PNG chart. Do not return the input table, JSON status object, script, or any intermediate file.
