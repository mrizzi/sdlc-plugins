<!-- Jira API Metadata
jira.create_issue parameters:
  project_key: ACME
  issue_type: Task
  labels:
    - ai-generated-jira
    - bug-fix
-->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature skill's convention extraction to strip trailing whitespace from `CONVENTIONS.md` headings, preventing silent convention drops during task generation. Currently, headings with trailing whitespace (e.g., `## Migration Patterns  `) produce dictionary keys that fail exact-match lookups, causing the convention to be silently omitted from generated task descriptions.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Apply `.strip()` to heading extraction (`line[3:]` -> `line[3:].strip()`) and add a warning log when a convention name is expected but not found

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- Eval fixture with trailing whitespace on convention headings to cover this edge case

## Implementation Notes
- The convention extraction loop is in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` in the convention conformance analysis section. The line `section_name = line[3:]` must be changed to `section_name = line[3:].strip()` to normalize heading keys.
- The convention-aware task enrichment section in the same file performs the lookup `if convention_name in discovered_conventions`. Add an `else` branch that logs a warning identifying the unmatched convention name, so future mismatches are visible rather than silent.
- The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not include trailing whitespace on headings. Create a new fixture that does, or extend the existing one.

## Acceptance Criteria
- [ ] A reproducer test demonstrates the bug: a `CONVENTIONS.md` with trailing whitespace on a `##` heading causes the convention to be silently dropped before the fix, and correctly included after the fix
- [ ] Heading extraction applies `.strip()` to normalize section names regardless of trailing whitespace
- [ ] When a convention name is expected but not found in the discovered conventions dictionary, a warning is logged identifying the unmatched name
- [ ] Existing conventions without trailing whitespace continue to be matched correctly (no regression)

## Test Requirements
- [ ] Reproducer test: create a `CONVENTIONS.md` fixture with trailing whitespace on at least one `##` heading (e.g., `## Migration Patterns  `), run convention extraction, and assert that the convention key matches the clean name `"Migration Patterns"` (without trailing spaces) -- verifying the extracted key equals the expected clean string
- [ ] Test that conventions with no trailing whitespace are still correctly extracted and matched (regression guard)
- [ ] Test that the warning log is emitted when a convention name lookup fails (verifying the silent-failure fix)

## Verification Commands
- Run plan-feature eval suite to confirm no regressions in convention matching
- Run the new trailing-whitespace eval case to confirm the fix resolves the bug

## Bug Context
- **Bug Key**: ACME-500
- **Steps to Reproduce**:
  1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading (e.g., `## Migration Patterns  `)
  2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys
  3. Inspect the generated task's Implementation Notes
- **Expected Result**: The generated task's Implementation Notes should include: "Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction code `line[3:]` does not strip trailing whitespace, producing dictionary keys like `"Migration Patterns  "` that fail exact-match lookups against the clean convention name `"Migration Patterns"`.
