# Triage Bug - Step 1: Bug Description Validation

**Issue**: ACME-501 — API returns 500 on malformed input

## Bug Template Reference

Bug template path (from Bug Configuration): `docs/templates/bug-template.md`

## Required Sections Check

The bug template defines five required sections. Each section was checked against the bug description using the heading formats specified in the template.

| Required Section | Heading Format | Present |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to reproduce | `### **Steps to Reproduce**` | **No -- MISSING** |
| Expected Result | `### **Expected Result**` | **No -- MISSING** |
| Actual Result | `### **Actual Result**` | Yes |
| Attachments | `### **Attachments**` | Yes |

## Sections Found

1. **Issue Description** -- Present. Contains a description of the API gateway returning HTTP 500 on malformed JSON payloads.
2. **Actual Result** -- Present. States "HTTP 500 Internal Server Error with a stack trace in the response body."
3. **Attachments** -- Present. States "None."

## Missing Required Sections

1. **Steps to Reproduce** (`### **Steps to Reproduce**`) -- This section is entirely absent from the bug description. There are no reproduction steps provided.
2. **Expected Result** (`### **Expected Result**`) -- This section is entirely absent from the bug description. The expected behavior is not documented.

## Result

**VALIDATION FAILED** -- 2 of 5 required sections are missing.

Execution stops at Step 1. Steps 2 through 5 (severity/priority assessment, task decomposition, effort estimation, and Jira updates) are not performed.

The reporter must update ACME-501 to include the missing sections per the bug template (`docs/templates/bug-template.md`) before triage can proceed.
