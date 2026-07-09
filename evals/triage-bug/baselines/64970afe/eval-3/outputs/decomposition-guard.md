# Decomposition Guard — ACME-502

Investigation of ACME-502 reveals **two independent root causes** in different modules and code paths. The Decomposition Guard requires your decision before proceeding.

---

## Issue 1: Malformed convention references (wrong case transform)

- **Affected module**: `shared/convention-utils.md`
- **Problem**: The convention reference formatter lowercases and kebab-cases section headings (e.g., `§migration-patterns`) instead of preserving the original title case (`§Migration Patterns`).
- **Fix**: Update the case transform logic in the convention formatter to preserve the original heading text.

## Issue 2: Task creation uses wrong issue type ID

- **Affected module**: `plan-feature/SKILL.md` Step 6a
- **Problem**: Task creation reads the Feature issue type ID (`10142`) from CLAUDE.md instead of the Task issue type ID, causing tasks to be created as Feature issues.
- **Fix**: Change the config field read from `Feature issue type ID` to `Task issue type ID`.

---

These issues are in **different modules** (`shared/convention-utils.md` vs `plan-feature/SKILL.md`), follow **different code paths** (text formatting vs Jira API issue creation), and are **independently fixable**.

## Options

1. **Proceed** — Create a single Task under ACME-502 that addresses both root causes in one fix.
2. **Split** — Create two separate Bug issues, one for each root cause, so they can be tracked and fixed independently.

Choose (1/2):
