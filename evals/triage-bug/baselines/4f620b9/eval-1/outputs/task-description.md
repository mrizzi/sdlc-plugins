# Jira API Metadata

```
jira.create_issue(
  project: "ACME",
  issue_type: "Task",
  labels: ["ai-generated-jira"],
  summary: "Fix plan-feature convention extraction to strip trailing whitespace from CONVENTIONS.md headings"
)
```

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention extraction to strip trailing whitespace from
`CONVENTIONS.md` headings. Currently, headings with trailing spaces (e.g.,
`## Migration Patterns  `) are stored with whitespace in the dictionary key, causing
exact-match lookups to fail silently. This results in conventions being dropped from
generated task descriptions without any warning. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Add `.strip()` to heading extraction in the convention parsing loop

## Implementation Notes
The bug is in the convention extraction loop within the plan-feature skill. The current
heading extraction logic:

```python
section_name = line[3:]  # Does NOT strip trailing whitespace
```

Must be changed to:

```python
section_name = line[3:].strip()  # Strips trailing whitespace from heading text
```

This ensures that headings like `## Migration Patterns  ` (with trailing spaces) are
normalized to `"Migration Patterns"` before being stored in the conventions dictionary.

The convention matching step:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md {convention_name}: {action}")
```

will then succeed because the stored key matches the lookup key after normalization.

Additionally, consider adding a warning when a convention is expected but not found in
the parsed dictionary, to prevent silent failures in the future.

**Reproducer guidance**: The Steps to Reproduce specify creating a `CONVENTIONS.md` with
trailing whitespace on the heading `## Migration Patterns  ` and running `/plan-feature`
on a feature requiring a database migration. The reproducer test should:

1. Create a mock `CONVENTIONS.md` fixture with trailing whitespace on at least one heading
2. Run the convention extraction logic against this fixture
3. Assert that the extracted key is `"Migration Patterns"` (without trailing whitespace)
4. Assert that the convention is matched and included in the generated task output

Reference existing eval fixture at `evals/plan-feature/files/conventions-mock.md` for
test patterns -- note that this fixture does NOT currently cover the trailing whitespace
edge case.

## Acceptance Criteria
- [ ] Reproducer test: a test with a `CONVENTIONS.md` fixture containing trailing whitespace on headings demonstrates the bug (fails before fix, passes after fix)
- [ ] Convention headings with trailing whitespace are correctly matched during plan-feature convention conformance analysis
- [ ] Conventions with trailing whitespace on headings are included in generated task Implementation Notes
- [ ] No regression in existing plan-feature eval tests

## Test Requirements
- [ ] Reproducer test: create a `CONVENTIONS.md` fixture with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run the convention extraction and matching logic, and assert that the convention IS matched and included in output -- this test should fail before the fix and pass after
- [ ] Test that headings without trailing whitespace continue to work correctly (no regression)
- [ ] Test that headings with mixed whitespace (tabs, multiple spaces) are also handled correctly

## Verification Commands
- `pytest evals/plan-feature/` -- all plan-feature eval tests pass, including the new reproducer test

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading line (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring a database migration, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: "Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The convention extraction logic uses `line[3:]` to extract heading text after `## `, which does not strip trailing whitespace. The subsequent exact-match lookup fails because the stored key contains trailing spaces while the lookup key does not.
