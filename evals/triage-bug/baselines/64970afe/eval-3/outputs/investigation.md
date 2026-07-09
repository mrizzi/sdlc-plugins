# Investigation: ACME-502

## Bug Summary

**Key**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type

## Template Validation

All 4 required sections are present:
- [x] Issue Description
- [x] Steps to Reproduce
- [x] Expected Result
- [x] Actual Result

Optional sections also present: Attachments, Suggested Fix.

## Investigation Findings

Investigation of the `/plan-feature` skill execution path reveals **two independent root causes** in different modules.

### Root Cause 1: Convention reference formatter uses wrong case transform

- **Affected file**: `shared/convention-utils.md`
- **Problem**: The convention reference formatter lowercases and kebab-cases section headings when generating `§`-prefixed references in Implementation Notes. For a heading `## Migration Patterns`, it produces `§migration-patterns` instead of preserving the original title case as `§Migration Patterns`.
- **Expected behavior**: Convention references should preserve the original heading text exactly as written in `CONVENTIONS.md` (e.g., `§Migration Patterns`).
- **Actual behavior**: Headings are transformed through a lowercase + kebab-case pipeline, producing `§migration-patterns`.

### Root Cause 2: Task creation uses Feature issue type ID instead of Task

- **Affected file**: `plan-feature/SKILL.md` Step 6a
- **Problem**: The task creation logic reads the Feature issue type ID (`10142`) from the project's CLAUDE.md Jira Configuration instead of the Task issue type ID. When the project has a custom issue type scheme (where Task has a different ID, e.g., `10050`), the created issue is incorrectly typed as Feature.
- **Expected behavior**: Tasks created during `/plan-feature` should use the Task issue type ID from the project configuration.
- **Actual behavior**: The code reads `Feature issue type ID: 10142` and uses that value for task creation, ignoring the actual Task issue type ID.

## Independence Assessment

| Dimension | Root Cause 1 | Root Cause 2 |
|-----------|-------------|-------------|
| **Module** | `shared/convention-utils.md` | `plan-feature/SKILL.md` Step 6a |
| **Code path** | Convention formatting / text rendering | Jira issue creation / API call |
| **Symptom** | Malformed `§` references in description | Wrong issue type on created issue |
| **Fix scope** | Change case transform to preserve original heading text | Change config field read from Feature ID to Task ID |
| **Independently fixable** | Yes | Yes |

These two root causes are **fully independent**: they occur in different modules, affect different code paths, produce different symptoms, and can be fixed without any interaction between the changes.
