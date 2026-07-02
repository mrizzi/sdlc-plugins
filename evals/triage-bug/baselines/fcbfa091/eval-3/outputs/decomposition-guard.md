# Decomposition Guard -- ACME-502

## Trigger

The investigation of ACME-502 identified **two independent root causes** located in different modules with separate code paths. Per Step 6 of the triage-bug skill, the Decomposition Guard is triggered. The skill **stops here** and waits for user input before proceeding.

## Prompt Presented to User

> This bug appears to involve multiple independent issues:
>
> 1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`) -- The formatter applies kebab-case to section headings (producing `migration-patterns`) instead of preserving the original title case (`Migration Patterns`). This affects all convention references in generated Implementation Notes.
>
> 2. **Task creation uses wrong issue type ID** (in `plan-feature/SKILL.md` Step 6a) -- The task creation logic reads the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID, causing all generated tasks to be created as Feature issues.
>
> Options:
> 1. **Proceed** -- create a single Task covering all fixes
> 2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually
>
> Choose (1/2):

## Why the Guard Was Triggered

- The two root causes are in **different modules**: `shared/convention-utils.md` (shared formatting utilities) vs. `plan-feature/SKILL.md` (feature planning skill logic).
- They affect **different code paths**: convention reference formatting vs. Jira issue type selection during task creation.
- Each fix is **self-contained** and does not depend on the other -- fixing the case transform does not affect the issue type selection, and vice versa.
- This is **not** a single root cause manifesting across multiple files (which would not trigger the guard). These are genuinely independent defects that happen to be reported in the same Bug.

## What Happens Next

The skill **does not proceed** until the user responds:

- **If the user chooses 1 (Proceed)**: The skill continues to Step 5 and creates a single Task covering both fixes, with separate acceptance criteria for each root cause.
- **If the user chooses 2 (Split)**: The skill stops and suggests the user create two separate Bug issues -- one for the convention reference formatting problem and one for the issue type selection problem -- so each can be triaged and fixed independently.

No Task is created, no Jira comments are posted, and no links are established until the user makes their choice.
