# Jira API Metadata

```
jira.create_issue(
  project_key: "ACME",
  issue_type: "Task",
  labels: ["ai-generated-jira"]
)
```

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: ai-generated-jira
- **Link**: Blocks (inward: created task, outward: ACME-500)

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention lookup to strip trailing whitespace from CONVENTIONS.md headings before storing them as dictionary keys. Currently, headings with trailing spaces (e.g., `## Migration Patterns  `) are stored with the whitespace intact, causing exact-match lookups to fail silently. This results in conventions being dropped from generated task descriptions without any warning. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — add `.strip()` to heading extraction in convention lookup loop to normalize section names

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` — eval fixture with trailing whitespace on headings for reproducer test

## Implementation Notes
The defect is in the convention lookup loop within plan-feature's SKILL.md. The heading extraction code:

```python
section_name = line[3:]  # Does NOT strip trailing whitespace
```

should be changed to:

```python
section_name = line[3:].strip()  # Strips trailing whitespace from heading
```

This ensures that `## Migration Patterns  ` is stored as `"Migration Patterns"` rather than `"Migration Patterns  "`, allowing the exact-match comparison in the task enrichment step to succeed:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

**Reproducer test guidance**: Create a CONVENTIONS.md fixture file containing at least one heading with trailing whitespace (e.g., `## Migration Patterns  ` with two trailing spaces after "Patterns"). Run the convention lookup against this fixture and assert:
- The section name is stored without trailing whitespace
- The convention is matched when looked up by the clean name `"Migration Patterns"`
- The generated Implementation Notes include the convention reference: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`

**Existing test patterns**: The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` provides the structure for the new fixture. It does not include trailing whitespace on headings, which is the gap this fix addresses.

Fixes ACME-500.

## Reuse Candidates
- `evals/plan-feature/files/conventions-mock.md` — existing convention fixture to use as a base for the new trailing-whitespace fixture

## Acceptance Criteria
- [ ] A reproducer test demonstrates the bug: a CONVENTIONS.md fixture with trailing whitespace on headings causes convention matching to fail before the fix, and succeeds after the fix
- [ ] The convention lookup code strips trailing whitespace from extracted heading names using `.strip()`
- [ ] Conventions with trailing whitespace on headings are correctly matched and included in generated task Implementation Notes
- [ ] No warning-free silent dropping of conventions — if a heading is normalized, behavior is correct without requiring additional user action
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with trailing whitespace on the heading `## Migration Patterns  ` (two trailing spaces). Run the convention lookup and assert the section is stored with key `"Migration Patterns"` (no trailing spaces). Assert the convention is included in the generated task's Implementation Notes with the reference `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- [ ] Edge case: verify headings with mixed trailing whitespace (spaces and tabs) are also normalized
- [ ] Regression: verify that headings without trailing whitespace continue to work correctly (existing conventions-mock.md fixture)

## Verification Commands
- Run plan-feature eval suite against the new trailing-whitespace fixture and verify the convention is included in output
- Run existing plan-feature eval suite and verify no regressions

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring database migration with FKs, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown — the convention is silently dropped.
- **Root Cause**: The heading extraction `line[3:]` does not strip trailing whitespace, causing exact-match convention lookups to fail silently when headings have trailing spaces.
