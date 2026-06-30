# Triage Outcome — TC-8003

## Decision: Close as Duplicate

**TC-8003** is a duplicate of **TC-7999**. Both issues track the same vulnerability (CVE-2026-31812 in quinn-proto) for the same product stream (2.2.x / [rhtpa-2.2]).

## Summary of Analysis

### Step 1 — Data Extraction
- CVE-2026-31812 affects quinn-proto versions before 0.11.14 (CVSS 7.5, High severity)
- Issue is scoped to the 2.2.x stream via summary suffix `[rhtpa-2.2]`
- Ecosystem: Cargo (Rust crate, source dependency)

### Step 2 — Version Impact Analysis (2.2.x stream)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | — | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | fixed |
| 2.2.4 | 0.11.14 | NO | fixed |

Versions 2.2.0 through 2.2.2 ship a vulnerable version of quinn-proto. The fix was picked up in version 2.2.3 (build v0.4.11).

### Step 3 — Affects Versions Correction
Not performed. Since the issue is being closed as a duplicate, Affects Versions correction is not needed. The sibling issue TC-7999 already has the correct Affects Versions (RHTPA 2.2.0, RHTPA 2.2.1).

### Step 4 — Duplicate Check
TC-7999 was identified as a same-stream sibling:
- Same CVE: CVE-2026-31812
- Same stream: [rhtpa-2.2] (2.2.x)
- Status: In Progress (actively being remediated)
- Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (superset of TC-8003's RHTPA 2.2.0)

Per Step 4.1, same-stream siblings that are open or in progress trigger a duplicate closure of the current issue.

### Steps 5-7 — Skipped
Steps 5 (Version Lifecycle Check), 6 (Already Fixed Check), and 7 (Remediation) are skipped because TC-8003 is being closed as a duplicate. All remediation is handled through TC-7999.

## Proposed Jira Mutations (require engineer confirmation)

1. Add comment to TC-8003 documenting the duplicate finding and version impact evidence
2. Transition TC-8003 to **Closed** with resolution **Duplicate**
3. Assign TC-8003 to current user
4. Add label `ai-cve-triaged` to TC-8003

## No Remediation Tasks Created

No new remediation tasks are needed. TC-7999 (the existing sibling) is In Progress and owns remediation for CVE-2026-31812 in the 2.2.x stream.
