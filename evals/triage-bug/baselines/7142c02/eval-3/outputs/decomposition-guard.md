# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`) -- The heading formatter lowercases and kebab-cases CONVENTIONS.md section headings when generating `§` references for Implementation Notes, producing `§migration-patterns` instead of preserving the original title case `§Migration Patterns`.

2. **Task creation uses wrong issue type ID** (in `plan-feature/SKILL.md` Step 6a) -- The task creation logic reads the Feature issue type ID (10142) from CLAUDE.md's Jira Configuration instead of using the Task issue type ID (10050) from the type-to-role mapping discovered in Step 2.5, causing tasks to be created as Feature issues instead of Task issues.

These root causes are in different modules and different code paths:
- Root cause 1 is in the shared convention utilities (`shared/convention-utils.md`), triggered during convention-aware task enrichment (Step 5).
- Root cause 2 is in the plan-feature skill (`plan-feature/SKILL.md` Step 6a), triggered during Jira task creation (Step 6a).

Options:
1. **Proceed** -- create a single Task covering both fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
