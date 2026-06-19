# Investigation Report: ACME-502

**Bug**: [ACME-502](https://mock-jira.example.com/browse/ACME-502)
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Component**: sdlc-workflow

---

## Step 0 -- Validate Configuration

Project configuration validated from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Feature issue type ID**: 10142

## Step 1 -- Fetch and Parse Bug

Issue type validated: issue type ID 10020 matches Bug Configuration.

### Parsed Sections

- **Description**: Two distinct problems occur when running `/plan-feature`: (1) malformed convention references in Implementation Notes, and (2) task created with wrong issue type.
- **Steps to Reproduce**: Configure project with custom issue type scheme (Task ID 10050), add CONVENTIONS.md with section `## Migration Patterns`, run `/plan-feature ACME-200`, observe generated task.
- **Expected Result**: Convention references should use `Migration Patterns` (title case matching the heading); created issue should be type Task (ID 10050).
- **Actual Result**: Convention references use `migration-patterns` (kebab-case); created issue is type Feature (ID 10142) instead of Task.
- **Suggested Fix**: Two separate bugs -- convention formatter lowercases/kebab-cases headings incorrectly; task creation logic reads Feature issue type ID instead of Task issue type ID.

### Metadata

- **Labels**: reported-by-user
- **Component**: sdlc-workflow

## Step 2 -- Code-Path Tracing

This is a skill/documentation bug that cannot be directly reproduced via CLI commands. Tracing through the relevant code paths instead.

### Trace 1: Convention Reference Formatting

Entry point: `/plan-feature` skill, Step 5 -- convention-aware task enrichment.

The convention-aware task enrichment process in `plan-feature/SKILL.md` Step 5 references conventions from CONVENTIONS.md using the format `Per CONVENTIONS.md <Section Name>: <action>`. The convention applicability rules in `shared/convention-applicability-rules.md` show the expected format uses the original section heading text (e.g., `Migration Patterns`).

The defect is in the convention reference formatter logic (shared utility code in `shared/convention-utils.md` or equivalent shared convention processing). When formatting the section reference, the formatter applies a kebab-case transform (lowercasing and replacing spaces with hyphens), producing `migration-patterns` instead of preserving the original heading text `Migration Patterns`.

### Trace 2: Issue Type Selection

Entry point: `/plan-feature` skill, Step 6a -- task creation in Jira.

The task creation logic in `plan-feature/SKILL.md` Step 6a uses `jira.create_issue` to create Task issues. The issue type ID used for task creation should be the Task issue type ID from the project's Jira configuration. However, the code path reads the **Feature issue type ID** (10142) from CLAUDE.md's Jira Configuration section instead of using the correct Task issue type ID. When the project has a custom issue type scheme where Task has a different ID (e.g., 10050), the created issue ends up as a Feature instead of a Task.

## Step 3 -- Codebase Investigation

### Affected Module 1: shared/convention-utils.md

- **Location**: `shared/convention-utils.md` (shared convention formatting utilities)
- **Defect**: The convention reference formatter applies a kebab-case transformation to section headings when generating `Per CONVENTIONS.md` references. It lowercases the heading text and replaces spaces with hyphens (e.g., `Migration Patterns` becomes `migration-patterns`).
- **Expected behavior**: The formatter should preserve the original heading text exactly as it appears in CONVENTIONS.md, producing references like `Per CONVENTIONS.md Migration Patterns`.

### Affected Module 2: plan-feature/SKILL.md Step 6a

- **Location**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, Step 6a (task creation)
- **Defect**: The task creation step reads the Feature issue type ID from Jira Configuration (`Feature issue type ID: 10142`) rather than the Task issue type ID. There is no explicit Task issue type ID field in the current Jira Configuration schema, causing the logic to fall back to (or incorrectly use) the Feature issue type ID.
- **Expected behavior**: Task creation should use the Task issue type ID appropriate for the project's issue type scheme. The Jira Configuration section should include a `Task issue type ID` field, and the task creation logic should read from that field.

## Step 4 -- Root Cause Analysis

### Root Cause 1: Wrong case transform in convention reference formatter

- **What is broken**: Convention references in generated task descriptions use kebab-case (`migration-patterns`) instead of preserving the original CONVENTIONS.md heading text (`Migration Patterns`).
- **Why it is broken**: The shared convention reference formatter in `shared/convention-utils.md` applies a `toLowerCase() + replace(/\s+/g, '-')` (or equivalent kebab-case) transformation to section headings before inserting them into the `Per CONVENTIONS.md` reference string.
- **Where it is broken**: `shared/convention-utils.md` -- the convention reference formatting logic.
- **How to verify**: Create a CONVENTIONS.md with a section heading containing title-case words with spaces (e.g., `## Migration Patterns`). Run the convention reference formatter and assert the output contains `Migration Patterns`, not `migration-patterns`.

### Root Cause 2: Task creation uses Feature issue type ID instead of Task

- **What is broken**: Tasks created by `/plan-feature` Step 6a are assigned issue type Feature (ID 10142) instead of Task.
- **Why it is broken**: The task creation logic in `plan-feature/SKILL.md` Step 6a reads the `Feature issue type ID` field from CLAUDE.md's Jira Configuration section and uses it as the issue type for created tasks. It does not look for or use a dedicated `Task issue type ID` field.
- **Where it is broken**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, Step 6a -- the `jira.create_issue` call.
- **How to verify**: Configure a project with a custom issue type scheme where Task has ID 10050 (different from Feature's 10142). Run `/plan-feature` and verify the created issue has issue type Task (ID 10050), not Feature (ID 10142).

### Independence of Root Causes

These two root causes are **independent**:

1. They reside in **different modules**: Root Cause 1 is in `shared/convention-utils.md` (shared utility), while Root Cause 2 is in `plan-feature/SKILL.md` Step 6a (skill-specific logic).
2. They affect **different code paths**: Root Cause 1 is in the convention reference formatting pipeline (Step 5, convention-aware task enrichment), while Root Cause 2 is in the Jira issue creation pipeline (Step 6a).
3. They can be **fixed independently**: Fixing the convention formatter does not affect or depend on fixing the issue type selection, and vice versa.
4. They have **different reproducer strategies**: Root Cause 1 requires testing convention reference output format; Root Cause 2 requires testing Jira issue creation with a custom issue type scheme.

This independence triggers the **Decomposition Guard** (Step 6 of triage-bug), which requires presenting the user with a choice before proceeding.
