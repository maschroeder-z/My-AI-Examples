---
name: count-words
description: >-
  Count occurrences of every word in supplied text and return a Markdown table
  with Word and Count columns. Use when asked for word frequencies, repeated-word
  counts, vocabulary counts, or a table of words occurring in a passage.
---

# Count words

Always run the bundled counting script. Do not estimate or manually count the words.

## Input

Use the complete text supplied by the user. If no text is supplied, ask for it.

## Counting rules

- Compare words case-insensitively, so `Word`, `word`, and `WORD` are one word.
- Return words in lowercase.
- A word is a sequence of Unicode letters or numbers and may contain internal apostrophes such as `don't` or `l'été`.
- Treat punctuation, quotation marks, dashes, and whitespace as separators.
- Do not count standalone punctuation.
- Sort results by descending count, then alphabetically by word when counts are equal.

## Executable workflow

1. Pass the supplied text to `scripts/count_words.py` through standard input.
2. Run the script from this skill's root directory in the skill script execution environment.
3. Request Markdown-table output with `--format markdown`.
4. Return exactly the table printed to stdout. Do not add commentary or wrap it in a code fence.

Run the script with an invocation equivalent to:

```text
scripts/count_words.py --format markdown
```

Provide the complete input text through stdin rather than placing untrusted text in a shell command argument. The script is non-interactive and supports `--help`. A nonzero exit status is an error; report stderr instead of inventing a result.

## Output contract

Return a Markdown table with exactly these columns:

```markdown
| Word | Count |
|---|---:|
| and | 5 |
| lorem | 3 |
```

For empty input or input containing no words, return only the header and separator rows.
