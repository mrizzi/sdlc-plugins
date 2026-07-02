# Triage-Bug Investigation: ACME-502

## Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Feature issue type ID**: 10142
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

All required sections present: Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration.

## Step 1 -- Fetch Bug

**Issue**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020) -- matches Bug issue type ID from configuration.
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502

### Parsed Description Sections

**Required Sections** (all present):

- **Issue Description**: Two distinct problems occur when running `/plan-feature`: (1) generated task description has malformed Implementation Notes where convention references use wrong section heading format (kebab-case instead of title case), and (2) task is created with issue type "Feature" instead of "Task" when the project has a custom issue type scheme.
- **Steps to Reproduce**: Configure project with custom issue type scheme (Task ID 10050), add CONVENTIONS.md with section `## Migration Patterns`, run `/plan-feature ACME-200`, observe task output.
- **Expected Result**: Convention references should use title case (`Migration Patterns`); created issue should be type Task (ID 10050).
- **Actual Result**: Convention references use kebab-case (`migration-patterns`); created issue is type Feature (ID 10142) instead of Task.

**Optional Sections**:

- **Suggested Fix**: Present. Reporter suspects two separate bugs: convention reference formatter lowercases/kebab-cases headings incorrectly, and task creation logic reads Feature issue type ID instead of Task issue type ID.

## Step 2 -- Reproduce/Trace

This bug involves skill/documentation behavior that cannot be directly executed. Code-path tracing was performed instead.

### Trace 1: Convention Reference Formatting

- **Entry point**: `/plan-feature` skill invocation
- **Code path**: When generating Implementation Notes, the skill references CONVENTIONS.md sections. The convention reference formatter in `shared/convention-utils.md` is responsible for transforming section headings into `section-reference` format (e.g., `Migration Patterns`).
- **Divergence point**: The formatter in `shared/convention-utils.md` applies a kebab-case transform to the heading text, producing `migration-patterns` instead of preserving the original title case (`Migration Patterns`). The formatter incorrectly lowercases and hyphenates the heading before prefixing it with the section symbol.

### Trace 2: Task Issue Type Selection

- **Entry point**: `/plan-feature` skill invocation
- **Code path**: When creating a Jira issue in Step 6a of `plan-feature/SKILL.md`, the skill needs to select the correct issue type ID for Task creation.
- **Divergence point**: The task creation logic in `plan-feature/SKILL.md` Step 6a reads the **Feature issue type ID** (10142) from Jira Configuration instead of looking up or using the correct **Task issue type ID** from the project's issue type scheme. This causes the created issue to be of type Feature rather than Task.

## Step 3 -- Codebase Investigation

### Target Repository

The bug affects the **sdlc-workflow** component within the sdlc-plugins repository.

### Affected Files and Modules

#### Root Cause 1: Convention Reference Formatter (Wrong Case Transform)

- **File**: `shared/convention-utils.md`
- **Module**: Convention reference formatter / section-reference generator
- **Defect**: The formatter applies a kebab-case transformation (lowercase + hyphenate) to CONVENTIONS.md section headings when generating section references. It should preserve the original title case of the heading as it appears in CONVENTIONS.md.
- **Impact**: All convention references in generated task Implementation Notes are malformed (e.g., `migration-patterns` instead of `Migration Patterns`).

#### Root Cause 2: Task Creation Issue Type (Wrong ID)

- **File**: `plan-feature/SKILL.md` (Step 6a)
- **Module**: Task creation logic in the plan-feature skill
- **Defect**: The task creation step reads the `Feature issue type ID` (10142) from Jira Configuration and uses it when creating Task issues. It should use the Task issue type ID appropriate to the project's issue type scheme.
- **Impact**: Created issues have the wrong issue type (Feature instead of Task), which breaks workflows that filter or process issues by type.

## Step 4 -- Root Cause Analysis

### Root Cause Determination

This bug has **two independent root causes** located in **different modules/code paths**:

#### Root Cause 1: Convention formatter uses wrong case transform

- **What is broken**: The convention reference formatter transforms CONVENTIONS.md section headings into kebab-case when generating section references for Implementation Notes.
- **Why it is broken**: The formatter applies `toLowerCase()` and replaces spaces with hyphens (kebab-case transform) to the heading text. It should instead preserve the original heading text as-is (title case), since convention references should match the actual section heading in CONVENTIONS.md.
- **Where it is broken**: `shared/convention-utils.md` -- the section-reference generation logic.
- **How to verify**: A reproducer test should create a CONVENTIONS.md with a section heading like `## Migration Patterns`, invoke the convention reference formatter, and assert the output is `Migration Patterns` (title case), not `migration-patterns` (kebab-case).

#### Root Cause 2: Task creation uses Feature issue type ID instead of Task issue type ID

- **What is broken**: The task creation logic uses the Feature issue type ID (10142) when creating Task issues in Jira.
- **Why it is broken**: The code in `plan-feature/SKILL.md` Step 6a reads `Feature issue type ID` from Jira Configuration and passes it as the issue type when calling `jira.create_issue`. It should instead use the Task issue type ID, which may come from a different configuration field or the project's issue type scheme.
- **Where it is broken**: `plan-feature/SKILL.md` Step 6a -- the `jira.create_issue` call.
- **How to verify**: A reproducer test should configure a project with a custom issue type scheme where Task has a specific ID (e.g., 10050), invoke `/plan-feature`, and assert the created issue's `issuetype.id` matches the Task ID, not the Feature ID (10142).

### Independence Assessment

These two root causes are **independent**:

- They affect **different modules**: `shared/convention-utils.md` vs `plan-feature/SKILL.md`
- They involve **different code paths**: string formatting logic vs Jira API issue creation
- They can be **fixed independently**: fixing the convention formatter does not affect task creation, and vice versa
- They have **different symptoms**: malformed text output vs wrong Jira issue type
- They require **different reproducer tests**: one tests string output formatting, the other tests Jira API call parameters

This triggers the **Decomposition Guard** (Step 6).

### Root Cause Comment (would be posted to ACME-502)

> **Root Cause**: This bug has two independent root causes:
>
> 1. The convention reference formatter in `shared/convention-utils.md` applies a kebab-case transform (lowercase + hyphenate) to section headings instead of preserving the original title case. This causes convention references like `Migration Patterns` to appear as `migration-patterns`.
>
> 2. The task creation logic in `plan-feature/SKILL.md` Step 6a reads the Feature issue type ID (10142) from Jira Configuration instead of using the correct Task issue type ID. This causes created issues to have the wrong issue type.
>
> **Affected Files**:
> - `shared/convention-utils.md` -- convention reference formatter (kebab-case transform)
> - `plan-feature/SKILL.md` Step 6a -- task creation issue type selection
>
> **Suggested Approach**: These should be fixed as two separate changes since they are in independent code paths. Fix 1: update the convention formatter to preserve original heading case. Fix 2: update task creation to use the Task issue type ID instead of Feature issue type ID.
>
> **Reproducer Strategy**:
> - For root cause 1: test that convention references preserve the original heading case from CONVENTIONS.md
> - For root cause 2: test that created issues use the Task issue type ID, not the Feature issue type ID
