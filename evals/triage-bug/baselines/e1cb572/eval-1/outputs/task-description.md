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
Fix the plan-feature skill's convention extraction to strip trailing whitespace from CONVENTIONS.md section headings. Currently, headings with trailing spaces (e.g., `## Migration Patterns  `) are stored with whitespace intact, causing downstream exact-match lookups to silently fail and omit the convention from generated task descriptions. Fixes ACME-500.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — add `.strip()` to the heading extraction logic (`line[3:]` -> `line[3:].strip()`) to normalize trailing whitespace from convention section names

## Implementation Notes
The defect is in the convention heading extraction loop in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`. The current code:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

Change `line[3:]` to `line[3:].strip()` so that trailing whitespace on heading lines is normalized before storing the section name in the conventions dictionary.

The downstream matching logic uses exact string comparison:
```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

This logic is correct and does not need modification — the fix is entirely in the extraction step.

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not cover trailing whitespace on headings. A new test fixture with trailing whitespace must be created to serve as the reproducer.

Fixes ACME-500.

## Acceptance Criteria
- [ ] A reproducer test demonstrates that CONVENTIONS.md headings with trailing whitespace are correctly matched: the test creates a conventions file with trailing whitespace on a heading (e.g., `## Migration Patterns  `), runs the convention extraction, and asserts the convention is included in the generated task output. The test must fail before the fix and pass after.
- [ ] The convention extraction logic strips trailing whitespace from heading lines, so `line[3:].strip()` is used instead of `line[3:]`.
- [ ] Conventions without trailing whitespace continue to work correctly (no regression).
- [ ] No regression in existing plan-feature eval tests.

## Test Requirements
- [ ] Reproducer test: Create a test fixture CONVENTIONS.md with trailing whitespace on a section heading (e.g., `## Migration Patterns  ` with two trailing spaces followed by content `Add Index::create() for all FK columns.`). Run the plan-feature convention extraction and assert that the section name `"Migration Patterns"` (clean, without trailing spaces) is present in the conventions dictionary and that the generated task's Implementation Notes include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- [ ] Regression test: Verify that the existing eval fixture `evals/plan-feature/files/conventions-mock.md` (which has clean headings without trailing whitespace) continues to produce correct convention matches after the fix.

## Verification Commands
- `python3 -m pytest evals/plan-feature/ -v` — all plan-feature eval tests pass, including the new reproducer test

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a CONVENTIONS.md with trailing whitespace on a section heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring a database migration with foreign keys, then inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: "Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns."
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown — the convention is silently dropped.
- **Root Cause**: The convention heading extraction uses `line[3:]` without `.strip()`, so trailing whitespace on CONVENTIONS.md headings is preserved in the dictionary key. Downstream exact-match lookup against the clean name fails silently.
