# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`) -- The convention reference formatter lowercases and kebab-cases CONVENTIONS.md section headings when generating `§` references, producing `§migration-patterns` instead of preserving the original title case `§Migration Patterns`.

2. **Task creation uses wrong issue type ID** (in `plan-feature/SKILL.md` Step 6a) -- The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID (10050), causing tasks to be created as Features in projects with custom issue type schemes.

These are independent defects in different modules with different code paths. Fixing one does not address the other.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually with `/triage-bug`

Choose (1/2):
