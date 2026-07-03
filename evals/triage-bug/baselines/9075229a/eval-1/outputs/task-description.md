<!-- Jira API Metadata
jira.create_issue parameters:
  project_key: ACME
  issue_type: Task
  labels:
    - ai-generated-jira
-->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention heading extraction to strip trailing whitespace before storing section names, preventing silent convention drops when `CONVENTIONS.md` headings contain trailing spaces. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to the heading extraction line (`section_name = line[3:]`) to normalize section names

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- test fixture with trailing whitespace on heading lines for reproducer test

## Implementation Notes
The defect is in the convention heading extraction loop in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The current code:

```python
section_name = line[3:]  # Does NOT strip trailing whitespace
```

must be changed to:

```python
section_name = line[3:].strip()  # Strip trailing whitespace from heading
```

This ensures that heading lines like `## Migration Patterns  ` (with trailing spaces) are normalized to `"Migration Patterns"` before being stored in the conventions dictionary. The downstream exact-match lookup (`if convention_name in discovered_conventions`) will then succeed regardless of trailing whitespace in the source file.

**Reproducer test guidance**: The Steps to Reproduce from the bug specify:
1. Create a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  ` with two trailing spaces).
2. Run `/plan-feature` on a feature requiring that convention.
3. Assert the generated task's Implementation Notes include the convention reference (e.g., `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`).

The test should first verify the bug exists (convention is dropped with trailing whitespace) and then verify the fix resolves it (convention is included after the `.strip()` change).

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not include trailing whitespace on headings. The new fixture should mirror its structure but add trailing spaces to at least one heading line.

Consider also adding a warning log when a convention name lookup fails, to prevent future silent failures.

Fixes ACME-500.

## Acceptance Criteria
- [ ] A reproducer test demonstrates that CONVENTIONS.md headings with trailing whitespace are correctly matched (test fails before fix, passes after fix)
- [ ] The convention heading extraction normalizes section names by stripping trailing whitespace
- [ ] Generated task descriptions include convention references even when CONVENTIONS.md headings have trailing whitespace
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with trailing whitespace on heading lines (e.g., `## Migration Patterns  `), run convention conformance analysis, and assert the convention is matched and included in the generated task's Implementation Notes (expected: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`)
- [ ] Verify that headings without trailing whitespace continue to work correctly (no regression)
- [ ] Verify that headings with various whitespace patterns (tabs, mixed spaces) are handled

## Verification Commands
- `python3 -m pytest evals/plan-feature/ -v` -- all plan-feature evals should pass, including the new trailing-whitespace reproducer

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading line (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: "Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The convention heading extraction uses `line[3:]` without stripping trailing whitespace, causing the extracted section name (e.g., `"Migration Patterns  "`) to fail exact-match comparison against the expected clean name (`"Migration Patterns"`). The failure is silent with no warning logged.
