# Step 1.7 -- Embargo Check: CVE-2026-31812

## Configuration Check

Embargo policy URL is configured in Security Configuration:
- **Embargo policy URL**: https://example.com/security/embargo-policy

Embargo check is **active** (URL configured -- proceeding with severity evaluation).

## Severity Evaluation

| Source | Severity | CVSS Score |
|--------|----------|------------|
| Jira description (Step 1) | High | 7.5 |

Trigger threshold: Critical or Important severity (CVSS >= 7.0)

CVE-2026-31812 has CVSS **7.5**, which is **High** severity. This **meets** the threshold (7.5 >= 7.0).

Result: **Threshold met** -- embargo warning gate must be presented.

## Warning Gate

The following warning is presented to the engineer before proceeding to Step 2:

```
EMBARGO CHECK -- CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Gate Behavior

- If the engineer answers **"Yes"**: proceed to Step 2 (Version Impact Analysis)
- If the engineer answers **"No"**: stop execution and inform the user to check embargo status before re-running triage. Do not proceed to Step 2.

This gate is consistent with the existing guardrail pattern (every Jira mutation requires confirmation). No Jira mutations occur at this step -- the gate fires before any triage output, so stopping is safe.
