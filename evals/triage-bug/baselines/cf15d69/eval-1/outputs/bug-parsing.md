# Bug Parsing - ACME-500

## Step 0: Configuration Validation

- **Project key**: ACME (from CLAUDE.md Jira Configuration)
- **Bug issue type ID**: 10020 (from CLAUDE.md Bug Configuration)
- **Issue type on ACME-500**: Bug (ID: 10020) -- matches Bug Configuration
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

Configuration is valid. Issue type ID 10020 on the bug matches the configured Bug issue type ID 10020.

## Step 1: Parsed Description Sections

Sections extracted using heading formats from the bug template:

### Issue Description
(Heading format: `### **Issue Description**`)

When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

### Steps to Reproduce
(Heading format: `### **Steps to Reproduce**`)

1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

### Expected Result
(Heading format: `### **Expected Result**`)

The generated task's Implementation Notes should include:
> Per CONVENTIONS.md Migration Patterns: add `Index::create()` for all FK columns.

### Actual Result
(Heading format: `### **Actual Result**`)

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown -- the convention is silently dropped.

### Attachments
(Heading format: `### **Attachments**`)

None.

## Parsing Summary

All 4 required sections successfully extracted:
- [x] Issue Description
- [x] Steps to Reproduce
- [x] Expected Result
- [x] Actual Result

Optional section extracted:
- [x] Attachments (empty)
