# Investigation Report: ACME-502

## Bug Summary

**Issue**: [ACME-502](https://mock-jira.example.com/browse/ACME-502)
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020)
**Component**: sdlc-workflow

## Step 0 -- Validate Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Feature issue type ID**: 10142

## Step 1 -- Fetch and Parse Bug

### Issue Type Validation

Issue type ID 10020 matches Bug Configuration's Bug issue type ID (10020). Validated.

### Parsed Description Sections

**Required Sections** (all present):

- **Description**: Two distinct problems occur when running `/plan-feature`: (1) malformed convention references in Implementation Notes using wrong heading format, (2) task created with "Feature" issue type instead of "Task" when project has custom issue type scheme.
- **Steps to Reproduce**: Configure project with custom issue type scheme (Task ID 10050), add CONVENTIONS.md with `## Migration Patterns`, run `/plan-feature ACME-200`, observe generated task.
- **Expected Result**: Convention references should be `Migration Patterns` (title case); created issue should be type Task (ID 10050).
- **Actual Result**: Convention references are `migration-patterns` (kebab-case); created issue is type Feature (ID 10142).

**Optional Sections**:

- **Suggested Fix**: Present -- reporter suspects two separate bugs in convention formatter and task creation logic.

### Metadata

- **Labels**: reported-by-user
- **Component**: sdlc-workflow

## Step 2 -- Code-Path Tracing

The bug references `/plan-feature` skill execution. Two independent code paths are involved:

### Trace 1: Convention Reference Formatting

Entry point: `/plan-feature` Step 5 (Generate Jira Tasks) invokes convention-aware task enrichment, which references conventions from CONVENTIONS.md by section heading. The formatting logic that produces the `Per CONVENTIONS.md ...` references is handled by the shared convention utilities module.

Traced path: When the formatter builds a convention reference string (e.g., `Per CONVENTIONS.md Migration Patterns`), it transforms the section heading. The expected behavior is to preserve the original title-case heading as written in CONVENTIONS.md (e.g., `Migration Patterns`). The actual behavior is that the formatter lowercases and kebab-cases the heading, producing `migration-patterns` instead.

### Trace 2: Task Creation Issue Type

Entry point: `/plan-feature` Step 6a (Create Tasks in Jira) calls `jira.create_issue`. The issue type ID passed to the create call determines whether the created issue is a Task or Feature.

Traced path: The task creation logic in `plan-feature/SKILL.md` Step 6a reads the issue type to use when creating tasks. The expected behavior is to use the Task issue type ID from the project's Jira Configuration (which for this project would be 10050 per the reporter's custom scheme). The actual behavior is that it uses the Feature issue type ID (10142) hardcoded or read from the `Feature issue type ID` field in Jira Configuration, rather than looking up a Task-specific issue type ID.

## Step 3 -- Codebase Investigation

### Root Cause 1: Convention Reference Formatter (shared/convention-utils.md)

**Affected file**: `shared/convention-utils.md` (shared convention utilities module)

**What is broken**: The convention reference formatter applies a lowercase + kebab-case transformation to CONVENTIONS.md section headings when building reference strings for task Implementation Notes.

**Why it is broken**: The formatter uses a case-transform function (lowercase then kebab-case) on the heading text, presumably to create URL-friendly anchors. However, the convention reference in the task description is a human-readable citation (e.g., `Per CONVENTIONS.md Migration Patterns:`), not a URL anchor. The heading should be preserved in its original title case as it appears in CONVENTIONS.md.

**Where it is broken**: The case-transform logic in `shared/convention-utils.md` that processes section headings before inserting them into Implementation Notes.

**How to verify**: A reproducer test should:
1. Provide a CONVENTIONS.md with a section heading `## Migration Patterns`
2. Run the convention reference formatter on this heading
3. Assert the output contains `Migration Patterns` (title case), not `migration-patterns` (kebab-case)

### Root Cause 2: Task Creation Issue Type (plan-feature/SKILL.md Step 6a)

**Affected file**: `plan-feature/SKILL.md` Step 6a (task creation logic)

**What is broken**: The task creation logic in Step 6a uses the Feature issue type ID (10142) from Jira Configuration when creating task issues, instead of using a Task issue type ID.

**Why it is broken**: The Jira Configuration section in CLAUDE.md contains `Feature issue type ID: 10142` but does not define a separate `Task issue type ID`. The plan-feature skill's Step 6a creates issues intended to be Tasks but reads the Feature issue type ID field, causing all created issues to be of type Feature rather than Task.

**Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the `jira.create_issue` call uses the Feature issue type ID from configuration rather than a Task-specific issue type ID.

**How to verify**: A reproducer test should:
1. Configure a project with `Feature issue type ID: 10142` and a custom task issue type ID (e.g., 10050)
2. Run `/plan-feature` to generate and create tasks
3. Assert that created issues have issue type Task (ID 10050), not Feature (ID 10142)

## Root Cause Summary

| # | Root Cause | Affected Module | File |
|---|-----------|----------------|------|
| 1 | Convention reference formatter lowercases and kebab-cases headings instead of preserving original title case | Shared convention utilities | `shared/convention-utils.md` |
| 2 | Task creation uses Feature issue type ID (10142) instead of Task issue type ID from config | Plan-feature task creation | `plan-feature/SKILL.md` Step 6a |

## Independence Assessment

These two root causes are **independent**:

- **Different modules**: Root cause 1 is in the shared convention utilities (`shared/convention-utils.md`), while root cause 2 is in the plan-feature skill logic (`plan-feature/SKILL.md` Step 6a).
- **Different code paths**: Root cause 1 is triggered during convention-aware task enrichment (Step 5 content generation), while root cause 2 is triggered during Jira issue creation (Step 6a API call).
- **No shared state**: Fixing one does not affect the other. The convention formatting bug produces wrong text content in the task description; the issue type bug creates the task with the wrong Jira issue type. These are orthogonal concerns.
- **Independent fixes**: Each can be fixed and tested independently without any interaction between the two changes.

**Conclusion**: The Decomposition Guard (Step 6) must be triggered because the bug involves multiple independent root causes in different modules requiring separate fixes.
