# Triage Outcome -- TC-8003

## Decision: Close as Duplicate

TC-8003 should be **closed as Duplicate** of **TC-7999**.

## Rationale

TC-8003 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]) is a same-stream duplicate of TC-7999:

1. **Same CVE**: Both issues track CVE-2026-31812 (quinn-proto panic on large stream counts).
2. **Same stream**: Both issues carry the stream suffix `[rhtpa-2.2]`, scoping them to the 2.2.x version stream.
3. **TC-7999 is already In Progress**: Triage and remediation work has already begun on TC-7999.
4. **TC-7999 has broader coverage**: TC-7999 has Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1], while TC-8003 only lists [RHTPA 2.2.0]. The existing issue already covers the wider set of affected versions.

Per Step 4.1 of the triage-security skill, when a same-stream sibling exists and is open or in progress, the current issue is closed as Duplicate.

## Version Impact Summary

The version impact analysis confirmed that quinn-proto versions before 0.11.14 are vulnerable:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | fixed version |
| 2.2.4 | 0.11.14 | NO | fixed version |

This analysis is consistent with TC-7999's Affects Versions, confirming RHTPA 2.2.0 and 2.2.1 are correctly identified as affected.

## Proposed Jira Mutations (require engineer confirmation)

1. **Add comment to TC-8003**:
   > Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. Version impact analysis confirms overlap. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1].
   >
   > Version impact analysis:
   > - RHTPA 2.2.0: quinn-proto 0.11.9 (affected)
   > - RHTPA 2.2.1: quinn-proto 0.11.12 (affected)
   > - RHTPA 2.2.2: retag of 2.2.1 (affected)
   > - RHTPA 2.2.3: quinn-proto 0.11.14 (not affected -- fixed version)
   > - RHTPA 2.2.4: quinn-proto 0.11.14 (not affected -- fixed version)

2. **Transition TC-8003** to Closed with resolution **Duplicate**.

3. **Assign TC-8003** to current user.

4. **Add label** `ai-cve-triaged` to TC-8003.

## What Is NOT Done

- No remediation tasks are created for TC-8003 (TC-7999 owns remediation).
- No Affects Versions correction is applied to TC-8003 (it will be closed).
- No cross-stream impact comment is posted (duplicate closure takes precedence).
- Steps 5 through 8 are skipped entirely due to the duplicate finding.

## Note on TC-7999 Affects Versions

TC-7999 lists Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]. Based on the version impact analysis, RHTPA 2.2.2 (retag of 2.2.1) is also affected. If TC-7999's Affects Versions have not been corrected to include 2.2.2, that correction should be addressed during TC-7999's triage, not through TC-8003.
