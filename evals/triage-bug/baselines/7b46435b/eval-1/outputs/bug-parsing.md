# Bug Parsing: ACME-500

## Configuration Validation

| Configuration Item | Expected | Found | Status |
|---|---|---|---|
| Repository Registry | Present | Present (acme-backend) | OK |
| Jira Configuration | Present | Present (Project key: ACME) | OK |
| Code Intelligence | Present | Present (no Serena configured) | OK |
| Bug Configuration | Present | Present | OK |
| Bug issue type ID | 10020 | 10020 (matches issue ACME-500 type ID) | OK |
| Bug template path | — | docs/templates/bug-template.md | OK |
| Bug-to-Task link type | — | Blocks | OK |

The bug issue ACME-500 has issue type `Bug (ID: 10020)`, which matches the Bug Configuration's `Bug issue type ID: 10020`. Validation passed.

## Required Sections

| Section | Heading Format | Found |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Attachments | `### **Attachments**` | Yes |

All required sections are present.

## Optional Sections

| Section | Heading Format | Found |
|---|---|---|
| Root Cause | `### **Root Cause**` | No |
| Suggested Fix | `### **Suggested Fix**` | No |

## Extracted Content

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
> Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.

### Actual Result

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.

### Attachments

None.
