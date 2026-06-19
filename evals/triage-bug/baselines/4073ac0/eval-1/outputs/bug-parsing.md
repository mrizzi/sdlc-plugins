# Bug Parsing — ACME-500

## Step 0 — Configuration Validation

The following configuration was extracted from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

## Step 1 — Issue Type Validation

The issue's type ID is **10020** (Bug). This matches the **Bug issue type ID** (10020) from Bug Configuration. Validation passed.

## Step 1 — Bug Description Template Heading Formats

From the bug template at `docs/templates/bug-template.md`, the required section heading formats are:

| Section | Heading Format |
|---------|----------------|
| Description | `### **Issue Description**` |
| Steps to Reproduce | `### **Steps to Reproduce**` |
| Expected Result | `### **Expected Result**` |
| Actual Result | `### **Actual Result**` |

Optional sections:

| Section | Heading Format |
|---------|----------------|
| Root Cause | `### **Root Cause**` |
| Suggested Fix | `### **Suggested Fix**` |

## Step 1 — Parsed Description Sections

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
> Per CONVENTIONS.md "Migration Patterns: add `Index::create()` for all FK columns.

### **Actual Result**

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.

## Step 1 — Optional Sections

- **Root Cause**: Not provided
- **Suggested Fix**: Not provided

## Step 1 — Metadata

- **Issue key**: ACME-500
- **Web URL**: https://mock-jira.example.com/browse/ACME-500
- **Summary**: plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: 0.9.0

## Validation Result

All four required sections (Description, Steps to Reproduce, Expected Result, Actual Result) are present. The bug description follows the template. Proceeding with investigation.
