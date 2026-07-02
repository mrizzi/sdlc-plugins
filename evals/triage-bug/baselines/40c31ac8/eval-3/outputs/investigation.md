# Triage Investigation: ACME-502

## Step 0 -- Validate Project Configuration

Configuration validated from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

All required sections present (Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration).

## Step 1 -- Fetch Bug

**Issue**: [ACME-502](https://mock-jira.example.com/browse/ACME-502)
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020) -- matches Bug issue type ID from configuration.
**Labels**: reported-by-user
**Component**: sdlc-workflow

### Parsed Description Sections

All required sections present per bug template:

| Section | Status |
|---------|--------|
| Issue Description | Present |
| Steps to Reproduce | Present |
| Expected Result | Present |
| Actual Result | Present |

Optional sections present: Attachments, Suggested Fix.

### Extracted Content

**Issue Description**: Two distinct problems occur when running `/plan-feature`: (1) generated task description has malformed Implementation Notes where convention references use the wrong section heading format (e.g., `§migration-patterns` instead of `§Migration Patterns`), and (2) the task is created with issue type "Feature" instead of "Task" when the project has a custom issue type scheme.

**Steps to Reproduce**:
1. Configure a project with a custom issue type scheme where Task has ID 10050.
2. Add a `CONVENTIONS.md` with section `## Migration Patterns`.
3. Run `/plan-feature ACME-200`.
4. Observe the generated task: check (a) Implementation Notes convention references and (b) the issue type.

**Expected Result**:
- Implementation Notes should reference conventions as `§Migration Patterns` (title case, matching the heading).
- The created issue should be of type Task (ID 10050).

**Actual Result**:
- Implementation Notes reference conventions as `§migration-patterns` (kebab-case, not matching the heading).
- The created issue is of type Feature (ID 10142) instead of Task.

**Suggested Fix** (from reporter): These are likely two separate bugs -- the convention reference formatter lowercases and kebab-cases headings incorrectly, and the task creation logic reads Feature issue type ID instead of Task issue type ID from configuration.

## Step 2 -- Reproduce/Trace

The bug involves a skill invocation (`/plan-feature`) and cannot be directly reproduced via CLI commands. Code-path tracing was used instead.

### Trace 1: Convention Reference Formatting

Entry point: `/plan-feature` skill invocation.
The plan-feature skill generates task descriptions with Implementation Notes that include convention references. These references are formatted using the shared convention utilities module.

Traced path:
- `/plan-feature` invokes convention lookup for the target repository's `CONVENTIONS.md`.
- The convention reference formatter in `shared/convention-utils.md` processes section headings from CONVENTIONS.md to produce `§<reference>` notation.
- The formatter applies a `lowercase + kebab-case` transform to the heading text (e.g., `## Migration Patterns` becomes `§migration-patterns`).
- This is incorrect -- the reference should preserve the original heading text as title case: `§Migration Patterns`.

### Trace 2: Task Creation Issue Type

Entry point: `/plan-feature` skill invocation, task creation step.
The plan-feature skill creates a Jira issue for each planned task.

Traced path:
- `plan-feature/SKILL.md` Step 6a handles task creation via `jira.create_issue`.
- The step retrieves the issue type ID from the Jira Configuration section of CLAUDE.md.
- It reads the **Feature issue type ID** (10142) instead of the **Task issue type ID**.
- In projects with custom issue type schemes where Task has a different ID (e.g., 10050), this causes the created issue to be of type "Feature" rather than "Task".

## Step 3 -- Codebase Investigation

### Target Repository

The component `sdlc-workflow` maps to the sdlc-plugins repository itself (the plugin source).

### Findings

#### Root Cause 1: Convention Reference Formatter (shared/convention-utils.md)

- **Affected file**: `shared/convention-utils.md`
- **Defect**: The convention reference formatter applies a `lowercase + kebab-case` transform to CONVENTIONS.md section headings when generating `§` references. This produces references like `§migration-patterns` instead of preserving the original title case as `§Migration Patterns`.
- **What is broken**: The string transformation function that converts headings to section references.
- **Why it is broken**: The formatter assumes section references should be URL-slug-like identifiers (lowercase, kebab-case) rather than human-readable title-case references matching the original headings.

#### Root Cause 2: Task Creation Issue Type (plan-feature/SKILL.md Step 6a)

- **Affected file**: `plan-feature/SKILL.md` (Step 6a)
- **Defect**: The task creation logic reads the `Feature issue type ID` (10142) from Jira Configuration when creating task issues, instead of using a dedicated `Task issue type ID` value.
- **What is broken**: The issue type ID selection in the task creation step.
- **Why it is broken**: The step references the wrong configuration field. It uses `Feature issue type ID` (intended for Feature-type issues) when it should use a Task-specific issue type ID (10050 in the reporter's configuration).

### Independence Assessment

These two root causes are **independent**:

- They reside in **different modules**: `shared/convention-utils.md` vs. `plan-feature/SKILL.md`.
- They affect **different code paths**: convention reference formatting vs. Jira issue creation.
- They produce **different symptoms**: malformed text content vs. wrong issue type.
- Fixing one does not fix the other.
- They could each be reproduced in isolation.

## Step 4 -- Root Cause Analysis

### Root Cause Summary

ACME-502 reports two symptoms that are caused by two independent defects in separate modules:

1. **Convention reference case transform** (`shared/convention-utils.md`): The convention reference formatter lowercases and kebab-cases CONVENTIONS.md section headings when generating `§` references, producing `§migration-patterns` instead of `§Migration Patterns`. The formatter should preserve the original title case of the heading.

2. **Wrong issue type ID in task creation** (`plan-feature/SKILL.md` Step 6a): The task creation logic retrieves the Feature issue type ID (10142) from Jira Configuration instead of using the Task issue type ID (10050). This causes tasks to be created as Features in projects with custom issue type schemes.

### Reproducer Strategy

**For Root Cause 1**: Create a CONVENTIONS.md with a section `## Migration Patterns`. Run the convention reference formatter and assert the output is `§Migration Patterns` (not `§migration-patterns`).

**For Root Cause 2**: Configure a project with Task issue type ID 10050. Run task creation and assert the created issue has issue type ID 10050 (not 10142).

### Decomposition Trigger

Because these are two independent root causes in different modules, the **Decomposition Guard (Step 6)** is triggered. A single Task should not bundle both fixes -- the user must decide whether to proceed with one combined Task or split into separate Bugs.
