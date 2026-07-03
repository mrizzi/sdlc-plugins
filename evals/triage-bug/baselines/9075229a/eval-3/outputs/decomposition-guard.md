# Decomposition Guard -- ACME-502

This is the Decomposition Guard prompt (Step 6 of the triage-bug skill) presented to the user before any Task creation occurs. The skill does NOT silently create a single Task -- it stops here and waits for the user's choice.

---

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transformation** (in `shared/convention-utils.md`) -- The formatter lowercases and kebab-cases CONVENTIONS.md headings when generating section references, producing `§migration-patterns` instead of preserving the original title case `§Migration Patterns`.

2. **Task creation reads wrong issue type ID from configuration** (in `plan-feature/SKILL.md` Step 6a) -- The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of looking up the Task issue type ID (10050), causing created issues to be of type Feature instead of Task.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
