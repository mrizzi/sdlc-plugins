# Decomposition Guard -- ACME-502

## Triggered: Multiple Independent Root Causes Detected

This bug appears to involve multiple independent issues:

1. **Malformed convention references** (in `shared/convention-utils.md`) -- The convention reference formatter applies a kebab-case/slugify transformation to CONVENTIONS.md section headings, producing `§migration-patterns` instead of the correct `§Migration Patterns`. This is a text formatting bug in the shared convention utilities module.

2. **Wrong issue type on task creation** (in `plan-feature/SKILL.md` Step 6a) -- The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of using the project's Task issue type ID (10050). This is a configuration lookup bug in the plan-feature task creation step.

These two issues are in **independent code paths** in **different modules**. They do not share logic, do not interact, and fixing one has no effect on the other.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):

---

### Rationale for Split Recommendation

- **Independent root causes**: The convention formatter bug and the issue type bug arise from completely different code paths (`shared/convention-utils.md` vs. `plan-feature/SKILL.md` Step 6a).
- **Different concerns**: One is a text formatting problem; the other is a Jira API parameter problem.
- **Separate testability**: Each fix requires its own reproducer test with distinct inputs and assertions.
- **Cleaner traceability**: Separate Bugs and Tasks provide clearer Jira history and make it easier to verify each fix independently.

If **Split** is chosen, the recommended new Bug issues would be:

| New Bug | Summary | Root Cause Module |
|---------|---------|-------------------|
| Bug A | Convention reference formatter produces kebab-case instead of preserving heading text | `shared/convention-utils.md` |
| Bug B | plan-feature Step 6a creates tasks with Feature issue type instead of Task issue type | `plan-feature/SKILL.md` Step 6a |

Each new Bug would then be triaged individually with `/triage-bug`, producing a focused Task with a single reproducer test and a single fix scope.
