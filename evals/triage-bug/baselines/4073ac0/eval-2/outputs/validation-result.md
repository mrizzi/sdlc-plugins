# Triage Bug — ACME-501 — Validation Result

## Step 0 — Validate Project Configuration

Configuration validated successfully from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

## Step 1 — Fetch Bug

### Issue metadata

| Field | Value |
|-------|-------|
| Key | ACME-501 |
| Summary | API returns 500 on malformed input |
| Issue Type | Bug (ID: 10020) |
| Status | New |
| Labels | production-incident |
| Component | api-gateway |
| Web URL | https://mock-jira.example.com/browse/ACME-501 |

### Issue type validation

Issue type ID `10020` matches Bug issue type ID from Bug Configuration (`10020`). Validation passed.

### Parse bug description

The bug description template at **docs/templates/bug-template.md** defines the following required sections:

| Section | Heading Format | Required |
|---------|----------------|----------|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Attachments | `### **Attachments**` | Yes |

**Parsed sections from ACME-501 description:**

| Required Section | Heading | Status |
|------------------|---------|--------|
| Description | `### **Issue Description**` | FOUND |
| Steps to Reproduce | `### **Steps to Reproduce**` | **MISSING** |
| Expected Result | `### **Expected Result**` | **MISSING** |
| Actual Result | `### **Actual Result**` | FOUND |
| Attachments | `### **Attachments**` | FOUND |

**Found sections:**

- **Issue Description**: "The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request with a descriptive error message."
- **Actual Result**: "HTTP 500 Internal Server Error with a stack trace in the response body."

**Missing sections:**

- `### **Steps to Reproduce**` — not present in the bug description
- `### **Expected Result**` — not present in the bug description

### Validation Error

> Bug ACME-501 is missing required sections: **Steps to Reproduce**, **Expected Result**. The bug description does not follow the template at `docs/templates/bug-template.md`.

## Execution Stopped

Execution stopped at **Step 1 — Parse bug description** because required sections are missing from the bug description. Per the triage-bug skill specification:

> "If any Required Section is missing from the Bug description, list the missing sections and inform the user. Stop execution immediately. Do not attempt to investigate an incomplete bug report."

**Steps 2 through 7 were NOT executed.** No investigation, no root cause analysis, no task creation, and no Jira modifications were performed.

The reporter should update ACME-501 to include the missing `### **Steps to Reproduce**` and `### **Expected Result**` sections following the template at `docs/templates/bug-template.md`, then re-run `/triage-bug ACME-501`.
