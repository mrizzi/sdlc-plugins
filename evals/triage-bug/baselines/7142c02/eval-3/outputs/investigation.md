# Investigation Findings: ACME-502

## Step 0 -- Validate Project Configuration

Configuration validated from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

## Step 1 -- Fetch Bug

**Issue**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020) -- matches Bug Configuration (10020). Validated.
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502

### Parsed Description Sections

All required sections present per bug template:

| Section | Status |
|---------|--------|
| Issue Description | Present |
| Steps to Reproduce | Present |
| Expected Result | Present |
| Actual Result | Present |
| Attachments | Present (None) |

Optional sections:

| Section | Status |
|---------|--------|
| Root Cause | Not present |
| Suggested Fix | Present |

### Extracted Content

**Description**: Two distinct problems occur when running `/plan-feature`: (1) malformed convention references in Implementation Notes using wrong heading format, and (2) task created with wrong issue type "Feature" instead of "Task".

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

**Suggested Fix**: Two separate bugs -- convention reference formatter lowercases and kebab-cases headings; task creation reads Feature issue type ID instead of Task issue type ID.

## Step 2 -- Code-Path Tracing

The bug cannot be directly reproduced (it involves skill/plugin behavior). Tracing through the relevant code paths instead.

### Trace 1: Convention Reference Formatting

Entry point: `/plan-feature` invocation -> Step 5 (Generate Jira Tasks) -> Convention-aware task enrichment.

The convention-aware task enrichment process in `plan-feature/SKILL.md` Step 5 instructs the skill to cross-reference CONVENTIONS.md sections with task scope and produce Implementation Notes lines of the form:

```
Per CONVENTIONS.md §<Section Name>: <specific action required>
```

The `<Section Name>` should preserve the original heading text from CONVENTIONS.md (e.g., `§Migration Patterns`). However, the convention reference formatter in `shared/convention-utils.md` is applying a transformation that lowercases the heading and converts spaces to hyphens (kebab-case), producing `§migration-patterns` instead of `§Migration Patterns`.

**Divergence point**: The convention formatter in `shared/convention-utils.md` applies a `lowercase + kebab-case` transform to section headings when generating the `§` reference. It should instead preserve the original title case of the heading as written in CONVENTIONS.md.

### Trace 2: Task Creation Issue Type

Entry point: `/plan-feature` invocation -> Step 6a (Create Tasks in Jira) -> `jira.create_issue`.

The task creation logic in `plan-feature/SKILL.md` Step 6a creates issues using `jira.create_issue`. The issue type for tasks should be "Task" with the project's Task issue type ID. However, the code reads the **Feature issue type ID** (10142) from the Jira Configuration section of CLAUDE.md instead of using the Task issue type ID (10050) discovered during Step 2.5 (Discover Project Issue Types).

**Divergence point**: In `plan-feature/SKILL.md` Step 6a, the task creation logic reads `Feature issue type ID` from `## Jira Configuration` in CLAUDE.md (which is 10142) instead of using the Task type-to-role mapping (ID 10050, level 0) that should have been established in Step 2.5.

## Step 3 -- Codebase Investigation

### Root Cause 1: Convention Reference Formatter (shared/convention-utils.md)

**Affected file**: `shared/convention-utils.md` (in the sdlc-plugins repository)
**What is broken**: The convention heading formatter applies a `lowercase + kebab-case` transformation to CONVENTIONS.md section headings when generating `§` references for Implementation Notes. This produces references like `§migration-patterns` instead of preserving the original heading text `§Migration Patterns`.
**Why it is broken**: The formatter treats section headings as URL-style anchors (which conventionally use kebab-case) rather than as human-readable cross-references that should match the source document's heading text exactly.

### Root Cause 2: Task Creation Issue Type (plan-feature/SKILL.md Step 6a)

**Affected file**: `plan-feature/SKILL.md` Step 6a (in the sdlc-plugins repository)
**What is broken**: When creating Task issues in Jira, the code uses the Feature issue type ID (10142) from CLAUDE.md's `## Jira Configuration` section instead of the Task issue type ID (10050) from the type-to-role mapping established in Step 2.5.
**Why it is broken**: The task creation logic reads the wrong configuration field. It pulls `Feature issue type ID` from CLAUDE.md's Jira Configuration rather than using the dynamically discovered Task type from Step 2.5's hierarchy role mapping. The CLAUDE.md Jira Configuration only stores the Feature issue type ID -- the Task type ID is supposed to come from the dynamic discovery in Step 2.5.

## Step 4 -- Root Cause Analysis

### Summary

This bug report contains **two independent root causes** affecting **different modules** in **different code paths**:

| # | Root Cause | Affected Module | Code Path |
|---|-----------|-----------------|-----------|
| 1 | Convention reference formatter uses wrong case transform -- lowercases and kebab-cases headings instead of preserving title case | `shared/convention-utils.md` | plan-feature Step 5 -> convention enrichment -> heading formatter |
| 2 | Task creation uses Feature issue type ID (10142) instead of Task issue type ID (10050) -- reads wrong config field | `plan-feature/SKILL.md` Step 6a | plan-feature Step 6a -> create_issue -> issue type selection |

### Independence Assessment

These two root causes are **independent**:

- **Different modules**: Root cause 1 is in `shared/convention-utils.md` (a shared utility), while root cause 2 is in `plan-feature/SKILL.md` Step 6a (plan-feature-specific task creation logic).
- **Different code paths**: Root cause 1 is triggered during convention-aware task enrichment (Step 5), while root cause 2 is triggered during Jira task creation (Step 6a).
- **Different fix scopes**: Fixing root cause 1 requires changing the heading formatter in the shared utility; fixing root cause 2 requires changing how the issue type is selected in the task creation step.
- **No shared dependency**: Neither fix depends on or affects the other. Each can be fixed and verified independently.

This triggers the **Decomposition Guard** (Step 6 of triage-bug).

### Reproducer Strategies

**Root Cause 1**: Create a CONVENTIONS.md with a titled section (e.g., `## Migration Patterns`), run convention enrichment, and assert the generated `§` reference preserves the original title case (`§Migration Patterns`) rather than using kebab-case (`§migration-patterns`).

**Root Cause 2**: Configure a project with a custom issue type scheme where Task has ID 10050, run plan-feature task creation, and assert the created issue uses type ID 10050 (Task) rather than 10142 (Feature).
