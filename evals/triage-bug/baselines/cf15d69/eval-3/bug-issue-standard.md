<!-- SYNTHETIC TEST DATA — standard Bug issue with all required sections for triage-bug eval testing -->

# Mock Jira Bug Issue

**Key**: ACME-500
**Summary**: plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
**Issue Type**: Bug (ID: 10020)
**Status**: New
**Labels**: reported-by-user
**Component**: sdlc-workflow
**Affects Version/s**: 0.9.0
**Web URL**: https://mock-jira.example.com/browse/ACME-500

---

## Description

### **Issue Description**

When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

### **Steps to Reproduce**

1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

### **Expected Result**

The generated task's Implementation Notes should include:
> Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns.

### **Actual Result**

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown — the convention is silently dropped.

### **Attachments**

None.
