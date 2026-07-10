# Triage Outcome for TC-8003

## Decision: CLOSE AS DUPLICATE

TC-8003 should be closed as a **Duplicate** of **TC-7999**.

## Rationale

TC-8003 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]) is a same-stream duplicate of TC-7999, which tracks the identical CVE for the identical version stream and is already In Progress.

### Key findings from triage:

1. **Data Extraction (Step 1)**: TC-8003 tracks CVE-2026-31812, affecting quinn-proto versions before 0.11.14 (fixed in 0.11.14). The issue is scoped to the 2.2.x stream via the `[rhtpa-2.2]` suffix. CVSS is 7.5 (High).

2. **Version Impact Analysis (Step 2)**: Within the 2.2.x stream, versions RHTPA 2.2.0 (quinn-proto 0.11.9) and RHTPA 2.2.1 (quinn-proto 0.11.12) are affected. RHTPA 2.2.2 is a retag of 2.2.1 and also affected. RHTPA 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are NOT affected. The 2.1.x stream is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9), but that is outside this issue's stream scope.

3. **Affects Versions (Step 3)**: PSIRT assigned only `[RHTPA 2.2.0]`, but lock file analysis shows `[RHTPA 2.2.0, RHTPA 2.2.1]` should be the correct set. However, TC-7999 already has the correct Affects Versions, making this correction moot for TC-8003.

4. **Duplicate Check (Step 4)**: JQL search found TC-7999 with the same CVE label (CVE-2026-31812), same stream suffix [rhtpa-2.2], and status In Progress. Per Step 4.1, a same-stream sibling that is open or in progress triggers a duplicate closure recommendation. TC-7999 already has the correct Affects Versions (RHTPA 2.2.0, RHTPA 2.2.1) and is actively being worked on.

5. **Steps 5-8 are bypassed**: Since the issue is being closed as duplicate, version lifecycle check, already-fixed check, concurrent triage detection, and remediation task creation are all skipped. The sibling issue TC-7999 is responsible for remediation.

## Proposed Jira Mutations (require engineer confirmation)

1. **Add comment to TC-8003**:
   > Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. Version impact analysis confirms overlap: both issues cover quinn-proto < 0.11.14 affecting RHTPA 2.2.0 and RHTPA 2.2.1. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1].
   >
   > _This triage was performed by the triage-security skill._

2. **Transition TC-8003** to Closed with resolution **Duplicate**

3. **Assign TC-8003** to current user

4. **Add label** `ai-cve-triaged` to TC-8003

## Summary

| Attribute | Value |
|-----------|-------|
| Issue | TC-8003 |
| CVE | CVE-2026-31812 |
| Library | quinn-proto |
| Fix threshold | >= 0.11.14 |
| Stream scope | 2.2.x ([rhtpa-2.2]) |
| Affected versions in scope | RHTPA 2.2.0, RHTPA 2.2.1 |
| Not affected in scope | RHTPA 2.2.3, RHTPA 2.2.4 |
| Duplicate of | TC-7999 (In Progress) |
| Triage decision | Close as Duplicate |
| Remediation tasks created | None (handled by TC-7999) |
