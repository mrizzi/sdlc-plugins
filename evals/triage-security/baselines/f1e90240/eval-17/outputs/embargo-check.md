# Step 1.7 -- Embargo Check

## Configuration

- Embargo policy URL: https://example.com/security/embargo-policy
- Embargo policy URL is **configured** in Security Configuration -- Step 1.7 applies.

## Severity Evaluation

| Criterion | Value |
|-----------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Threshold | CVSS >= 7.0 (Critical or Important) |
| Threshold met? | **YES** -- 7.5 >= 7.0 |

The CVSS score of 7.5 meets the embargo check threshold of >= 7.0. This CVE is classified as High severity, which falls within the Critical/Important range that triggers the embargo warning gate.

## Warning Gate

The following warning gate is presented to the engineer before proceeding:

```
EMBARGO CHECK -- CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Decision Point

- If the engineer answers **Yes**: proceed to Step 2 (Version Impact Analysis).
- If the engineer answers **No**: stop execution. The engineer must verify embargo status with the security team before re-running triage.

No Jira mutations occur at this step -- the gate fires before any triage output, so stopping is safe and consistent with the guardrail pattern (every Jira mutation requires confirmation).
