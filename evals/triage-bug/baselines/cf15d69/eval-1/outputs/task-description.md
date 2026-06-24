<!-- Jira API metadata: jira.create_issue -->
<!-- project: ACME -->
<!-- issuetype: 10020 -->
<!-- labels: ["ai-generated-jira"] -->
<!-- link: { type: "Blocks", inwardIssue: "ACME-500" } -->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the plan-feature convention lookup to strip trailing whitespace from `CONVENTIONS.md` heading lines. Currently, `line[3:]` preserves trailing spaces, causing exact-match convention lookups to fail silently. Apply `.strip()` to the extracted heading text so that headings like `## Migration Patterns  ` are correctly normalized to `"Migration Patterns"`. Additionally, add a warning log when a convention name is not found during task enrichment to prevent silent failures.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- fix heading extraction to strip trailing whitespace from `line[3:]` and add a warning log for unmatched convention names

## Files to Create
- `evals/plan-feature/files/conventions-trailing-whitespace-mock.md` -- eval fixture with trailing whitespace on headings for reproducer test

## Implementation Notes
- In the convention conformance analysis section, change `section_name = line[3:]` to `section_name = line[3:].strip()` to normalize heading text
- In the convention-aware task enrichment section, add a warning log when `convention_name not in discovered_conventions` so that missing conventions are no longer silently dropped
- Follow the existing pattern in `evals/plan-feature/files/conventions-mock.md` for the new eval fixture structure, but add trailing whitespace (spaces) to at least one heading line
- The existing eval fixture `evals/plan-feature/files/conventions-mock.md` must NOT be modified -- the new fixture is additive

## Acceptance Criteria
- [ ] Reproducer test: a test with trailing whitespace on a `CONVENTIONS.md` heading (e.g., `## Migration Patterns  `) correctly matches the convention and includes it in the generated task's Implementation Notes
- [ ] Convention headings with trailing spaces or tabs are normalized before storage in the conventions dictionary
- [ ] Convention headings with leading spaces after `## ` are also normalized (defensive fix)
- [ ] A warning is logged when a convention name is expected but not found in the discovered conventions
- [ ] Existing conventions without trailing whitespace continue to work unchanged

## Test Requirements
- [ ] Reproducer test: create a `CONVENTIONS.md` fixture with trailing whitespace on the `## Migration Patterns  ` heading, run convention conformance analysis, and assert the output contains `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- [ ] Test that headings with mixed trailing whitespace (spaces and tabs) are correctly stripped
- [ ] Test that headings with no trailing whitespace continue to match correctly (regression guard)
- [ ] Test that the warning log is emitted when a convention name is not found

## Bug Context
- **Bug**: ACME-500 -- plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Steps to Reproduce**:
  1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading (e.g., `## Migration Patterns  `)
  2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys
  3. Inspect the generated task's Implementation Notes
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown -- the convention is silently dropped.
- **Root Cause**: The heading extraction code `line[3:]` in the plan-feature convention lookup does not strip trailing whitespace. When a heading line has trailing spaces (e.g., `## Migration Patterns  `), the extracted key becomes `"Migration Patterns  "`, which fails exact-match comparison against the clean key `"Migration Patterns"`.
