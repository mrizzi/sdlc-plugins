# Validation Result: ACME-501

## Step 0 -- Validate Project Configuration

Configuration validated successfully. Extracted values from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

## Step 1 -- Fetch Bug

### Issue type validation

The issue type ID (10020) matches the Bug issue type ID from Bug Configuration (10020). Validation passed.

### Bug description parsing

The bug description template at `docs/templates/bug-template.md` defines the following **Required Sections**:

| Section | Heading Format | Present in ACME-501? |
|---------|----------------|----------------------|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | **No -- MISSING** |
| Expected Result | `### **Expected Result**` | **No -- MISSING** |
| Actual Result | `### **Actual Result**` | Yes |

The template also lists `### **Attachments**` in the Required Sections table. That heading is present in ACME-501.

**Parsing detail:** The bug description was scanned for each required heading defined in the template. The following headings were found:

1. `### **Issue Description**` -- found. Content: "The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request with a descriptive error message."
2. `### **Steps to Reproduce**` -- **not found.** No heading matching this format exists in the description.
3. `### **Expected Result**` -- **not found.** No heading matching this format exists in the description.
4. `### **Actual Result**` -- found. Content: "HTTP 500 Internal Server Error with a stack trace in the response body."

### Validation outcome: FAILED

Bug ACME-501 is missing **2 required sections** as defined by the template at `docs/templates/bug-template.md`:

1. **Steps to Reproduce** (expected heading: `### **Steps to Reproduce**`)
2. **Expected Result** (expected heading: `### **Expected Result**`)

Per the skill specification (Step 1, "Parse bug description"):

> "If any Required Section is missing from the Bug description, list the missing sections and inform the user ... Stop execution immediately. Do not attempt to investigate an incomplete bug report."

Message to user:

> "Bug ACME-501 is missing required sections: **Steps to Reproduce**, **Expected Result**. The bug description does not follow the template at `docs/templates/bug-template.md`."

## Execution halted after Step 1

Because the bug description failed validation, execution **stops immediately**. The following steps were **not performed**:

- Step 2 (Reproduce/Trace) -- skipped
- Step 3 (Codebase Investigation) -- skipped
- Step 4 (Root Cause Analysis) -- skipped
- Step 5 (Generate Task) -- skipped
- Step 5b (Link Task to Bug) -- skipped
- Step 5c (Post Digest) -- skipped
- Step 6 (Decomposition Guard) -- skipped
- Step 7 (Report Result) -- skipped

No investigation, root cause analysis, or task creation was attempted. The user must update the bug description in ACME-501 to include the missing sections before re-running `/triage-bug ACME-501`.
