# Triage Outcome: TC-8003

## Decision: Close as Duplicate

TC-8003 should be **closed as Duplicate** of TC-7999.

## Rationale

1. **Same CVE**: Both TC-8003 and TC-7999 track CVE-2026-31812 (quinn-proto panic on large stream counts).

2. **Same stream scope**: Both issues have the stream suffix `[rhtpa-2.2]`, scoping them to the 2.2.x version stream. PSIRT creates one Vulnerability issue per stream, so having two issues for the same CVE in the same stream is a duplicate.

3. **TC-7999 is already In Progress**: The sibling issue TC-7999 is actively being worked on, with status "In Progress". It already has the correct Affects Versions (RHTPA 2.2.0, RHTPA 2.2.1), which is a superset of TC-8003's Affects Versions (RHTPA 2.2.0 only).

4. **Version impact analysis confirms overlap**: The lock file analysis shows quinn-proto is vulnerable in versions 2.2.0 (v0.11.9), 2.2.1 (v0.11.12), and 2.2.2 (retag of 2.2.1), all of which are below the fixed version 0.11.14. The fix was already picked up in version 2.2.3 (v0.11.14). TC-7999 already tracks this same set of affected versions for the same stream.

5. **No remediation tasks needed from TC-8003**: Since TC-7999 is the active tracker and is already In Progress, any remediation work (upstream backport of quinn-proto to >= 0.11.14 on the release/0.4.z branch, plus downstream propagation in the Konflux release repo rhtpa-release.0.4.z) would be tracked under TC-7999.

## Proposed Jira Actions

The following actions would be performed after engineer confirmation:

1. **Add comment to TC-8003**:
   > Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. Version impact analysis confirms overlap.
   >
   > Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):
   >
   > | Version | quinn-proto | Affected? | Notes |
   > |---------|-------------|-----------|-------|
   > | 2.2.0 | 0.11.9 | YES | |
   > | 2.2.1 | 0.11.12 | YES | |
   > | 2.2.2 | -- | YES | retag of 2.2.1 |
   > | 2.2.3 | 0.11.14 | NO | fixed version |
   > | 2.2.4 | 0.11.14 | NO | fixed version |
   >
   > TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]. No additional tracking needed.

2. **Transition TC-8003** to Closed with resolution **Duplicate**.

3. **Assign TC-8003** to the current user.

4. **Add label** `ai-cve-triaged` to TC-8003.

## Steps Not Executed

Because TC-8003 is a duplicate, the following steps are short-circuited:

- **Step 3 (Affects Versions Correction)**: Not needed -- the issue is being closed as Duplicate; no point correcting versions on an issue that will be closed.
- **Step 5 (Version Lifecycle Check)**: Not needed -- TC-7999 is the active tracker.
- **Step 6 (Already Fixed Check)**: Not needed -- TC-7999 is In Progress, not resolved.
- **Step 7 (Remediation)**: Not needed -- remediation is tracked under TC-7999.

## Cross-Stream Impact Note

The version impact analysis also covers the 2.1.x stream (for completeness):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |

The 2.1.x stream is also affected by CVE-2026-31812, but that is outside the scope of TC-8003 (which is scoped to [rhtpa-2.2]). Any 2.1.x tracking would be handled by a separate PSIRT-created Vulnerability issue for that stream. This is noted for informational purposes only -- no action is taken for cross-stream impact on a duplicate issue.
