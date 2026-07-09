# Jira API Metadata

Parameters for `jira.create_issue`:

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: `ai-generated-jira`, `bug-fix`

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature convention heading extraction to strip trailing whitespace so that conventions from `CONVENTIONS.md` are matched correctly even when heading lines contain trailing spaces. Currently, the extraction uses `line[3:]` without stripping, which causes convention names to be stored with trailing whitespace. The downstream exact-match lookup then fails silently, dropping the convention from generated task descriptions.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- strip trailing whitespace from extracted heading text in the convention conformance analysis (`line[3:]` -> `line[3:].strip()`)

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- eval fixture with trailing whitespace on heading lines for reproducer test

## Implementation Notes
The fix is a single-character change in the convention heading extraction logic. In the convention conformance analysis section of `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, change:

```python
section_name = line[3:]
```

to:

```python
section_name = line[3:].strip()
```

This ensures that heading names like `"Migration Patterns  "` are normalized to `"Migration Patterns"` before being stored in the `conventions` dictionary, allowing the downstream exact-match lookup in the convention-aware task enrichment step to succeed.

The existing convention lookup code (`if convention_name in discovered_conventions`) does not need to change -- the fix should be applied at the extraction site so all downstream consumers benefit from normalized keys.

## Acceptance Criteria
- [ ] Reproducer test: a test using a `CONVENTIONS.md` fixture with trailing whitespace on a heading line (e.g., `## Migration Patterns  `) confirms that the convention is correctly extracted and matched. The test must assert that the generated task's Implementation Notes include the expected convention reference (e.g., `Per CONVENTIONS.md "Migration Patterns: ...`). This test should fail before the fix and pass after.
- [ ] Convention heading extraction in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` strips trailing whitespace from extracted heading text
- [ ] Conventions with trailing whitespace on headings are included in generated task descriptions
- [ ] No regression: conventions without trailing whitespace continue to be matched correctly

## Test Requirements
- [ ] Reproducer test: create an eval fixture `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` with a heading that has trailing spaces (e.g., `## Migration Patterns  ` followed by convention content). Run the plan-feature convention conformance analysis against this fixture and assert that the output includes `Per CONVENTIONS.md "Migration Patterns: add Index::create() for all FK columns.` -- if the heading is not matched, the convention is silently dropped and no such line appears in the output.
- [ ] Verify that existing conventions without trailing whitespace still pass (run existing plan-feature evals to confirm no regression)

## Verification Commands
- Run plan-feature evals with the new trailing-whitespace fixture and confirm the convention appears in generated task Implementation Notes
- Run existing plan-feature evals to confirm no regression

## Bug Context
- **Bug**: ACME-500 -- plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Steps to Reproduce**:
  1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading (e.g., `## Migration Patterns  `)
  2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys
  3. Inspect the generated task's Implementation Notes
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md "Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction in the plan-feature convention conformance analysis uses `line[3:]` which does not strip trailing whitespace. This causes convention names to be stored with trailing spaces, failing the downstream exact-match lookup.
