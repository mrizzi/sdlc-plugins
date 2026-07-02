# Step 1.7 -- Embargo Check

## Configuration

Embargo policy URL is configured in Security Configuration:
**https://example.com/security/embargo-policy**

Since the Embargo policy URL is present, this step is active (not skipped).

## Severity Evaluation

| Attribute | Value |
|-----------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Threshold | CVSS >= 7.0 (Critical or Important) |
| Meets threshold? | **YES** (7.5 >= 7.0) |

The CVSS score of 7.5 classifies this vulnerability as **High** severity, which meets the embargo check threshold of CVSS >= 7.0.

## Warning Gate

The following warning gate is presented to the engineer:

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

- If the engineer responds **"No"**: execution stops immediately. The engineer must check embargo status with their security team before re-running triage. No Jira mutations occur, and no triage output is produced.
- If the engineer responds **"Yes"**: triage proceeds to Step 2 (Version Impact Analysis) as normal.

This gate is consistent with the existing guardrail pattern -- every Jira mutation requires confirmation. No Jira mutations occur at this step, so stopping is safe. The gate fires before any triage output.
