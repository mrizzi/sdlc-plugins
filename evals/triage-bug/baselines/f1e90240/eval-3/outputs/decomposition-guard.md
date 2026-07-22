# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Malformed convention references** -- the convention reference formatter applies kebab-case instead of preserving title case for section headings (in `shared/convention-utils.md`)
2. **Wrong issue type for created tasks** -- the task creation logic reads the Feature issue type ID (10142) instead of the Task issue type ID from configuration (in `plan-feature/SKILL.md` Step 6a)

Options:

1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
