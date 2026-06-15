# Triage Outcome for TC-8003

## Decision: Close as Duplicate

TC-8003 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]) should be **closed as Duplicate** of **TC-7999**.

## Rationale

### Version Impact Analysis (Step 2)

The version impact analysis for the 2.2.x stream (the scoped stream for TC-8003) determined:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 0.11.14 | NO | ships fixed version |

The vulnerable range is quinn-proto versions before 0.11.14. Versions 2.2.0 through 2.2.2 ship vulnerable versions (0.11.9 and 0.11.12). Versions 2.2.3 and 2.2.4 ship the fixed version 0.11.14.

### Affects Versions Correction (Step 3)

PSIRT assigned Affects Versions: [RHTPA 2.2.0].

Based on lock file analysis, the correct Affects Versions for this stream scope would be: [RHTPA 2.2.0, RHTPA 2.2.1] (2.2.2 is a retag and typically not listed separately).

However, since TC-8003 is being closed as a duplicate, the Affects Versions correction is not applied to TC-8003. The sibling TC-7999 already carries [RHTPA 2.2.0, RHTPA 2.2.1].

### Duplicate Detection (Step 4)

A JQL search for sibling issues with the CVE-2026-31812 label returned TC-7999:

- **TC-7999** has the same stream suffix `[rhtpa-2.2]` as TC-8003 -- making it a **same-stream sibling**.
- **TC-7999** is already **In Progress**, meaning remediation work has begun.
- **TC-7999** already carries Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1], which correctly covers the affected versions.

Per the triage-security skill Step 4.1: when a same-stream sibling exists and is open or in progress, the current issue should be closed as Duplicate.

### Steps 5-7 Skipped

Since the triage outcome is Duplicate closure, the remaining steps are not applicable:

- **Step 5 (Version Lifecycle Check)**: Not needed -- TC-7999 handles the lifecycle check.
- **Step 6 (Already Fixed Check)**: Not needed -- TC-7999 is In Progress, not resolved.
- **Step 7 (Remediation)**: Not needed -- remediation is tracked under TC-7999.

## Proposed Jira Actions

1. **Add comment** to TC-8003:
   > Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]. Version impact analysis confirms overlap: versions 2.2.0, 2.2.1, and 2.2.2 (retag) ship quinn-proto < 0.11.14 (vulnerable); versions 2.2.3 and 2.2.4 ship 0.11.14 (fixed).

2. **Transition** TC-8003 to Closed with resolution **Duplicate**.

3. **Assign** TC-8003 to current user.

4. **Add label** `ai-cve-triaged` to TC-8003.

## Cross-Stream Note

The 2.1.x stream (rhtpa-release.0.3.z) also ships vulnerable versions of quinn-proto (0.11.9 in both 2.1.0 and 2.1.1). However, this is outside the scope of TC-8003 (which is scoped to [rhtpa-2.2]). PSIRT would manage any 2.1.x tracking separately via a different Vulnerability issue.
