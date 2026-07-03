<!-- Jira API Metadata
jira.create_issue parameters:
  project: ACME
  issue_type: Task
  labels:
    - ai-generated-jira
-->

## Repository

acme-backend

## Target Branch

main

## Description

Fix the convention heading extraction in the plan-feature skill to strip trailing whitespace from `CONVENTIONS.md` headings. Currently, `section_name = line[3:]` preserves trailing whitespace, causing silent match failures when the downstream task enrichment step performs exact-match lookups against heading names. This results in conventions being silently dropped from generated task descriptions.

## Files to Modify

- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- Convention conformance analysis (heading extraction logic)
- `evals/plan-feature/files/conventions-mock.md` -- Add trailing-whitespace test fixture

## Implementation Notes

- In the convention heading extraction logic, change `section_name = line[3:]` to `section_name = line[3:].strip()` so that trailing whitespace on headings is normalized before being stored as dictionary keys
- This is a one-line fix with high confidence -- the `.strip()` call removes leading and trailing whitespace, ensuring exact-match lookups succeed regardless of whitespace in the source `CONVENTIONS.md`
- Reference: Bug [ACME-500](https://mock-jira.example.com/browse/ACME-500)

## Acceptance Criteria

- [ ] Reproducer test: a test using a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `) fails before the fix and passes after, asserting that the convention IS included in the generated task output
- [ ] Convention heading extraction strips trailing whitespace from section names (`line[3:].strip()`)
- [ ] No regression in existing tests -- all current plan-feature evals continue to pass

## Test Requirements

- [ ] Reproducer test: Create a `CONVENTIONS.md` fixture with trailing whitespace on a heading (e.g., `## Migration Patterns  ` with two trailing spaces after "Patterns"). Run convention extraction against this fixture. Assert that the convention section IS included in the generated task output (i.e., the task's Implementation Notes contain the `Per CONVENTIONS.md` reference for the affected convention). This test must fail before the fix is applied and pass after.
- [ ] Verify that the existing `evals/plan-feature/files/conventions-mock.md` fixture (without trailing whitespace) continues to produce correct output after the fix
- [ ] Edge case test: headings with mixed whitespace (tabs, multiple spaces) are also handled correctly by `.strip()`

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a section heading (e.g., `## Migration Patterns  `), run `/plan-feature` on a feature requiring that convention, and inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes include the convention reference (e.g., `Per CONVENTIONS.md Migration Patterns: add Index::create() for all FK columns.`).
- **Actual Result**: The convention is silently dropped -- no reference appears in Implementation Notes, and no warning is emitted.
- **Root Cause**: Convention heading extraction uses `line[3:]` without `.strip()`, so trailing whitespace on headings causes silent exact-match failure in the downstream task enrichment step.
