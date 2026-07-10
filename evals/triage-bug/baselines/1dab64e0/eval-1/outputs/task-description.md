<!-- Jira API metadata block: parameters for jira.create_issue -->
<!--
  project: ACME
  issuetype: Task
  labels: ["ai-generated-jira"]
  summary: "Fix plan-feature convention heading extraction to strip trailing whitespace"
-->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention conformance analysis to handle trailing whitespace on `CONVENTIONS.md` section headings. Currently, heading extraction uses `line[3:]` without stripping whitespace, causing conventions to be silently dropped when headings have trailing spaces. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- update convention heading extraction to strip trailing whitespace from `line[3:]`

## Implementation Notes
The bug is in the convention conformance analysis section of the plan-feature skill. The heading extraction logic currently reads:

```python
section_name = line[3:]  # Does NOT strip trailing whitespace
```

This must be changed to:

```python
section_name = line[3:].strip()
```

When `CONVENTIONS.md` contains a heading like `## Migration Patterns  ` (with trailing spaces), the current code stores the section name as `"Migration Patterns  "`. The downstream task enrichment step performs an exact match:

```python
if convention_name in discovered_conventions:
```

This match fails because the canonical name `"Migration Patterns"` does not equal the whitespace-padded key `"Migration Patterns  "`.

**Reproducer test guidance**: Create a `CONVENTIONS.md` fixture with trailing whitespace on a heading line:
```
## Migration Patterns  
Add Index::create() for all FK columns.
```
Run the convention conformance analysis against this fixture. Before the fix, the convention will be silently dropped (not included in the generated task's Implementation Notes). After the fix, the convention should appear as:
> Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.

**Existing test patterns**: The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` provides the structure for convention test fixtures but does not include trailing whitespace. Use it as a reference for the reproducer fixture format.

Consider also adding a warning log when a heading is extracted with leading/trailing whitespace, to surface similar issues in the future.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` -- existing convention fixture that can be used as a template for the reproducer test fixture

## Acceptance Criteria
- [ ] Reproducer test: a test with trailing whitespace on a `CONVENTIONS.md` heading demonstrates the bug (fails before the fix, passes after the fix)
- [ ] Convention headings with trailing whitespace are correctly matched during convention conformance analysis
- [ ] Conventions with trailing whitespace on headings are included in the generated task's Implementation Notes
- [ ] No regression in existing plan-feature tests and evals

## Test Requirements
- [ ] Reproducer test: create a `CONVENTIONS.md` fixture with trailing whitespace on the `## Migration Patterns  ` heading; run the convention conformance analysis and assert that the `Migration Patterns` convention is matched and included in the generated task's Implementation Notes (should fail before fix, pass after fix)
- [ ] Test that headings without trailing whitespace continue to work correctly (no regression)
- [ ] Test that headings with mixed whitespace (leading and trailing) are handled correctly

## Verification Commands
- Run plan-feature eval suite to confirm no regressions
- Run the new reproducer test fixture to confirm the trailing-whitespace heading is matched

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring a database migration with foreign keys, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: "Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction logic `line[3:]` does not strip trailing whitespace, causing the extracted section name (e.g., `"Migration Patterns  "`) to fail exact-match comparison against the canonical convention name (`"Migration Patterns"`). The convention is silently dropped with no warning.
