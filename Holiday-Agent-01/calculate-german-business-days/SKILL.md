---
name: calculate-german-business-days
description: >-
  Calculate inclusive total calendar days and Monday-to-Friday business days
  between two dates, excluding German nationwide public holidays and optional
  state-specific holidays. Use for German leave-duration and workday calculations.
---

# Calculate German business days

Always run the bundled calculation script. Do not calculate the result manually and do not stop after describing the workflow.

## Inputs

- Start date: required, normalized to `YYYY-MM-DD`.
- End date: required, normalized to `YYYY-MM-DD`.
- State: optional, using a German postal two-letter state code, case-insensitive.

Ask for clarification if a required date is absent or ambiguous. The end date must be on or after the start date.

Supported state codes are `BB`, `BE`, `BW`, `BY`, `HB`, `HE`, `HH`, `MV`, `NI`, `NW`, `RP`, `SH`, `SL`, `SN`, `ST`, and `TH`.

## Executable workflow

1. Normalize the dates and, if present, uppercase the state code.
2. Run `scripts/calculate_days.py` from this skill's root directory in the skill script execution environment.
3. Pass `--start-date`, `--end-date`, and, only when provided, `--state`.
4. Return exactly the JSON printed to stdout, without a Markdown fence or additional prose.

With a state, run arguments equivalent to:

```text
scripts/calculate_days.py --start-date "2026-09-14" --end-date "2026-09-18" --state "BY"
```

Without a state, run arguments equivalent to:

```text
scripts/calculate_days.py --start-date "2026-09-14" --end-date "2026-09-18"
```

The script is non-interactive and supports `--help`. A nonzero exit status is an error; report stderr instead of inventing a result.

## Definitions

Both endpoints are included.

- `CalculateBusinessDays`: Monday through Friday excluding German nationwide public holidays.
- `CalculateBusinessDaysWithState`: when state is present, Monday through Friday excluding nationwide and state-wide holidays for that state; otherwise `null`.
- `State`: resolved German state long name when state is present; otherwise `null`.
- `TotalDays`: inclusive calendar days without exclusions.

Only holidays valid throughout the entire state are excluded. Municipality-specific holidays are not excluded because a state code cannot identify them.

## Output contract

```json
{
  "CalculateBusinessDays": 0,
  "CalculateBusinessDaysWithState": null,
  "State": null,
  "TotalDays": 0
}
```
