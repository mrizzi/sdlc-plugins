# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`) -- The convention reference formatter applies a kebab-case transformation to CONVENTIONS.md section headings, producing `§migration-patterns` instead of preserving the original heading text `§Migration Patterns`. This affects task description generation in Step 5 of plan-feature, where Implementation Notes reference conventions by section name. The fix requires changing the case transform function in the shared convention utilities module.

2. **Task creation uses Feature issue type ID instead of Task** (in `plan-feature/SKILL.md` Step 6a) -- The task creation logic reads the Feature issue type ID (10142) from Jira Configuration and uses it when creating Task issues. Projects with custom issue type schemes have a distinct Task issue type ID (e.g., 10050), so using the Feature ID results in issues of the wrong type. The fix requires updating the issue type resolution in Step 6a to use the correct Task issue type ID from configuration.

These are independent issues in different modules with different code paths:
- Root Cause 1 is in the shared convention formatting layer (`shared/convention-utils.md`), executed during task description generation (Step 5).
- Root Cause 2 is in the plan-feature task creation logic (`plan-feature/SKILL.md` Step 6a), executed during Jira issue creation (Step 6).
- Fixing one does not affect or depend on the other.

Options:
1. **Proceed** -- create a single Task covering both fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
