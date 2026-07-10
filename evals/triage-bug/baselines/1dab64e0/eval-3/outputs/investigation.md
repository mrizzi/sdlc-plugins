# Triage-Bug Investigation: ACME-502

## Step 0 -- Validate Project Configuration

Configuration validated from project CLAUDE.md:

| Field | Value |
|-------|-------|
| Project key | ACME |
| Cloud ID | mock-cloud-id-for-eval |
| Feature issue type ID | 10142 |
| Bug issue type ID | 10020 |
| Bug template path | docs/templates/bug-template.md |
| Bug-to-Task link type | Blocks |

All required sections present: Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration.

## Step 1 -- Fetch Bug

**Issue**: [ACME-502](https://mock-jira.example.com/browse/ACME-502)
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020) -- matches Bug issue type ID (10020)
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow

### Parsed Description Sections

All required sections are present per the bug template:

**Issue Description**: Two distinct problems occur when running `/plan-feature`:
1. The generated task description has malformed Implementation Notes -- convention references use the wrong section heading format (e.g., `§migration-patterns` instead of `§Migration Patterns`).
2. The task is created with issue type "Feature" instead of "Task" when the project has a custom issue type scheme.

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

**Attachments**: None.

**Suggested Fix** (optional): The reporter suggests these are likely two separate bugs -- one in the convention reference formatter and one in the task creation logic.

## Step 2 -- Reproduce/Trace

The Steps to Reproduce reference a skill invocation (`/plan-feature ACME-200`), which cannot be directly executed in a read-only triage context. Code-path tracing was performed instead.

### Trace 1 -- Convention reference formatting

- **Entry point**: `/plan-feature` skill invocation
- **Code path**: During task description generation, the skill formats convention references by reading section headings from `CONVENTIONS.md`. The convention formatter in `shared/convention-utils.md` is responsible for transforming heading text into `§`-prefixed references.
- **Divergence**: The formatter applies a slugify/kebab-case transformation to the heading text (e.g., "Migration Patterns" becomes "migration-patterns"), producing `§migration-patterns` instead of preserving the original title case as `§Migration Patterns`.

### Trace 2 -- Issue type selection during task creation

- **Entry point**: `/plan-feature` skill invocation, Step 6a (sub-task creation)
- **Code path**: When creating sub-task issues in Jira, the task creation logic in `plan-feature/SKILL.md` Step 6a reads the issue type ID to use for the `create_issue` call.
- **Divergence**: The logic reads `Feature issue type ID` (10142) from the Jira Configuration section instead of using the correct Task issue type ID (10050) from the project's issue type scheme. This causes all generated tasks to be created as Feature issues rather than Task issues.

## Step 3 -- Codebase Investigation

### Target repository

The bug affects the **sdlc-workflow** component. Per the Repository Registry, the relevant repository is **acme-backend** at `/home/dev/repos/acme-backend`, but the affected code is within the sdlc-workflow plugin itself.

No Serena instance is available for code intelligence. Investigation used read-only file inspection (Read/Grep/Glob fallback).

### Affected modules

Two independent modules are implicated:

1. **`shared/convention-utils.md`** -- Contains the convention reference formatter. This module provides the logic that reads `CONVENTIONS.md` section headings and produces `§`-prefixed references for use in task description Implementation Notes. The heading-to-reference conversion function applies an incorrect kebab-case transformation.

2. **`plan-feature/SKILL.md` Step 6a** -- Contains the task creation logic for sub-tasks. This step specifies which issue type ID to pass to the Jira `create_issue` call. It currently hardcodes or reads the Feature issue type ID from Jira Configuration rather than using the Task issue type ID.

### Key observation

These two modules are **independent** -- they do not share code paths, do not call each other, and address completely different concerns (text formatting vs. Jira API parameters). A fix to one has no bearing on the other.

## Step 4 -- Root Cause Analysis

### Root Cause 1 -- Malformed convention references

- **What is broken**: The convention reference formatter in `shared/convention-utils.md` produces kebab-case references (`§migration-patterns`) instead of preserving the original heading text (`§Migration Patterns`).
- **Why it is broken**: The formatter applies a slugify transformation (lowercase + hyphen-separated) to CONVENTIONS.md section headings before inserting them as `§`-prefixed references. This transformation is incorrect -- convention references should preserve the original heading text verbatim.
- **Where it is broken**: `shared/convention-utils.md` -- the function that converts a heading string to a `§`-prefixed reference.
- **How to verify the fix**: A reproducer test should:
  1. Provide a mock `CONVENTIONS.md` with a heading `## Migration Patterns`.
  2. Invoke the convention reference formatter.
  3. Assert the output contains `§Migration Patterns` (title case), not `§migration-patterns` (kebab-case).

### Root Cause 2 -- Wrong issue type on task creation

- **What is broken**: Tasks created by `/plan-feature` Step 6a use issue type "Feature" (ID 10142) instead of "Task" (ID 10050).
- **Why it is broken**: The task creation logic reads `Feature issue type ID` from the Jira Configuration section in CLAUDE.md, rather than determining the correct Task issue type ID. The Jira Configuration section only defines the Feature issue type ID; the Task issue type ID is part of the project's custom issue type scheme and is not explicitly configured.
- **Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the `issue_type` parameter in the `jira.create_issue` call.
- **How to verify the fix**: A reproducer test should:
  1. Configure a project with a custom issue type scheme where Task has ID 10050.
  2. Run the task creation logic from Step 6a.
  3. Assert the created issue has `issuetype.id` equal to 10050 (Task), not 10142 (Feature).

### Summary

The two root causes are **independent**:

| # | Root Cause | Module | Concern |
|---|-----------|--------|---------|
| 1 | Convention reference formatter slugifies headings to kebab-case | `shared/convention-utils.md` | Text formatting |
| 2 | Task creation uses Feature issue type ID instead of Task issue type ID | `plan-feature/SKILL.md` Step 6a | Jira API parameters |

Fixing one does not affect the other. They operate on different data, in different modules, at different points in the `/plan-feature` execution flow. This triggers the **Decomposition Guard** (Step 6) -- a single Task bundling both fixes would be inappropriate.

---

*This comment was AI-generated by [sdlc-workflow/triage-bug](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.1.*
