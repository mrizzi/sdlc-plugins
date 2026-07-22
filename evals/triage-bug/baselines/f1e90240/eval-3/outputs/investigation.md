# Investigation: ACME-502

**Bug Summary**: Skill output is malformed and task creation uses wrong issue type

## Validation

- **Issue type ID**: 10020 (Bug) -- matches Bug Configuration (10020)
- **Template compliance**: All required sections present (Issue Description, Steps to Reproduce, Expected Result, Actual Result, Attachments)

## Root Cause Analysis

Investigation reveals **two independent root causes** located in different modules with separate code paths.

---

### Root Cause 1: Malformed convention references

**Affected file/module**: `shared/convention-utils.md` (convention reference formatter)

**Problem**: The convention reference formatter applies a kebab-case transform to section headings when generating convention references. For example, a `CONVENTIONS.md` heading `## Migration Patterns` is converted to `§migration-patterns` instead of preserving the original title case as `§Migration Patterns`.

**Expected behavior**: Convention references should preserve the original heading case exactly as written in the source document (e.g., `§Migration Patterns`).

**Actual behavior**: The formatter lowercases the heading and inserts hyphens between words, producing kebab-case references (e.g., `§migration-patterns`).

---

### Root Cause 2: Wrong issue type used for task creation

**Affected file/module**: `plan-feature/SKILL.md` Step 6a (task creation logic)

**Problem**: The task creation logic reads the Feature issue type ID (10142) from the project's Jira Configuration instead of the Task issue type ID. This causes newly created issues to be of type "Feature" instead of "Task" when the project has a custom issue type scheme.

**Expected behavior**: Created issues should use the Task issue type ID (e.g., 10050 as configured in the project's custom issue type scheme).

**Actual behavior**: Created issues use the Feature issue type ID (10142) from the Jira Configuration block, resulting in issues of type "Feature" instead of "Task".

---

## Independence Assessment

These two root causes are **independent** for the following reasons:

1. **Different modules**: Root Cause 1 is in `shared/convention-utils.md` (a shared utility for formatting convention references), while Root Cause 2 is in `plan-feature/SKILL.md` Step 6a (the task creation workflow logic).
2. **Different code paths**: The convention reference formatting happens during task description generation (text formatting), while the issue type selection happens during Jira API call construction (issue creation). These are separate phases of the `/plan-feature` workflow.
3. **Independent fixes**: Fixing the case transform in the convention formatter has no effect on which issue type ID is used for task creation, and vice versa. Each can be fixed and tested independently.
