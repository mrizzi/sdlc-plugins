# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`) -- the formatter lowercases and kebab-cases CONVENTIONS.md headings when generating `§`-prefixed references, producing `§migration-patterns` instead of preserving the original title case `§Migration Patterns`.

2. **Task creation uses wrong issue type ID** (in `plan-feature/SKILL.md` Step 6a) -- the task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID, causing tasks to be created as Feature issues.

These are independent defects in different modules with different code paths. Fixing one does not affect the other.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
