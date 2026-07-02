# Jira API Metadata

Parameters for `jira.create_issue`:

- **Project key**: ACME
- **Issue type**: Task
- **Labels**: `["ai-generated-jira", "bug-fix"]`
- **additional_fields**: `{ "labels": ["ai-generated-jira", "bug-fix"] }`

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix trailing-whitespace handling in plan-feature's convention heading extraction so that conventions from `CONVENTIONS.md` are not silently dropped when heading lines have trailing spaces. Fixes [ACME-500](https://mock-jira.example.com/browse/ACME-500).

The convention extraction logic uses `line[3:]` to parse `## ` headings, which preserves trailing whitespace. This causes the convention-matching step to fail on exact-match lookup, silently dropping the convention from the generated task description.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — fix heading extraction to strip trailing whitespace (`line[3:]` to `line[3:].strip()`)

## Implementation Notes
The defect is in the convention conformance analysis section of the plan-feature skill. The heading extraction loop:

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # BUG: does not strip trailing whitespace
        conventions[section_name] = current_section_content
```

Change `line[3:]` to `line[3:].strip()` to normalize heading names.

The convention-matching step already uses clean names:

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md §{convention_name}: {action}")
```

No changes needed to the matching step — only the extraction step needs the fix.

**Reproducer test guidance**: The Steps to Reproduce specify creating a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `). The test should:
- Set up a `CONVENTIONS.md` fixture with trailing whitespace on a heading line
- Run the convention extraction logic
- Assert the extracted section name equals `"Migration Patterns"` (no trailing spaces)
- Assert the convention appears in the generated task's Implementation Notes as `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`

**Before fix (Actual Result)**: The extracted section name is `"Migration Patterns  "`, the convention lookup fails, and the Implementation Notes omit the convention silently.

**After fix (Expected Result)**: The extracted section name is `"Migration Patterns"`, the convention lookup succeeds, and the Implementation Notes include `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`

The existing eval fixture at `evals/plan-feature/files/conventions-mock.md` does not include trailing whitespace on headings — the reproducer test must add this edge case.

Fixes ACME-500.

## Acceptance Criteria
- [ ] Reproducer test: a test with a `CONVENTIONS.md` heading containing trailing whitespace (e.g., `## Migration Patterns  `) demonstrates the bug fails before the fix and passes after — the convention is correctly included in the generated task's Implementation Notes
- [ ] The heading extraction uses `line[3:].strip()` instead of `line[3:]` to normalize section names
- [ ] Conventions with trailing whitespace on headings are matched and included in generated tasks
- [ ] No regression in existing plan-feature tests and evals

## Test Requirements
- [ ] Reproducer test: create a `CONVENTIONS.md` fixture with trailing whitespace on a `## ` heading line, run convention extraction, and assert the section name is stripped and the convention is included in the generated output (test should fail before fix, pass after)
- [ ] Test that conventions with clean headings (no trailing whitespace) continue to work correctly (regression guard)
- [ ] Test that headings with mixed whitespace (tabs, multiple spaces) are also handled by `.strip()`

## Verification Commands
- Run plan-feature evals to confirm no regression: `<eval-runner> evals/plan-feature/`
- Run the new reproducer test in isolation to confirm it passes after the fix

## Bug Context

- **Bug**: [ACME-500](https://mock-jira.example.com/browse/ACME-500)
- **Steps to Reproduce**: Create a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `), run `/plan-feature ACME-100` on a feature requiring that convention, inspect the generated task's Implementation Notes.
- **Expected Result**: The generated task's Implementation Notes should include: `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`
- **Actual Result**: The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error is shown — the convention is silently dropped.
- **Root Cause**: The heading extraction `line[3:]` does not strip trailing whitespace, causing the convention dictionary key to include trailing spaces. The exact-match lookup in the task enrichment step then fails to find the convention, silently dropping it.
