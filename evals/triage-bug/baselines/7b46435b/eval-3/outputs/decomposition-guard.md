This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`)
   - Heading references are kebab-cased instead of preserving original case
   - Produces `§migration-patterns` instead of `§Migration Patterns`

2. **Task creation uses wrong issue type ID** (in `plan-feature/SKILL.md Step 6a`)
   - Reads Feature issue type ID (10142) instead of Task issue type ID
   - Creates Feature issues instead of Task issues

Options:
1. **Proceed** — create a single Task covering both fixes
2. **Split** — I recommend creating separate Bugs for each independent issue, then triaging each one individually with /triage-bug

Choose (1/2):
