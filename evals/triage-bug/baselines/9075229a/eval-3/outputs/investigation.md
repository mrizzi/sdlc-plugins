# Codebase Investigation Findings -- ACME-502

## Summary

Investigation of Bug ACME-502 ("Skill output is malformed and task creation uses wrong issue type") reveals **two independent root causes** in different modules with different code paths. These are not two manifestations of a single defect -- they are separate bugs that happen to be observed together when running `/plan-feature`.

---

## Root Cause 1: Convention reference formatter produces wrong heading format

**Affected file:** `shared/convention-utils.md`

**Code path:** When `/plan-feature` generates a task description with Implementation Notes, it calls the convention reference formatter in `shared/convention-utils.md` to produce section references (e.g., `§Migration Patterns`) from CONVENTIONS.md headings. The formatter applies a case transformation that lowercases the heading text and converts spaces to hyphens (kebab-case), producing `§migration-patterns` instead of preserving the original title case `§Migration Patterns`.

**What is broken:** The convention reference formatter transforms headings by lowercasing and kebab-casing them. For a CONVENTIONS.md heading `## Migration Patterns`, the formatter produces `§migration-patterns` instead of `§Migration Patterns`.

**Why it is broken:** The formatter applies a slug-style transformation (lowercase + kebab-case) that is appropriate for URL anchors but incorrect for human-readable convention references in task descriptions. The convention reference format should preserve the original title case of the heading as it appears in CONVENTIONS.md.

**Expected behavior:** Convention references in Implementation Notes should read `§Migration Patterns`, matching the original heading text verbatim.

**Actual behavior:** Convention references in Implementation Notes read `§migration-patterns`, a kebab-cased slug that does not match the heading.

---

## Root Cause 2: Task creation uses Feature issue type ID instead of Task issue type ID

**Affected file:** `plan-feature/SKILL.md` (Step 6a -- task creation logic)

**Code path:** When `/plan-feature` creates a Task issue in Jira (Step 6a), it reads the issue type ID from the project's CLAUDE.md Jira Configuration section. The logic reads the **Feature issue type ID** (10142) instead of looking up the **Task issue type ID** (10050). As a result, the created issue has type "Feature" instead of "Task".

**What is broken:** The task creation step in `plan-feature/SKILL.md` Step 6a uses the wrong field from Jira Configuration. It reads `Feature issue type ID: 10142` and passes that as the issue type when creating the task.

**Why it is broken:** The task creation logic does not distinguish between the Feature issue type and the Task issue type. It references the Feature issue type ID field from the Jira Configuration section rather than resolving the correct Task issue type ID (10050) for the project's custom issue type scheme.

**Expected behavior:** Created issues should be of type Task (issue type ID 10050) as defined in the project's custom issue type scheme.

**Actual behavior:** Created issues are of type Feature (issue type ID 10142) because the logic reads the Feature issue type ID from CLAUDE.md Jira Configuration.

---

## Independence Confirmation

These two root causes are **independent**:

- **Different modules:** Root Cause 1 is in `shared/convention-utils.md` (shared utility for formatting convention references). Root Cause 2 is in `plan-feature/SKILL.md` (skill-specific task creation logic).
- **Different code paths:** Root Cause 1 occurs during task description generation (convention reference formatting). Root Cause 2 occurs during Jira API issue creation (issue type ID selection). They execute at different stages of the `/plan-feature` workflow.
- **Different fix scope:** Fixing one does not affect or resolve the other. The convention formatter fix is about string transformation logic; the task creation fix is about reading the correct configuration field.
- **Either can be fixed independently:** A fix to the convention reference formatter would produce correct `§Migration Patterns` references regardless of the issue type bug, and vice versa.
