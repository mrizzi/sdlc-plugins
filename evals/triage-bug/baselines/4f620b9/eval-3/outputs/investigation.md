# Investigation Report: ACME-502

## Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks
- **Feature issue type ID**: 10142

All required sections present: Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration.

## Step 1 -- Fetch Bug

**Issue key**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue type ID**: 10020 (Bug) -- matches Bug Configuration, validated.
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502

### Parsed Description Sections

**Required Sections** (all present):

- **Description**: Two distinct problems occur when running `/plan-feature`: (1) generated task description has malformed Implementation Notes where convention references use wrong section heading format (e.g., `§migration-patterns` instead of `§Migration Patterns`), and (2) the task is created with issue type "Feature" instead of "Task" when the project has a custom issue type scheme.
- **Steps to Reproduce**: Configure a project with custom issue type scheme (Task ID 10050), add CONVENTIONS.md with section `## Migration Patterns`, run `/plan-feature ACME-200`, observe the generated task for convention references and issue type.
- **Expected Result**: Convention references should use `§Migration Patterns` (title case, matching the heading). Created issue should be type Task (ID 10050).
- **Actual Result**: Convention references use `§migration-patterns` (kebab-case). Created issue is type Feature (ID 10142) instead of Task.

**Optional Sections**:

- **Suggested Fix**: Present. Two separate bugs suspected: convention reference formatter applies wrong case transform; task creation logic reads Feature issue type ID instead of Task.

## Step 2 -- Code-Path Tracing

This is a skill/documentation bug that cannot be directly reproduced via commands. Code-path tracing was performed.

### Trace 1: Convention reference formatting

Entry point: `/plan-feature` invocation -> Step 5 (Generate Jira Tasks) -> Convention-aware task enrichment.

The convention-aware task enrichment in plan-feature/SKILL.md Step 5 instructs the agent to cross-reference CONVENTIONS.md sections and include references in Implementation Notes using the format:

```
Per CONVENTIONS.md §<Section Name>: <specific action required>
```

The `<Section Name>` should preserve the original heading text from CONVENTIONS.md (e.g., `Migration Patterns`). However, the convention reference formatter in `shared/convention-applicability-rules.md` (and the corresponding utility logic in `shared/convention-utils.md`) applies a kebab-case transform to the section name, producing `§migration-patterns` instead of `§Migration Patterns`.

**Divergence point**: The convention formatter transforms heading text to kebab-case (URL-slug style) rather than preserving the original title-case heading text. This is the wrong transform for the `§<Section Name>` reference format, which expects the human-readable heading.

### Trace 2: Task creation issue type

Entry point: `/plan-feature` invocation -> Step 6a (Create Tasks in Jira) -> `jira.create_issue`.

The task creation logic in plan-feature/SKILL.md Step 6a calls `jira.create_issue` to create Task issues. The issue type should be "Task", but the logic reads the **Feature issue type ID** (10142) from the Jira Configuration instead of using the Task issue type. When the project has a custom issue type scheme where Task has a different ID (e.g., 10050), the created issue ends up as a Feature instead of a Task.

**Divergence point**: Step 6a does not explicitly resolve the Task issue type ID from configuration. It falls back to the Feature issue type ID (10142) from Jira Configuration, which is the only issue type ID configured there. The Task issue type ID is not present in the Jira Configuration section, causing the logic to use the wrong ID.

## Step 3 -- Codebase Investigation

### Target repository

Based on the Component field (sdlc-workflow) and the code paths referenced, the bug affects the sdlc-plugins repository itself, specifically the plugin skill definitions.

No Serena instance is available for this repository (per Code Intelligence section). Investigation performed using Read, Grep, and Glob fallback.

### Affected files and modules

**Root Cause 1 -- Convention reference formatting:**

- **File**: `shared/convention-utils.md` (shared utility module for convention handling)
- **Related file**: `shared/convention-applicability-rules.md` (defines the `§<Section Name>` format)
- **Related file**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 5 (convention-aware task enrichment)
- **Symptom**: Convention section names are kebab-cased (`§migration-patterns`) instead of preserving original heading case (`§Migration Patterns`)
- **Fix location**: The case transform function in `shared/convention-utils.md` that converts heading text to reference format

**Root Cause 2 -- Wrong issue type in task creation:**

- **File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 6a (task creation)
- **Related file**: Project CLAUDE.md Jira Configuration section
- **Symptom**: Tasks created with Feature issue type ID (10142) instead of Task issue type
- **Fix location**: Step 6a's issue type resolution logic, which should use `--issue-type Task` (the REST fallback already does this correctly) or resolve the Task issue type ID from configuration rather than defaulting to the Feature issue type ID

## Step 4 -- Root Cause Analysis

### Root Cause 1: Convention reference formatter uses wrong case transform

**What is broken**: The convention reference formatter in `shared/convention-utils.md` applies a kebab-case transformation to CONVENTIONS.md section headings when generating `§<Section Name>` references in task Implementation Notes.

**Why it is broken**: The formatter treats section names like URL slugs (lowercased, hyphenated) rather than preserving the original heading text. The `§<Section Name>` format specified in `shared/convention-applicability-rules.md` and `plan-feature/SKILL.md` Step 5 expects the human-readable heading (e.g., `§Migration Patterns`), not a slug (e.g., `§migration-patterns`).

**Where it is broken**: `shared/convention-utils.md` -- the case transform function applied to convention section names.

**How to verify the fix**: A reproducer test should:
1. Provide a CONVENTIONS.md with a heading `## Migration Patterns`
2. Run the convention reference formatter
3. Assert the output contains `§Migration Patterns` (title case), not `§migration-patterns` (kebab-case)

### Root Cause 2: Task creation uses Feature issue type ID instead of Task

**What is broken**: The task creation logic in `plan-feature/SKILL.md` Step 6a creates issues using the Feature issue type ID (10142) from Jira Configuration, even though it intends to create Task issues.

**Why it is broken**: The Jira Configuration section only defines `Feature issue type ID: 10142`. There is no `Task issue type ID` field configured. When the skill creates tasks, it defaults to the only available issue type ID (Feature), resulting in issues of the wrong type. Projects with custom issue type schemes have distinct IDs for Feature and Task, so using the Feature ID creates Feature issues instead of Tasks.

**Where it is broken**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` Step 6a -- the issue type resolution when calling `jira.create_issue`.

**How to verify the fix**: A reproducer test should:
1. Configure a project with a custom issue type scheme (Task ID = 10050, Feature ID = 10142)
2. Run `/plan-feature` to generate and create tasks
3. Assert the created issues have issue type ID 10050 (Task), not 10142 (Feature)

## Independence Assessment

These two root causes are **independent**:

1. **Different modules**: Root Cause 1 is in the shared convention formatting utilities (`shared/convention-utils.md`). Root Cause 2 is in the plan-feature task creation logic (`plan-feature/SKILL.md` Step 6a).
2. **Different code paths**: The convention formatter runs during Step 5 (task description generation). The issue type resolution runs during Step 6a (Jira API call).
3. **No shared state**: Fixing one does not affect the other. The convention formatting bug could exist without the issue type bug, and vice versa.
4. **Different fix approaches**: Root Cause 1 requires changing a string transformation function. Root Cause 2 requires changing how the issue type ID is resolved from configuration.

This triggers the **Decomposition Guard** (Step 6) -- the bug involves multiple independent issues in different modules that should not be silently bundled into a single Task.
