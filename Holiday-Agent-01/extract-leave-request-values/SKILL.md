---
name: extract-leave-request-values
description: >-
  Extract the requester's full name, department, first day off, and last day off
  from an email body or leave-request message and return JSON. Use when supplied
  text contains vacation, absence, annual-leave, or time-off details.
---

# Extract leave request values

Follow this workflow whenever this skill is selected. Do not stop after describing the workflow.

## Required input

Use the complete email body supplied by the user. Use sender name, sender address, subject, or sent date only when included with that input. Do not search for a different email.

## Workflow

1. Read the newest non-quoted part of the supplied message.
2. Determine the person taking leave, their department, and the leave interval using the rules below.
3. Normalize unambiguous dates to `YYYY-MM-DD`.
4. Run the bundled script `scripts/format_extraction.py` from this skill's root directory. Pass each known value with its corresponding option. Omit the option for any unknown value.
5. Return exactly the JSON printed to stdout. Do not wrap it in a Markdown fence.

Run the script in the skill script execution environment with arguments equivalent to:

```text
scripts/format_extraction.py --fullname "Erika Mustermann" --department "Product Development" --first-day-off "2026-09-14" --last-day-off "2026-09-18"
```

Available options are `--fullname`, `--department`, `--first-day-off`, and `--last-day-off`. The script is non-interactive and supports `--help`. A nonzero exit status is an error; report stderr instead of inventing output.

## Extraction rules

- Prefer explicit statements in the newest non-quoted message.
- Use the signature name when it clearly belongs to the requester.
- If leave is explicitly requested for another person, use that person's name.
- Do not select an approver, manager, recipient, replacement, or a person found only in quoted history.
- Use only an explicitly stated department. Do not infer it from a title, domain, project, or recipient.
- Select the leave dates, not the sent date, approval date, return date, deadline, or legal-notice dates.
- For a single leave date, use that date as both first and last day.
- For a date range, use the earlier endpoint as first day and the later endpoint as last day.
- Resolve relative dates only when a reliable reference date is included in the supplied input.
- Do not guess ambiguous numeric dates. Leave the affected value unknown.
- Preserve Unicode and capitalization for names and departments; trim surrounding whitespace.
- If multiple equally current requests cannot be distinguished, leave non-unique values unknown.

## Output contract

The script prints exactly these keys in this order, with JSON `null` for unknown values:

```json
{
  "Fullname": null,
  "Department": null,
  "LastDayOff": null,
  "FirstDayOff": null
}
```
