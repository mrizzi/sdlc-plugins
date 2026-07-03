# Investigation: ACME-502

**Bug**: Skill output is malformed and task creation uses wrong issue type
**Status**: New
**Component**: sdlc-workflow

## Step 1 - Bug Parsing

Issue type Bug (ID: 10020) matches configured Bug issue type ID. All required sections present (Issue Description, Steps to Reproduce, Expected Result, Actual Result, Attachments) plus optional Suggested Fix section.

Two distinct symptoms reported:
1. Convention references in Implementation Notes use kebab-case (`§migration-patterns`) instead of preserving original heading case (`§Migration Patterns`).
2. Task issues are created with type Feature (ID 10142) instead of Task when the project has a custom issue type scheme.

## Step 2 - Reproduce/Trace

### Trace 1: Convention Reference Formatting

The convention reference formatter in `shared/convention-utils.md` takes a heading like "Migration Patterns" and transforms it to kebab-case (`migration-patterns`) before building the `§` reference. The expected output should preserve the original title case (`§Migration Patterns`), matching the CONVENTIONS.md heading exactly.

- Input: heading `## Migration Patterns` from CONVENTIONS.md
- Current behavior: transforms to `§migration-patterns`
- Expected behavior: preserves as `§Migration Patterns`

### Trace 2: Issue Type Selection

The task creation logic in `plan-feature/SKILL.md Step 6a` reads the Feature issue type ID (10142) from Jira Configuration instead of the Task issue type ID. When the project has a custom issue type scheme with Task ID 10050, the wrong ID is used, creating a Feature instead of a Task.

- Configuration read: Feature issue type ID (10142) from `## Jira Configuration`
- Should read: Task issue type ID (10050) from the project's custom issue type scheme
- Result: issues created as Feature instead of Task

## Step 3 - Codebase Investigation

### Finding 1: Convention Reference Formatter (`shared/convention-utils.md`)

The convention reference utility applies a kebab-case transform to section headings when generating `§` references. This lowercases all characters and replaces spaces with hyphens. The transform should instead preserve the original heading text exactly as written in CONVENTIONS.md.

- **Affected module**: `shared/convention-utils.md`
- **Affected code path**: Convention reference formatting / `§` reference generation
- **Symptom**: Produces `§migration-patterns` instead of `§Migration Patterns`

### Finding 2: Task Creation Issue Type (`plan-feature/SKILL.md Step 6a`)

The task creation step reads the Feature issue type ID (10142) from the Jira Configuration block instead of the Task issue type ID. This causes all created tasks to have the wrong issue type when the project uses a custom issue type scheme where Task and Feature have different IDs.

- **Affected module**: `plan-feature/SKILL.md Step 6a`
- **Affected code path**: Jira issue creation / issue type selection
- **Symptom**: Creates Feature issues (ID 10142) instead of Task issues (ID 10050)

## Step 4 - Root Cause Analysis

### Root Cause 1: Convention reference formatter uses wrong case transform

**Location**: `shared/convention-utils.md`

The convention reference formatter applies a kebab-case transform (lowercase + hyphen-separated) to headings when generating `§` references. It should preserve the original heading case from CONVENTIONS.md. This produces references like `§migration-patterns` instead of the correct `§Migration Patterns`.

### Root Cause 2: Task creation reads wrong issue type ID from configuration

**Location**: `plan-feature/SKILL.md Step 6a`

The task creation logic reads the Feature issue type ID (10142) from the Jira Configuration section instead of the Task issue type ID. When the project has a custom issue type scheme where Task has a distinct ID (10050), the created issue gets the wrong type (Feature instead of Task).

### Independence Assessment

These two root causes are **independent**:

- **Different modules**: Root Cause 1 is in `shared/convention-utils.md`; Root Cause 2 is in `plan-feature/SKILL.md Step 6a`.
- **Different code paths**: Root Cause 1 affects convention reference formatting (string transformation of headings); Root Cause 2 affects Jira issue creation (issue type ID selection from configuration).
- **Can be fixed independently**: Fixing the case transform in `shared/convention-utils.md` has no effect on the issue type selection in `plan-feature/SKILL.md`, and vice versa. Neither fix depends on the other.
- **Different domains**: One is a text formatting concern; the other is a Jira API integration concern.

This independence triggers the **Decomposition Guard** (Step 6). The skill pauses to ask the user whether to proceed with a single combined Task or split into separate Bug issues.
