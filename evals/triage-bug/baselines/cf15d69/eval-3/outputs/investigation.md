# Investigation Findings: ACME-502

## Bug Summary

**Key**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Component**: sdlc-workflow

Two distinct problems occur when running `/plan-feature`: (1) convention references in generated task descriptions use wrong heading format, and (2) tasks are created with the wrong Jira issue type.

---

## Step 2 -- Reproduce/Trace

The bug cannot be directly reproduced (it involves skill behavior and Jira issue creation). Code-path tracing was used instead.

### Trace 1: Convention reference formatting

Entry point: `/plan-feature` invocation generating Implementation Notes that reference CONVENTIONS.md headings.

The execution path flows through the convention reference formatter in `shared/convention-utils.md`. When the formatter encounters a CONVENTIONS.md heading such as `## Migration Patterns`, it transforms the heading text into a section reference. The current logic lowercases the heading and converts spaces to hyphens (kebab-case), producing `migration-patterns`. The resulting reference is output as `§migration-patterns`.

Expected behavior: the formatter should preserve the original title case of the heading, producing `§Migration Patterns`.

### Trace 2: Task issue type selection

Entry point: `/plan-feature` task creation step.

The execution path flows through `plan-feature/SKILL.md` Step 6a, which creates a Jira issue for the planned task. The creation logic reads the issue type ID from the project's Jira Configuration. The current logic uses the **Feature issue type ID** (10142) from CLAUDE.md rather than the Task issue type ID. When the project has a custom issue type scheme with a distinct Task issue type (e.g., ID 10050), the created issue is incorrectly typed as Feature.

---

## Step 3 -- Codebase Investigation

### Root Cause 1: Convention reference formatter (shared/convention-utils.md)

- **Affected file**: `shared/convention-utils.md`
- **Defect**: The convention reference formatting logic applies a lowercase + kebab-case transform to CONVENTIONS.md section headings when generating `§`-prefixed references. This destroys the original title case of the heading.
- **Correct behavior**: The formatter should preserve the heading text as-is (title case), producing references like `§Migration Patterns` that match the actual CONVENTIONS.md heading.

### Root Cause 2: Task creation issue type (plan-feature/SKILL.md Step 6a)

- **Affected file**: `plan-feature/SKILL.md` (Step 6a)
- **Defect**: The task creation step reads the `Feature issue type ID` (10142) from Jira Configuration and uses it when creating Task issues. It should instead use the Task issue type ID appropriate for the project's issue type scheme.
- **Correct behavior**: The task creation logic should use the correct Task issue type ID (e.g., 10050 in the reporter's project), not the Feature issue type ID.

---

## Step 4 -- Root Cause Analysis

### Independence Assessment

These two root causes are **independent**:

1. **Different modules**: Root cause 1 is in `shared/convention-utils.md` (a shared utility for formatting convention references). Root cause 2 is in `plan-feature/SKILL.md` Step 6a (the task creation logic specific to plan-feature).
2. **Different code paths**: The convention formatter runs during description generation (building the Implementation Notes content). The issue type selection runs during Jira API invocation (creating the issue). These are separate phases of the plan-feature workflow.
3. **Different fix scopes**: Fixing the convention formatter requires changing the case transform logic in shared/convention-utils.md. Fixing the issue type requires changing the configuration field read in plan-feature/SKILL.md. Neither fix depends on the other.

### Root Cause Summary

| # | Root Cause | Affected File | What Is Broken | Why It Is Broken |
|---|-----------|---------------|----------------|------------------|
| 1 | Convention reference uses wrong case transform | `shared/convention-utils.md` | `§`-prefixed references render headings as kebab-case (e.g., `§migration-patterns`) | The formatter lowercases and kebab-cases the heading text instead of preserving title case |
| 2 | Task created with wrong issue type | `plan-feature/SKILL.md` Step 6a | Tasks are created as Feature (ID 10142) instead of Task | The creation logic reads `Feature issue type ID` from configuration instead of the Task issue type ID |

### Reproducer Strategies

1. **Convention reference fix**: Provide a CONVENTIONS.md with a multi-word title-case heading (e.g., `## Migration Patterns`). Run the convention reference formatter and assert the output is `§Migration Patterns`, not `§migration-patterns`.
2. **Issue type fix**: Configure a project with a custom issue type scheme where Task has a distinct ID (e.g., 10050). Run `/plan-feature` and assert the created issue's `issuetype.id` matches the Task ID, not the Feature ID (10142).

---

## Decomposition Guard Triggered

Because the investigation found two independent root causes in different modules, the **Decomposition Guard (Step 6)** is triggered. See `decomposition-guard.md` for the user prompt.
