# Jira API Metadata

Parameters for `jira.create_issue`:

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: ai-generated-jira
- **Summary**: Fix trailing whitespace in CONVENTIONS.md heading extraction causing silent convention drop

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention conformance analysis to strip trailing whitespace from CONVENTIONS.md headings during extraction. Currently, `line[3:]` captures trailing spaces, causing exact-match lookups to fail silently and drop conventions from generated task descriptions. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Fix heading extraction to strip trailing whitespace from `line[3:]`

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- Test fixture with trailing whitespace on headings

## Implementation Notes
The defect is in the convention conformance analysis section of `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The heading extraction logic currently uses:

```python
section_name = line[3:]
```

This must be changed to:

```python
section_name = line[3:].strip()
```

This ensures trailing (and leading) whitespace on CONVENTIONS.md headings is normalized before being stored as dictionary keys. The exact-match lookup in the task enrichment step (`if convention_name in discovered_conventions`) will then succeed regardless of whitespace formatting in the source file.

**Reproducer test guidance**:
- Create a CONVENTIONS.md fixture containing a heading with trailing whitespace: `## Migration Patterns  ` (two trailing spaces after "Patterns")
- The fixture should include content under the heading: `Add Index::create() for all FK columns.`
- Parse the fixture using the convention extraction logic
- Before the fix, the extracted key will be `"Migration Patterns  "` (with trailing spaces), and the lookup for `"Migration Patterns"` will fail -- the convention will be silently dropped
- After the fix, the extracted key will be `"Migration Patterns"` (stripped), and the lookup will succeed -- the convention will appear in the generated task's Implementation Notes as: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`

**Existing patterns to reuse**:
- `evals/plan-feature/files/conventions-mock.md` -- existing eval fixture for convention parsing (use as a structural template for the new trailing-whitespace fixture)

Fixes ACME-500.

## Acceptance Criteria
- [ ] A reproducer test exists that creates a CONVENTIONS.md fixture with trailing whitespace on headings, runs the convention extraction, and asserts the convention is correctly matched (test fails before fix, passes after)
- [ ] The heading extraction logic in plan-feature applies `.strip()` to `line[3:]` so that trailing whitespace is removed from section names
- [ ] Conventions with trailing whitespace on headings appear in generated task Implementation Notes with the correct section name reference
- [ ] No regression in existing plan-feature convention conformance tests

## Test Requirements
- [ ] Reproducer test: create a CONVENTIONS.md fixture with `## Migration Patterns  ` (trailing whitespace), parse it with the convention extraction logic, and assert that the key `"Migration Patterns"` exists in the resulting conventions dictionary and that the generated task notes include `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- [ ] Verify that existing conventions without trailing whitespace continue to be extracted correctly (no regression)
- [ ] Verify that headings with various whitespace patterns (tabs, multiple spaces, mixed) are all normalized correctly

## Verification Commands
- Run plan-feature eval suite to confirm no regressions in convention handling

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring database migration with foreign keys, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction logic `line[3:]` does not strip trailing whitespace, causing the extracted section name to include trailing spaces. The subsequent exact-match lookup fails silently because the dictionary key `"Migration Patterns  "` does not match the expected `"Migration Patterns"`.
