# Decomposition Guard -- ACME-502

## Trigger

The investigation of ACME-502 identified **two independent root causes** located in **different modules and code paths**. Per Step 6 of the triage-bug workflow, this triggers the Decomposition Guard. A single Task must NOT be silently created bundling both fixes.

## Prompt to User

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`) -- The formatter applies a kebab-case transformation (lowercase + hyphenate) to CONVENTIONS.md section headings when generating section references. For example, the heading `## Migration Patterns` is rendered as `migration-patterns` instead of `Migration Patterns`. This is a string formatting defect in the shared convention utilities module.

2. **Task creation uses wrong issue type ID** (in `plan-feature/SKILL.md` Step 6a) -- The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID. This causes created issues to be of type "Feature" instead of "Task" when the project has a custom issue type scheme.

Options:
1. **Proceed** -- create a single Task covering all fixes
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):

## Rationale for Triggering

These two issues qualify as independent because:

- **Different modules**: Root cause 1 is in `shared/convention-utils.md` (shared utility); root cause 2 is in `plan-feature/SKILL.md` (plan-feature skill step 6a)
- **Different code paths**: Root cause 1 involves string formatting/case transformation logic; root cause 2 involves Jira API issue creation and configuration field lookup
- **Independent fixes**: Fixing the convention formatter does not affect or depend on fixing the task creation issue type, and vice versa
- **Different test domains**: Root cause 1 requires testing string output format; root cause 2 requires testing Jira API parameters

## Awaiting User Input

Execution is **stopped** at Step 6. No Task has been created. The workflow will resume based on the user's choice:

- If **Option 1 (Proceed)**: Continue to Step 5 and create a single Task covering both fixes.
- If **Option 2 (Split)**: Stop and suggest the user create two separate Bug issues -- one for the convention formatter defect and one for the task creation issue type defect -- then triage each individually with `/triage-bug`.
