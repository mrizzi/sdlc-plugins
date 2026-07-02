<!-- Jira API Metadata
jira.create_issue parameters:
  project_key: ACME
  issue_type: Task
  summary: "Fix trailing-whitespace handling in plan-feature convention heading extraction"
  labels:
    - ai-generated-jira
  additional_fields:
    labels:
      - ai-generated-jira
-->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature convention conformance analysis to strip trailing whitespace from
CONVENTIONS.md heading lines during extraction. Currently, `line[3:]` preserves trailing
spaces on headings like `## Migration Patterns  `, causing the extracted section name to
include trailing whitespace. This breaks exact-match lookups in the convention-aware task
enrichment step, silently dropping conventions from generated task descriptions.

Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Add `.strip()` to heading extraction in convention conformance analysis

## Implementation Notes
The bug is in the convention conformance analysis section of the plan-feature skill. The
heading extraction logic currently reads:

```python
section_name = line[3:]
```

This must be changed to:

```python
section_name = line[3:].strip()
```

This ensures that headings with trailing whitespace (spaces, tabs, newline characters) are
normalized before being stored as dictionary keys in `conventions[section_name]`.

The convention-aware task enrichment step uses exact-match comparison:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

After the fix, `"Migration Patterns"` will correctly match the dictionary key
`"Migration Patterns"` (stripped) instead of failing against `"Migration Patterns  "`
(with trailing whitespace).

### Reproducer test guidance

Translate the Steps to Reproduce into a test scenario:

1. **Input**: Create a CONVENTIONS.md fixture string with trailing whitespace on a heading:
   ```
   ## Migration Patterns  \n
   Add Index::create() for all FK columns.\n
   ```
   Note the two trailing spaces after `Migration Patterns`.

2. **Bug behavior (before fix)**: The convention extraction produces a dictionary key
   `"Migration Patterns  "`. Looking up `"Migration Patterns"` returns no match. The
   generated task's Implementation Notes omit the convention reference entirely.

3. **Fixed behavior (after fix)**: The convention extraction produces a dictionary key
   `"Migration Patterns"` (stripped). Looking up `"Migration Patterns"` succeeds. The
   generated task's Implementation Notes include:
   `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`

### Existing test reference

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not
include trailing whitespace on headings. The reproducer test should create a new fixture
or inline the CONVENTIONS.md content with trailing whitespace to cover this edge case.

## Acceptance Criteria
- [ ] A reproducer test exists that uses a CONVENTIONS.md fixture with trailing whitespace on a heading (e.g., `## Migration Patterns  `), asserts the convention is correctly extracted and matched, fails before the fix, and passes after the fix
- [ ] The heading extraction in plan-feature convention conformance analysis strips trailing whitespace from section names (e.g., via `.strip()`)
- [ ] Conventions with trailing whitespace on headings are included in generated task Implementation Notes with the correct reference format (`Per CONVENTIONS.md §<section>: ...`)
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with trailing whitespace on a heading line (`## Migration Patterns  ` with trailing spaces), run the convention extraction logic, and assert that looking up `"Migration Patterns"` (without trailing spaces) returns the convention content. Assert that the generated Implementation Notes include `Per CONVENTIONS.md §Migration Patterns:`. This test must fail before the fix and pass after.
- [ ] Verify that headings without trailing whitespace continue to work correctly (no regression)
- [ ] Verify that headings with other whitespace variants (tabs, mixed spaces/tabs, newlines) are also stripped correctly

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (`## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring a database migration with foreign keys, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction `line[3:]` in plan-feature convention conformance analysis does not strip trailing whitespace, so `"## Migration Patterns  \n"` becomes `"Migration Patterns  "` which fails exact-match comparison against `"Migration Patterns"`.
