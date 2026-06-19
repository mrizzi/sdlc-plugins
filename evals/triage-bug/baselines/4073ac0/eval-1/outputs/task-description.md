# Jira API Metadata

The following parameters would be passed to `jira.create_issue`:

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: `["ai-generated-jira"]`

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix trailing-whitespace handling in plan-feature convention heading extraction so that CONVENTIONS.md headings with trailing spaces are correctly matched during convention-aware task enrichment. Currently, `line[3:]` preserves trailing whitespace, causing exact-match lookups to silently fail. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — strip trailing whitespace from heading extraction in the convention conformance analysis section

## Implementation Notes
The bug is in the convention conformance analysis loop in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The heading extraction uses:

```python
section_name = line[3:]
```

This preserves trailing whitespace from the heading line. When `CONVENTIONS.md` contains `## Migration Patterns  ` (with trailing spaces), the extracted key is `"Migration Patterns  "`, which fails the exact-match lookup `convention_name in discovered_conventions` in the task enrichment step.

**Fix**: Change the extraction to strip trailing whitespace:

```python
section_name = line[3:].strip()
```

**Reproducer test guidance** (derived from Steps to Reproduce):
- **Input**: A `CONVENTIONS.md` fixture with trailing whitespace on a heading, e.g., `## Migration Patterns  \n` (two trailing spaces after "Patterns").
- **Scenario**: Run the convention extraction logic on this fixture, then perform the convention-name lookup used in task enrichment.
- **Incorrect behavior (before fix)**: The convention name `"Migration Patterns"` is not found in the extracted conventions dictionary because the key is `"Migration Patterns  "` (with trailing spaces). The generated task's Implementation Notes omit the convention.
- **Correct behavior (after fix)**: The convention name `"Migration Patterns"` is found and the generated task's Implementation Notes include: `Per CONVENTIONS.md "Migration Patterns: add Index::create() for all FK columns.`

Existing test file `evals/plan-feature/files/conventions-mock.md` does not include trailing whitespace on headings — the reproducer test should create a new fixture or modify the existing one to include trailing whitespace.

Fixes ACME-500.

## Acceptance Criteria
- [ ] A reproducer test demonstrates the bug: a CONVENTIONS.md heading with trailing whitespace is correctly matched after the fix (the test fails before the fix and passes after)
- [ ] The convention heading extraction in plan-feature strips trailing whitespace from extracted section names
- [ ] Conventions with trailing whitespace on headings are included in the generated task's Implementation Notes
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with trailing whitespace on a heading (e.g., `## Migration Patterns  ` with trailing spaces), run the convention extraction and lookup logic, and assert that the convention name `"Migration Patterns"` is found in the extracted conventions dictionary and that the generated Implementation Notes contain the convention reference `Per CONVENTIONS.md`. The test must fail before the fix (convention not found due to trailing whitespace mismatch) and pass after (convention correctly matched).
- [ ] Verify that headings without trailing whitespace continue to be extracted correctly (no regression)
- [ ] Verify that headings with mixed trailing whitespace (spaces and tabs) are also handled

## Verification Commands
- Run plan-feature eval suite to confirm no regressions: `claude /plan-feature ACME-100` with the whitespace fixture and inspect the output task description

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md "Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction in plan-feature's convention conformance analysis uses `line[3:]` without stripping trailing whitespace. Headings with trailing spaces produce dictionary keys like `"Migration Patterns  "` that fail exact-match lookup against the expected `"Migration Patterns"`.
