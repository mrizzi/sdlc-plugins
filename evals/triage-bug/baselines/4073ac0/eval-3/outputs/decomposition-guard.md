# Decomposition Guard -- ACME-502

This bug appears to involve multiple independent issues:

1. **Convention reference formatter uses wrong case transform** (in `shared/convention-utils.md`)
   The shared convention reference formatter applies a kebab-case transformation to CONVENTIONS.md section headings, producing references like `migration-patterns` instead of preserving the original heading text `Migration Patterns`. This affects the Implementation Notes of all generated task descriptions that reference conventions.

2. **Task creation uses Feature issue type ID instead of Task** (in `plan-feature/SKILL.md` Step 6a)
   The task creation logic reads the `Feature issue type ID` (10142) from Jira Configuration and uses it as the issue type when creating Tasks via `jira.create_issue`. When the project has a custom issue type scheme with a different Task ID (e.g., 10050), all created tasks are incorrectly assigned the Feature issue type.

These two root causes are in **different modules** and affect **different code paths**:
- Root Cause 1 is in the shared convention formatting utilities (`shared/convention-utils.md`), invoked during Step 5 (convention-aware task enrichment).
- Root Cause 2 is in the plan-feature skill logic (`plan-feature/SKILL.md`), invoked during Step 6a (Jira task creation).

They can be fixed and tested independently.

---

## Options

1. **Proceed** -- create a single Task covering both fixes (convention formatter fix in `shared/convention-utils.md` and issue type fix in `plan-feature/SKILL.md` Step 6a)
2. **Split** -- I recommend creating separate Bugs for each independent issue, then triaging each one individually:
   - Bug A: "Convention reference formatter uses wrong case transform" (affects `shared/convention-utils.md`)
   - Bug B: "Task creation uses Feature issue type ID instead of Task" (affects `plan-feature/SKILL.md` Step 6a)

Choose (1/2):

---

*The skill stops here and waits for user input before proceeding. No Task will be created until the user chooses an option. This ensures the user explicitly decides whether to bundle unrelated fixes into a single Task or split them into separate Bug issues for independent triage.*
