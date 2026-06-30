# Step 1.7 -- Embargo Check

## Configuration

- Embargo policy URL: https://example.com/security/embargo-policy (configured in CLAUDE.md Security Configuration)

## Severity Evaluation

- CVE: CVE-2026-31812
- CVSS score: 7.5
- Severity: **High** (Important)
- Embargo threshold: Critical or Important severity (CVSS >= 7.0)
- Result: **CVSS 7.5 >= 7.0 -- threshold met, embargo warning gate triggered**

## Warning Gate

```
WARNING: EMBARGO CHECK -- CVE-2026-31812 (High severity, CVSS 7.5)

High-severity vulnerabilities may be under embargo.
Before proceeding, verify with your security team that this CVE
is cleared for public triage.

Embargo policy: https://example.com/security/embargo-policy

Proceed with triage? (Yes / No)
```

## Resolution

This gate requires the engineer to confirm that CVE-2026-31812 is not under embargo before proceeding to Step 2 (Version Impact Analysis). No Jira mutations occur at this step -- stopping is safe.

- If "Yes": proceed to Step 2.
- If "No": stop execution and advise the engineer to verify embargo status with their security team before re-running triage.
