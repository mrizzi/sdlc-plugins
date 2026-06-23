# Decomposition Guard — ACME-502

This bug appears to involve multiple independent issues:

1. **Malformed convention references** — the convention reference formatter in `shared/convention-utils.md` transforms CONVENTIONS.md section headings into kebab-case slugs (e.g., `§migration-patterns`) instead of preserving the original heading text (e.g., `§Migration Patterns`). This affects task description generation during Step 5 of plan-feature.

2. **Wrong issue type in task creation** — the task creation logic in `plan-feature/SKILL.md` Step 6a uses the Feature issue type ID (10142) from Jira Configuration instead of a Task issue type ID, causing created tasks to have the wrong issue type when the project has a custom issue type scheme.

These two problems are caused by independent code paths in different modules:
- Issue 1 is in the shared convention formatting utilities, invoked during task description generation.
- Issue 2 is in the plan-feature task creation logic, invoked during Jira issue creation.

A fix to one does not affect or depend on the other.

Options:
1. **Proceed** — create a single Task covering all fixes
2. **Split** — I recommend creating separate Bugs for each independent issue, then triaging each one individually

Choose (1/2):
