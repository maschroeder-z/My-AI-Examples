---
name: fill-leave-request-form
description: >-
  Create a completed PDF leave-request form from a full name, department, first
  day off, last day off, and duration. Use when asked to fill or generate the
  bundled leave request PDF and return the completed PDF file.
---

# Fill leave request form

Always run the bundled PDF-generation script. Do not merely describe the process. On success, return the generated PDF file as the only deliverable.

## Bundled resources

- `assets/leave_request_form.pdf`: the fillable template; never overwrite it.
- `scripts/fill_leave_request.py`: the only authorized PDF generator and verifier.

## Single-artifact invariant

Generate exactly one completed PDF. The file returned by the bundled script is the
immutable `leave-request-form` artifact and is the only PDF that may be attached,
uploaded, or otherwise delivered.

- Choose the final deterministic output path before running the script and retain
  that exact path for the entire request.
- Never create an upload copy, optimized copy, flattened copy, preview PDF, or
  fallback PDF.
- Never modify the output after the script reports success. In particular, do not
  rewrite it with pypdf, ReportLab, Ghostscript, qpdf, or another PDF library.
- On an explicit retry, run the bundled script against the same output path with
  `--overwrite`. Do not choose a new filename or timestamp.
- If a downstream system cannot consume the exact returned file as binary, stop
  and report the integration error. Never regenerate a smaller PDF to work around
  transport or context-length limits.

## Required inputs

Obtain all five values before execution:

1. Full name
2. Department
3. First day off
4. Last day off
5. Duration

Do not infer a missing value. Ask for it. Preserve the user's name, department, and duration after trimming surrounding whitespace. Normalize unambiguous dates to `YYYY-MM-DD`; ask about ambiguous dates. The last day must be on or after the first day.

## PDF field mapping

| Input | PDF field |
|---|---|
| Full name | `Name` |
| Department | `Department` |
| First day off | `FirstDay` |
| Last day off | `LastDay` |
| Duration | `Duration` |

## Executable workflow

1. Select a writable output path ending in `.pdf` outside the skill directory.
2. Run `scripts/fill_leave_request.py` from this skill's root directory in the skill script execution environment.
3. Supply all six required options: `--name`, `--department`, `--first-day`, `--last-day`, `--duration`, and `--output`.
4. Use arguments equivalent to the following, replacing every sample value with the real value:

```text
scripts/fill_leave_request.py --name "Erika Mustermann" --department "Product Development" --first-day "2026-09-14" --last-day "2026-09-18" --duration "5" --output "/writable/output/leave-request-erika-mustermann.pdf"
```

The script is non-interactive and supports `--help`. It locates `assets/leave_request_form.pdf` relative to itself, creates the output directory when needed, writes a new PDF, and verifies all five saved field values. A first attempt fails if the output already exists. An explicit retry must reuse the same path and add `--overwrite`.

On success, the script prints one JSON object with this contract:

```json
{
  "status": "success",
  "output": "/absolute/path/to/the-single-generated.pdf",
  "media_type": "application/pdf",
  "size_bytes": 0,
  "sha256": "lowercase SHA-256 digest"
}
```

`size_bytes` and `sha256` identify the exact immutable artifact. A nonzero exit status is an error; report stderr and do not return or upload a partial PDF.

## Binary handoff to SharePoint or another destination

1. Read the exact `output` path from the JSON result and bind that file to the
   variable `leave-request-form`.
2. Pass the file attachment or a trusted binary file handle directly to the upload
   action. Do not print, paste, or manually reconstruct the PDF bytes in the model
   context.
3. If the integration receives Base64, decode it inside the trusted connector or
   Power Automate flow before SharePoint `Create file`; do not decode by generating
   another PDF.
4. Upload with the same filename. For retries, enable overwrite and reuse the same
   destination path.
5. Verify that the uploaded byte size and, when retrievable, SHA-256 equal the
   script's `size_bytes` and `sha256`. A filename-only check is insufficient.
6. If the uploader accepts only inline text and cannot accept the returned binary
   artifact, halt. This is an integration failure, not permission to create a
   replacement PDF.

## Response

When execution succeeds:

1. Read the `output`, `size_bytes`, and `sha256` values from the JSON printed by the script.
2. Confirm that the exact output file exists and still matches both integrity values.
3. Attach or upload that exact PDF without copying, rewriting, optimizing, or Base64-printing it.
4. Do not return the template, JSON, Markdown, a second PDF, or any other file.
