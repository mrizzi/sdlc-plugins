# Jira API Metadata

Parameters for `jira.create_issue`:

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: ai-generated-jira

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix silent convention dropping in plan-feature when `CONVENTIONS.md` headings contain trailing whitespace. The heading extraction uses `line[3:]` without stripping whitespace, causing exact-match lookups to fail silently. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add `.strip()` to heading extraction in convention conformance analysis

## Implementation Notes
The plan-feature skill parses `CONVENTIONS.md` section headings in a line-by-line loop:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

The fix is to apply `.strip()` to the extracted section name:

```python
section_name = line[3:].strip()
```

The convention-aware task enrichment step performs exact-match comparison:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

This match fails when the stored key has trailing spaces from the extraction step.
After applying `.strip()`, keys will be normalized and match correctly.

Additionally, consider adding a warning when a convention defined in `CONVENTIONS.md`
is not matched during task enrichment, to surface silent failures in the future.

**Reproducer test guidance**: The reproducer should create a `CONVENTIONS.md` fixture
with trailing whitespace on a heading (e.g., `## Migration Patterns  ` with trailing
spaces). Run the convention extraction logic and assert that the convention is matched
and included in the generated task's Implementation Notes. The test should initially
fail (demonstrating the bug) and pass after the fix.

Existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not
include trailing whitespace on headings -- this edge case is not covered by current
tests.

Fixes ACME-500.

## Acceptance Criteria
- [ ] Reproducer test: a test with a `CONVENTIONS.md` heading containing trailing whitespace (e.g., `## Migration Patterns  `) demonstrates that the convention is correctly matched and included in the generated task -- fails before fix, passes after
- [ ] The heading extraction in the convention conformance analysis applies `.strip()` to normalize section names (i.e., `section_name = line[3:].strip()`)
- [ ] Conventions with trailing whitespace on headings are no longer silently dropped
- [ ] No regression in existing plan-feature tests and evals

## Test Requirements
- [ ] Reproducer test: create a `CONVENTIONS.md` fixture with trailing whitespace on a section heading (`## Migration Patterns  `), run the convention extraction, and assert that `"Migration Patterns"` is a key in the resulting conventions dictionary and that the generated task's Implementation Notes contain `Per CONVENTIONS.md Migration Patterns:`
- [ ] Test that headings without trailing whitespace continue to work correctly (regression guard)
- [ ] Test that headings with mixed leading/trailing whitespace are normalized correctly

## Verification Commands
- `python3 -m pytest evals/plan-feature/ -v` -- all plan-feature evals should pass, including the new trailing-whitespace test case

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with a trailing-whitespace heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring database migration with foreign keys, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction `line[3:]` does not strip trailing whitespace, causing exact-match convention lookups to fail silently when `CONVENTIONS.md` headings contain trailing spaces.
