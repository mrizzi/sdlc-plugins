# Step 1.7 -- Embargo Check: CVE-2026-31812

## Configuration Check

Embargo policy URL is configured in Security Configuration:
- **Embargo policy URL**: https://example.com/security/embargo-policy

Step 1.7 applies (not skipped).

## Severity Evaluation

| Attribute | Value |
|-----------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Trigger threshold | Critical or Important (CVSS >= 7.0) |
| Threshold met? | **YES** (7.5 >= 7.0) |

The CVSS score of 7.5 classifies this vulnerability as **High** severity, which meets the embargo check threshold of CVSS >= 7.0.

## Warning Gate

Since the severity meets the threshold, the following warning gate is presented to the engineer:

---

> **EMBARGO CHECK -- CVE-2026-31812 (High severity)**
>
> High-severity vulnerabilities may be under embargo.
> Before proceeding, verify with your security team that this CVE
> is cleared for public triage.
>
> Embargo policy: https://example.com/security/embargo-policy
>
> Proceed with triage? (Yes / No)

---

## Gate Behavior

- If the engineer responds **"No"**: Stop execution immediately. Inform the user to check embargo status with their security team before re-running triage. Do not proceed to Step 2 (Version Impact Analysis).
- If the engineer responds **"Yes"**: Proceed to Step 2 (Version Impact Analysis) as normal.

This gate fires before any triage output or Jira mutations, so stopping is safe. No data has been written to Jira at this point.
