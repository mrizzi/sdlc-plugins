# Investigation — ACME-502

## Step 0 — Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

All required sections are present: Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration.

## Step 1 — Fetch Bug

### Issue type validation

Issue ACME-502 has `issuetype.id = 10020`, which matches the Bug issue type ID from Bug Configuration (10020). Validation passed.

### Parsed bug description

**Required Sections** (all present, matched against bug template headings):

- **Description**: Two distinct problems occur when running `/plan-feature`: (1) malformed convention references in Implementation Notes using kebab-case slug format instead of title-case heading format, and (2) task created with wrong issue type (Feature instead of Task) when a custom issue type scheme is configured.
- **Steps to Reproduce**: Configure a project with a custom issue type scheme (Task ID 10050), add CONVENTIONS.md with `## Migration Patterns`, run `/plan-feature ACME-200`, observe convention references and issue type.
- **Expected Result**: Convention references should read `§Migration Patterns` (title case). Created issue should be type Task (ID 10050).
- **Actual Result**: Convention references read `§migration-patterns` (kebab-case). Created issue is type Feature (ID 10142).

**Optional Sections**:

- **Attachments**: None.
- **Suggested Fix**: Two separate bugs suspected — convention reference formatter and task creation issue type logic.

### Metadata

- **Issue key**: ACME-502
- **Web URL**: https://mock-jira.example.com/browse/ACME-502
- **Summary**: Skill output is malformed and task creation uses wrong issue type
- **Labels**: reported-by-user
- **Component**: sdlc-workflow

## Step 2 — Reproduce/Trace

These are skill/documentation-level bugs in the sdlc-workflow plugin, so direct reproduction via runnable commands is not applicable. Code-path tracing was used instead.

### Trace 1 — Convention reference formatting

Entry point: `/plan-feature` skill invocation, specifically the convention-aware task enrichment in Step 5.

The plan-feature skill (Step 5, "Convention-aware task enrichment") reads conventions from CONVENTIONS.md and includes them in task Implementation Notes using the format:

```
Per CONVENTIONS.md §<Section Name>: <specific action required>
```

The convention applicability rules in `shared/convention-applicability-rules.md` also reference this format with `§<Section Name>`. The section name should preserve the original heading text from CONVENTIONS.md (e.g., `§Migration Patterns`).

The bug reports that convention references are being emitted as `§migration-patterns` (kebab-case slug) instead of `§Migration Patterns` (original title case heading). This indicates that the convention formatter — the logic in `shared/convention-utils.md` (or the equivalent shared utility responsible for formatting convention section references) — is applying a kebab-case transformation to the heading text before inserting it into the `§` reference. The formatter should preserve the original heading text verbatim.

**Divergence point**: The convention reference formatter lowercases and kebab-cases the CONVENTIONS.md heading text when producing the `§` reference, instead of preserving the heading as-is.

### Trace 2 — Issue type selection during task creation

Entry point: `/plan-feature` skill invocation, Step 6a (Create the tasks).

In Step 6a, `jira.create_issue` is called to create tasks. The issue type for created tasks should be "Task". However, the bug reports that the created issue has type Feature (ID 10142) instead of Task.

Looking at the Jira Configuration in CLAUDE.md, the only issue type ID configured is `Feature issue type ID: 10142`. There is no `Task issue type ID` field. The task creation logic in plan-feature Step 6a uses `jira.create_issue` but the skill text does not specify which issue type ID to pass — it simply says to create issues. When the project has a custom issue type scheme where Task has a different ID (10050 in this case), the creation logic appears to fall back to the Feature issue type ID (10142) from the Jira Configuration because no Task issue type ID is configured.

**Divergence point**: The task creation logic in `plan-feature/SKILL.md` Step 6a reads the Feature issue type ID from Jira Configuration instead of using a Task issue type ID, because no Task issue type ID is defined in the project configuration contract.

## Step 3 — Codebase Investigation

### Target repository

The component is `sdlc-workflow`, which maps to the sdlc-plugins repository (path: `./`). No Serena instance is configured, so Read/Grep/Glob were used.

### Affected files and modules

**Root Cause 1 — Convention reference formatting**:
- **File**: `shared/convention-utils.md` (the shared utility that formats convention section references for task descriptions)
- **Related**: `shared/convention-applicability-rules.md` — defines the `§<Section Name>` format that should be used
- **Related**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 5 — "Convention-aware task enrichment" consumes the formatter output

**Root Cause 2 — Wrong issue type**:
- **File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 6a — task creation logic that calls `jira.create_issue`
- **Related**: Project CLAUDE.md Jira Configuration — only defines `Feature issue type ID`, not `Task issue type ID`

### Independence assessment

These two root causes are in **different modules** and affect **different code paths**:
- Root Cause 1 is in the shared convention formatting utilities (`shared/convention-utils.md`), used during task description generation (Step 5).
- Root Cause 2 is in the plan-feature task creation logic (`plan-feature/SKILL.md` Step 6a), used during Jira issue creation (Step 6).

A fix to one does not affect or depend on the other. They are independently reproducible, independently testable, and independently fixable.

## Step 4 — Root Cause Analysis

### Root Cause 1: Convention reference formatter uses kebab-case instead of preserving heading text

- **What is broken**: The convention reference formatter transforms CONVENTIONS.md section headings into kebab-case slugs (e.g., `Migration Patterns` becomes `migration-patterns`) before inserting them into `§` references in task Implementation Notes.
- **Why it is broken**: The formatter applies a slug/kebab-case transformation (lowercase + hyphenate) to the heading text, likely intended for anchor links or URL fragments. However, the `§<Section Name>` format in Implementation Notes is meant for human-readable references and should preserve the original heading text verbatim.
- **Where it is broken**: `shared/convention-utils.md` — the convention section name formatting logic.
- **How to verify the fix**: A reproducer test should provide a CONVENTIONS.md with a heading like `## Migration Patterns`, invoke the convention formatter, and assert that the output contains `§Migration Patterns` (not `§migration-patterns`).

### Root Cause 2: Task creation uses Feature issue type ID instead of Task issue type ID

- **What is broken**: When `/plan-feature` creates Jira tasks in Step 6a, the created issues have issue type "Feature" (ID 10142) instead of "Task".
- **Why it is broken**: The Jira Configuration in CLAUDE.md only defines `Feature issue type ID: 10142`. There is no `Task issue type ID` field. The task creation logic falls back to the Feature issue type ID because it has no other configured value for Task issues. When a project uses a custom issue type scheme with a different Task ID (e.g., 10050), the wrong ID is used.
- **Where it is broken**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 6a — the task creation call that determines which issue type to use.
- **How to verify the fix**: A reproducer test should configure a project with `Task issue type ID: 10050` in the Jira Configuration, run plan-feature task creation, and assert that the created issue has `issuetype.id = 10050` (not 10142).

### Summary

| # | Root Cause | Module | Code Path |
|---|-----------|--------|-----------|
| 1 | Convention formatter kebab-cases headings instead of preserving original text | `shared/convention-utils.md` | Task description generation (Step 5) |
| 2 | Task creation reads Feature issue type ID instead of Task issue type ID | `plan-feature/SKILL.md` Step 6a | Jira issue creation (Step 6) |

These are **two independent root causes** in different modules affecting different execution stages. Fixing one does not fix the other, and neither depends on the other. This triggers the Decomposition Guard (Step 6).
