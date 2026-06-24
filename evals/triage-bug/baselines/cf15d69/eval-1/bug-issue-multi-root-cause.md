<!-- SYNTHETIC TEST DATA — Bug issue whose investigation reveals multiple independent root causes for triage-bug eval testing -->

# Mock Jira Bug Issue (Multi-Root-Cause)

**Key**: ACME-502
**Summary**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020)
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502

---

## Description

### **Issue Description**

Two distinct problems occur when running `/plan-feature`:
1. The generated task description has malformed Implementation Notes — convention
   references use the wrong section heading format (e.g., `§migration-patterns`
   instead of `§Migration Patterns`).
2. The task is created with issue type "Feature" instead of "Task" when the project
   has a custom issue type scheme.

### **Steps to Reproduce**

1. Configure a project with a custom issue type scheme where Task has ID 10050.
2. Add a `CONVENTIONS.md` with section `## Migration Patterns`.
3. Run `/plan-feature ACME-200`.
4. Observe the generated task: check (a) Implementation Notes convention references and (b) the issue type.

### **Expected Result**

- Implementation Notes should reference conventions as `§Migration Patterns` (title case, matching the heading).
- The created issue should be of type Task (ID 10050).

### **Actual Result**

- Implementation Notes reference conventions as `§migration-patterns` (kebab-case, not matching the heading).
- The created issue is of type Feature (ID 10142) instead of Task.

### **Attachments**

None.

### **Suggested Fix**

These are likely two separate bugs:
- The convention reference formatter lowercases and kebab-cases headings incorrectly.
- The task creation logic reads Feature issue type ID instead of Task issue type ID from configuration.
