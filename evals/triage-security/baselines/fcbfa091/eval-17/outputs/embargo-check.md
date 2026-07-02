# Step 1.7 -- Embargo Check

## Configuration

Embargo policy URL is configured in Security Configuration:
- **Embargo policy URL**: https://example.com/security/embargo-policy

Because this field is present, Step 1.7 is **active** (not skipped).

## Severity Evaluation

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Embargo threshold | CVSS >= 7.0 (Critical or Important) |
| Threshold met? | **Yes** -- 7.5 >= 7.0 |

The CVSS score of 7.5 (High severity) meets the embargo trigger threshold of >= 7.0.
This triggers the embargo warning gate.

For reference, this gate is NOT triggered for Low or Moderate severity vulnerabilities
(CVSS < 7.0). Only Critical (CVSS >= 9.0) and Important/High (CVSS >= 7.0) severities
activate the embargo check.

## Warning Gate (PROPOSAL)

The following warning is presented to the engineer for confirmation before proceeding:

---

> **EMBARGO CHECK -- CVE-2026-31812 (High severity)**
>
> High-severity vulnerabilities may be under embargo.
> Before proceeding, verify with your security team that this CVE
> is cleared for public triage.
>
> Embargo policy: https://example.com/security/embargo-policy
>
> **Proceed with triage? (Yes / No)**

---

## Decision Points

- **If "Yes"**: Proceed to Step 2 (Version Impact Analysis) as normal.
- **If "No"**: Stop execution immediately. The engineer should check embargo status
  with their security team before re-running triage. No Jira mutations or further
  analysis will occur.

## Rationale

This gate is consistent with the existing guardrail pattern where every Jira mutation
requires confirmation. No Jira mutations occur at this step -- the gate fires before
any triage output, so stopping is safe. The embargo check is advisory only; it does
not enforce embargo procedures but surfaces a warning and links to the organization's
embargo policy for the engineer to verify.
