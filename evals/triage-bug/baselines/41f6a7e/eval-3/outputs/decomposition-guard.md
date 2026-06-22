# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`) -- the formatter lowercases and kebab-cases CONVENTIONS.md section headings (producing `migration-patterns`) instead of preserving the original title case (`Migration Patterns`) when building Implementation Notes references.

2. **Task creation uses wrong issue type ID** (in `plan-feature/SKILL.md` Step 6a) -- the task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of a Task issue type ID, causing all generated tasks to be created as Feature issues rather than Task issues.

These root causes are in different modules and code paths, and each can be fixed independently.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
