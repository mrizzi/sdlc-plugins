# Step 1.7 -- Embargo Check

## Configuration

- **Embargo policy URL**: https://example.com/security/embargo-policy
- The Embargo policy URL is **configured** in Security Configuration (extracted in Step 0
  as an optional field, backward compatible -- no error raised if absent).
- Because the URL is present, Step 1.7 is **active** and will evaluate the CVE severity
  against the embargo threshold.

## Severity Evaluation

| Parameter | Value |
|-----------|-------|
| CVE ID | CVE-2026-31812 |
| CVSS Score | 7.5 |
| Severity | High |
| Trigger threshold | CVSS >= 7.0 (Critical or Important) |
| Threshold met? | **Yes** -- 7.5 >= 7.0 |

The vulnerability severity (High, CVSS 7.5) meets the embargo check threshold
(Critical or Important, CVSS >= 7.0). The warning gate is triggered and must be
presented to the engineer before proceeding to Step 2.

Note: For Low or Moderate severity CVEs (CVSS < 7.0), this step would be skipped
silently and triage would proceed directly to Step 2 without any warning or prompt.

## Warning Gate

The following confirmation prompt is presented to the engineer:

```
EMBARGO CHECK -- CVE-2026-31812 (High severity)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Gate Behavior

This is a **confirmation prompt** -- not an informational message. The engineer must
explicitly answer Yes or No before triage proceeds.

- If the engineer answers **Yes**: Proceed to Step 2 (Version Impact Analysis) as normal.
- If the engineer answers **No**: Stop execution immediately. Inform the user to check
  embargo status with their security team before re-running triage. Do not proceed to
  Step 2 or perform any further triage actions.

This gate fires before any triage output or Jira mutations beyond the Step 0.7 assignment,
so stopping is safe. No version impact analysis, Affects Versions corrections, or
remediation tasks have been created at this point.

## Consistency

This gate is consistent with the existing guardrail pattern: every Jira mutation requires
confirmation. The embargo check extends this principle to the triage workflow itself --
high-severity CVEs require an additional confirmation that the CVE is cleared for triage
before any analysis output is generated.
