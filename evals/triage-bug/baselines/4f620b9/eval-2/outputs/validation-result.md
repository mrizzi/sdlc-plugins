# Validation Result: ACME-501 — Bug Description Parsing (Step 1)

## Outcome

**Execution stopped at Step 1 with a validation error.** The bug description is missing required sections and does not conform to the bug template.

## Step 0 — Configuration Validation (passed)

The project CLAUDE.md (`claude-md-bug-config.md`) contains valid Bug Configuration:

- **Bug issue type ID**: 10020
- **Bug template path**: `docs/templates/bug-template.md`
- **Bug-to-Task link type**: Blocks

## Step 1 — Fetch Bug and Parse Description

### Issue type validation (passed)

Issue ACME-501 has issue type Bug with ID 10020, which matches the Bug issue type ID from Bug Configuration. Validation passed.

### Bug description parsing

The bug template (`bug-template-mock.md`) defines the following required and optional sections:

**Required Sections (from template):**

| Section | Heading Format |
|---------|----------------|
| Description | `### **Issue Description**` |
| Steps to reproduce | `### **Steps to Reproduce**` |
| Expected Result | `### **Expected Result**` |
| Actual Result | `### **Actual Result**` |

**Optional Sections (from template):**

| Section | Heading Format |
|---------|----------------|
| Root Cause | `### **Root Cause**` |
| Suggested Fix | `### **Suggested Fix**` |

### Sections found in ACME-501 description

The bug description was parsed by matching headings against the template's heading formats. The following sections were **found**:

1. **Issue Description** (`### **Issue Description**`) — Present. Content: "The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request with a descriptive error message."
2. **Actual Result** (`### **Actual Result**`) — Present. Content: "HTTP 500 Internal Server Error with a stack trace in the response body."
3. **Attachments** (`### **Attachments**`) — Present. Content: "None."

### Sections missing from ACME-501 description

The following **required sections** are missing from the bug description:

1. **Steps to Reproduce** (`### **Steps to Reproduce**`) — Not found. No heading matching `### **Steps to Reproduce**` exists in the description.
2. **Expected Result** (`### **Expected Result**`) — Not found. No heading matching `### **Expected Result**` exists in the description.

### Optional sections

Neither optional section (Root Cause, Suggested Fix) was present in the description. This is acceptable since they are optional.

## Why Execution Stopped

Per the triage-bug skill specification (Step 1, "Parse bug description"):

> "If any Required Section is missing from the Bug description, list the missing sections and inform the user... Stop execution immediately. Do not attempt to investigate an incomplete bug report."

Two of the four required sections — **Steps to Reproduce** and **Expected Result** — are absent from the ACME-501 bug description. The description does not follow the template at `docs/templates/bug-template.md`.

**Validation error message:**

> Bug ACME-501 is missing required sections: Steps to Reproduce, Expected Result. The bug description does not follow the template at `docs/templates/bug-template.md`.

Steps 2 through 7 were not executed.
