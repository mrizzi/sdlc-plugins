# Bug Parsing: ACME-500

## Metadata

- **Issue Key**: ACME-500
- **Summary**: plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Issue Type**: Bug (ID: 10020)
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: 0.9.0
- **Web URL**: https://mock-jira.example.com/browse/ACME-500

## Issue Type Validation

Bug issue type ID from issue: **10020**
Bug issue type ID from Bug Configuration (CLAUDE.md): **10020**

**Result**: Match confirmed. Issue is a valid Bug for triage.

## Template Heading Formats

Parsed from bug template at `docs/templates/bug-template.md`:

### Required Sections

| Section | Heading Format | Present in Bug? |
|---------|----------------|-----------------|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |

### Optional Sections

| Section | Heading Format | Present in Bug? |
|---------|----------------|-----------------|
| Root Cause | `### **Root Cause**` | No |
| Suggested Fix | `### **Suggested Fix**` | No |
| Attachments | `### **Attachments**` | Yes (content: "None.") |

**Validation Result**: All four required sections are present. Bug description follows the template.

## Parsed Sections

### Issue Description

When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

### Steps to Reproduce

1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

### Expected Result

The generated task's Implementation Notes should include:
> Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns.

### Actual Result

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.

### Attachments

None.

## Optional Sections

No optional sections (Root Cause, Suggested Fix) were provided by the reporter.
