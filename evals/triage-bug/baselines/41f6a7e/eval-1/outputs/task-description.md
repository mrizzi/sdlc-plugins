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
Fix trailing whitespace handling in plan-feature convention heading extraction so that CONVENTIONS.md headings with trailing spaces are correctly matched during convention-aware task enrichment. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to heading extraction at `line[3:]`

## Implementation Notes
The plan-feature skill's convention conformance analysis extracts CONVENTIONS.md headings using `line[3:]`, which preserves trailing whitespace. This causes exact-match lookups to fail silently when headings have trailing spaces.

**Fix location**: In the convention heading extraction loop in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, change:

```python
section_name = line[3:]
```

to:

```python
section_name = line[3:].strip()
```

This normalizes the heading text before storing it as a dictionary key, ensuring the subsequent exact-match lookup in the task enrichment step succeeds regardless of trailing whitespace.

**Reproducer test guidance**:
- Input: a CONVENTIONS.md fixture with trailing whitespace on a heading (e.g., `## Migration Patterns  ` with two trailing spaces after "Patterns")
- Incorrect behavior (before fix): the convention is silently dropped -- no `Per CONVENTIONS.md` annotation appears in the task's Implementation Notes
- Correct behavior (after fix): the convention is matched and the annotation `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.` appears in the Implementation Notes
- Existing test fixture: `evals/plan-feature/files/conventions-mock.md` -- does not currently include trailing whitespace cases; add a new fixture or extend it

**Existing patterns to follow**:
- The convention extraction loop is in the plan-feature skill's convention conformance analysis section
- The task enrichment step uses `if convention_name in discovered_conventions:` for lookup
- Existing eval fixtures in `evals/plan-feature/files/` provide the pattern for test data

Fixes ACME-500.

## Acceptance Criteria
- [ ] A reproducer test demonstrates the bug: a CONVENTIONS.md heading with trailing whitespace is correctly extracted and matched (test fails before fix, passes after)
- [ ] `line[3:]` is replaced with `line[3:].strip()` in the convention heading extraction logic
- [ ] Convention headings with trailing whitespace produce the correct `Per CONVENTIONS.md` annotation in generated task descriptions
- [ ] No regression in existing plan-feature convention tests

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with trailing whitespace on a `## ` heading line (e.g., `## Migration Patterns  `); run the convention extraction and verify the heading is matched and the expected annotation is produced in the task's Implementation Notes
- [ ] Regression test: verify that convention headings without trailing whitespace continue to be extracted and matched correctly
- [ ] Edge case test: verify that headings with mixed whitespace (tabs, multiple spaces) are handled correctly by `.strip()`

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring a database migration with foreign keys, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The convention heading extraction uses `line[3:]` which does not strip trailing whitespace. The extracted key `"Migration Patterns  "` fails exact-match lookup against the normalized `"Migration Patterns"`, causing the convention to be silently omitted.
