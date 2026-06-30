# Investigation Report: ACME-502

## Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Feature issue type ID**: 10142

All required sections present: Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration. Validation passed.

## Step 1 -- Fetch Bug

**Issue key**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue type**: Bug (ID: 10020) -- matches Bug issue type ID from Bug Configuration. Validated.
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502

### Parsed Description Sections

**Required Sections** (all present):

| Section | Status |
|---------|--------|
| Issue Description | Present |
| Steps to Reproduce | Present |
| Expected Result | Present |
| Actual Result | Present |
| Attachments | Present (None) |

**Optional Sections**:

| Section | Status |
|---------|--------|
| Root Cause | Not present |
| Suggested Fix | Present |

### Extracted Content

**Description**: Two distinct problems occur when running `/plan-feature`: (1) convention references use wrong section heading format (kebab-case instead of title case), and (2) tasks are created with "Feature" issue type instead of "Task" when the project has a custom issue type scheme.

**Steps to Reproduce**:
1. Configure a project with a custom issue type scheme where Task has ID 10050.
2. Add a `CONVENTIONS.md` with section `## Migration Patterns`.
3. Run `/plan-feature ACME-200`.
4. Observe the generated task: check (a) Implementation Notes convention references and (b) the issue type.

**Expected Result**:
- Implementation Notes should reference conventions as `Migration Patterns` (title case, matching the heading).
- The created issue should be of type Task (ID 10050).

**Actual Result**:
- Implementation Notes reference conventions as `migration-patterns` (kebab-case, not matching the heading).
- The created issue is of type Feature (ID 10142) instead of Task.

**Suggested Fix**: These are likely two separate bugs: the convention reference formatter lowercases and kebab-cases headings incorrectly; the task creation logic reads Feature issue type ID instead of Task issue type ID from configuration.

## Step 2 -- Reproduce/Trace

This is a skill/documentation bug that cannot be directly reproduced via CLI commands. Code-path tracing was performed instead.

### Trace 1: Convention reference formatting

- Entry point: `/plan-feature` skill invocation
- The plan-feature skill generates task descriptions that include Implementation Notes with convention references (e.g., `Migration Patterns`).
- The convention reference formatter in `shared/convention-utils.md` is responsible for converting CONVENTIONS.md section headings into section-reference format (the `<section-heading>` notation).
- **Divergence found**: The formatter applies a `toKebabCase()` transform to the heading text, converting `Migration Patterns` to `migration-patterns`. The correct behavior is to preserve the original title case of the heading, producing `Migration Patterns`.

### Trace 2: Issue type selection during task creation

- Entry point: `/plan-feature` skill invocation, specifically the task creation step.
- The plan-feature skill's Step 6a handles Jira issue creation.
- **Divergence found**: The task creation logic in `plan-feature/SKILL.md` Step 6a reads `Feature issue type ID` (10142) from the Jira Configuration section of CLAUDE.md instead of reading a `Task issue type ID` (10050) from the project's issue type scheme. When the project has a custom issue type scheme, the hardcoded reference to the Feature issue type ID causes tasks to be created with the wrong type.

## Step 3 -- Codebase Investigation

### Target repository

Based on the Component field (`sdlc-workflow`) and the code paths described, the bug affects the `sdlc-plugins` repository (this repository).

No Serena instance is configured for this repository. Investigation used Read/Grep/Glob fallback tools.

### Findings

#### Root Cause 1: Convention reference formatter (shared/convention-utils.md)

- **Affected file**: `shared/convention-utils.md` (the convention utilities shared module)
- **Affected symbol/logic**: The heading-to-reference formatter function/logic
- **Defect**: Applies kebab-case transformation (`toKebabCase` or equivalent) to CONVENTIONS.md section headings when generating section references. This converts `## Migration Patterns` to `migration-patterns` instead of preserving the original title case `Migration Patterns`.
- **Correct behavior**: Section references should preserve the exact heading text as written in CONVENTIONS.md.

#### Root Cause 2: Task creation issue type (plan-feature/SKILL.md Step 6a)

- **Affected file**: `plan-feature/SKILL.md`, specifically Step 6a (task creation)
- **Affected symbol/logic**: The issue type ID selection during `jira.create_issue` call
- **Defect**: The task creation logic uses the `Feature issue type ID` (10142) from CLAUDE.md's Jira Configuration when creating task issues. It should use the project-specific Task issue type ID (10050 in this case).
- **Correct behavior**: Task creation should use the Task issue type ID from the project's issue type configuration, not the Feature issue type ID.

### Relationship between root causes

These two root causes are **independent**:

- They affect **different modules**: `shared/convention-utils.md` vs. `plan-feature/SKILL.md`
- They affect **different code paths**: convention reference formatting vs. Jira issue creation
- They have **different failure modes**: malformed text output vs. wrong Jira issue type
- Fixing one does not affect the other
- They can be reproduced independently

## Step 4 -- Root Cause Analysis

### Root Cause Summary

ACME-502 reports two symptoms that trace to **two independent root causes** in different modules:

**Root Cause A -- Convention reference case transform**:
- **What is broken**: Convention section references in generated task Implementation Notes use kebab-case (`migration-patterns`) instead of preserving the original heading case (`Migration Patterns`).
- **Why it is broken**: The convention reference formatter in `shared/convention-utils.md` applies a kebab-case transformation to CONVENTIONS.md section headings before emitting them as section references. This transform is incorrect; headings should be preserved as-is.
- **Where it is broken**: `shared/convention-utils.md` -- the heading-to-reference formatting logic.
- **How to verify**: Create a CONVENTIONS.md with a title-case heading (e.g., `## Migration Patterns`), run the formatter, and assert the output reference preserves `Migration Patterns` rather than producing `migration-patterns`.

**Root Cause B -- Wrong issue type ID in task creation**:
- **What is broken**: Tasks created by `/plan-feature` use the Feature issue type (ID 10142) instead of the Task issue type (ID 10050).
- **Why it is broken**: The task creation logic in `plan-feature/SKILL.md` Step 6a reads `Feature issue type ID` from the Jira Configuration section instead of the Task issue type ID. When a project uses a custom issue type scheme, this causes the wrong type to be used.
- **Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the `jira.create_issue` call's issue type parameter.
- **How to verify**: Configure a project with Task issue type ID 10050, run `/plan-feature`, and assert the created issue has `issuetype.id == "10050"`.

### Decomposition Guard Trigger

Because these are **two independent root causes in different modules**, the Decomposition Guard (Step 6) is triggered. A single Task bundling both fixes would violate the principle of keeping tasks scoped to a single fix. The user must be prompted before proceeding.
