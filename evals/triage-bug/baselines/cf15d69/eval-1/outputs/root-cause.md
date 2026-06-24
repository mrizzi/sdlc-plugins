# Root Cause Analysis - ACME-500

## What is broken

The plan-feature skill's convention conformance analysis silently drops conventions from `CONVENTIONS.md` when heading lines contain trailing whitespace. This causes generated task descriptions to omit conventions that should have been included, with no warning or error.

## Where it is broken

The defect is in the plan-feature convention lookup logic in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`.

The heading extraction code uses `line[3:]` to extract the section name after the `## ` prefix:

```python
section_name = line[3:]  # Does NOT strip trailing whitespace
```

When a heading line has trailing whitespace (e.g., `## Migration Patterns  `), the extracted section name retains those trailing spaces (`"Migration Patterns  "`). The downstream exact-match lookup then fails because it compares against the clean name `"Migration Patterns"` (without trailing spaces).

## Why it is broken

`line[3:]` is a simple string slice that captures everything from index 3 to the end of the line, including any trailing spaces or tabs. The fix is to strip trailing whitespace from the extracted heading text, e.g., `line[3:].strip()`.

Additionally, no warning is logged when a convention name fails to match during the task enrichment step, making this a silent failure that is difficult to diagnose.

## How to verify the fix

Write a reproducer test that:

1. Creates a `CONVENTIONS.md` fixture with trailing whitespace on a heading line (e.g., `## Migration Patterns  ` with two trailing spaces)
2. Runs the convention conformance analysis against this fixture
3. Asserts that the convention IS matched and included in the generated task's Implementation Notes
4. Specifically asserts the output contains: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`

The reproducer test should fail before the fix and pass after.
