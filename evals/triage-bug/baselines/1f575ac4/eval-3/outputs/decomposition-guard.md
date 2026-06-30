# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`) -- The heading-to-reference formatter applies a kebab-case transformation to CONVENTIONS.md section headings, producing `migration-patterns` instead of preserving the original title case `Migration Patterns`. This is a formatting/text-processing defect in the shared convention utilities module.

2. **Task creation uses Feature issue type ID instead of Task issue type ID** (in `plan-feature/SKILL.md` Step 6a) -- The `jira.create_issue` call reads `Feature issue type ID` (10142) from Jira Configuration instead of the Task issue type ID (10050), causing tasks to be created with the wrong issue type. This is a configuration-reading defect in the plan-feature skill's task creation logic.

These are independent root causes:
- They reside in **different modules** (`shared/convention-utils.md` vs. `plan-feature/SKILL.md`)
- They affect **different code paths** (text formatting vs. Jira API calls)
- They can be **fixed and tested independently**
- Fixing one has **no effect** on the other

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually with `/triage-bug`

Choose (1/2):
