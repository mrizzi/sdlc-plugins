# Investigation Report: ACME-502

## Bug Summary

**Issue**: [ACME-502](https://mock-jira.example.com/browse/ACME-502)
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Component**: sdlc-workflow

## Step 0 -- Validate Configuration

Configuration validated from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020 (matches issue type on ACME-502)
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Feature issue type ID**: 10142 (from Jira Configuration)

## Step 1 -- Fetch and Parse Bug

All required sections present per the bug template:

| Section | Status |
|---------|--------|
| Issue Description | Present |
| Steps to Reproduce | Present |
| Expected Result | Present |
| Actual Result | Present |
| Attachments | Present (None) |
| Suggested Fix | Present (optional) |

### Parsed Description

**Steps to Reproduce:**
1. Configure a project with a custom issue type scheme where Task has ID 10050.
2. Add a `CONVENTIONS.md` with section `## Migration Patterns`.
3. Run `/plan-feature ACME-200`.
4. Observe the generated task: check (a) Implementation Notes convention references and (b) the issue type.

**Expected Result:**
- Implementation Notes should reference conventions as `Migration Patterns` (title case, matching the heading).
- The created issue should be of type Task (ID 10050).

**Actual Result:**
- Implementation Notes reference conventions as `migration-patterns` (kebab-case, not matching the heading).
- The created issue is of type Feature (ID 10142) instead of Task.

## Step 2 -- Code-Path Tracing

The bug involves the `/plan-feature` skill. Since this is a skill/documentation bug affecting how the skill generates output and creates Jira issues, direct reproduction is not applicable. Instead, the two reported problems were traced through the relevant code paths.

### Trace 1: Convention Reference Formatting

Entry point: `/plan-feature` invocation. When generating Implementation Notes, the skill calls a convention reference formatter to produce section references (e.g., `Migration Patterns`). The formatter is located in the shared utilities module.

Traced to: `shared/convention-utils.md` -- the convention reference formatting logic. The formatter applies a `toKebabCase()` transform to section headings before inserting them as references. This produces `migration-patterns` instead of preserving the original title-case heading text `Migration Patterns`.

### Trace 2: Task Issue Type Selection

Entry point: `/plan-feature` invocation, at the point where the task issue is created in Jira. The skill reads the issue type ID from the project configuration to determine what type of issue to create.

Traced to: `plan-feature/SKILL.md` Step 6a -- the task creation logic. The code reads the `Feature issue type ID` (10142) from CLAUDE.md Jira Configuration instead of reading the `Task issue type ID` from the project's issue type scheme. This causes all generated tasks to be created as Feature issues regardless of the project's configuration.

## Step 3 -- Codebase Investigation

### Affected Files and Modules

| # | File / Module | Affected Symbol / Section | Issue |
|---|---------------|--------------------------|-------|
| 1 | `shared/convention-utils.md` | Convention reference formatter (case transform logic) | Uses `toKebabCase()` on section headings instead of preserving original title case |
| 2 | `plan-feature/SKILL.md` Step 6a | Task creation issue type selection | Reads `Feature issue type ID` (10142) instead of `Task issue type ID` from configuration |

### Independence Assessment

These two problems are **independent**:

- **Different modules**: Root cause 1 is in `shared/convention-utils.md` (shared formatting utilities), while root cause 2 is in `plan-feature/SKILL.md` (feature planning skill logic).
- **Different code paths**: The convention formatter runs during Implementation Notes generation; the issue type selection runs during Jira issue creation. These are separate phases of the `/plan-feature` execution.
- **No shared state**: The convention formatting output does not influence the issue type selection, and vice versa. Fixing one does not affect the other.
- **Independent fixes**: Each root cause requires a separate, self-contained change to a different file.

## Step 4 -- Root Cause Analysis

### Root Cause 1: Wrong Case Transform in Convention Reference Formatter

- **What is broken**: The convention reference formatter in `shared/convention-utils.md` applies a kebab-case transform (`toKebabCase()`) to CONVENTIONS.md section headings when generating `section-reference` notation for Implementation Notes.
- **Why it is broken**: The formatter was implemented to normalize headings to a URL-friendly slug format (kebab-case), but convention references in Implementation Notes should preserve the original heading text in title case to match the source document. The transform discards capitalization and replaces spaces with hyphens.
- **Where it is broken**: `shared/convention-utils.md` -- the case transform function applied to section heading text.
- **How to verify**: A reproducer test should create a CONVENTIONS.md with a multi-word titled section (e.g., `## Migration Patterns`), run the formatter, and assert the output reference uses `Migration Patterns` (title case) rather than `migration-patterns` (kebab-case).

### Root Cause 2: Wrong Issue Type ID in Task Creation

- **What is broken**: The task creation logic in `plan-feature/SKILL.md` Step 6a uses the `Feature issue type ID` (10142) from CLAUDE.md Jira Configuration when creating task issues, instead of reading the correct Task issue type ID.
- **Why it is broken**: The code path that selects the issue type ID references the wrong configuration field. It reads `Feature issue type ID` unconditionally rather than using a Task-specific issue type ID (which may be configured per-project or derived from the issue type scheme).
- **Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the `create_issue` call's issue type parameter.
- **How to verify**: A reproducer test should configure a project with a custom issue type scheme where Task has a distinct ID (e.g., 10050), run `/plan-feature`, and assert the created issue has `issuetype.id` equal to the Task ID (10050), not the Feature ID (10142).

## Conclusion

The investigation reveals **two independent root causes** in **different modules** with **different code paths**. This triggers the Decomposition Guard (Step 6) -- the skill must pause and present the user with the option to proceed with a single bundled Task or split into separate Bug issues for each independent fix. See `decomposition-guard.md` for the guard prompt.
