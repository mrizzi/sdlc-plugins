# Triage Outcome -- TC-8020

## Summary

CVE-2026-31812 affects `quinn-proto` versions before 0.11.14, causing a denial-of-service panic via excessive QUIC stream counts. The issue is scoped to stream **2.2.x** per the summary suffix `[rhtpa-2.2]`.

## Version Impact

Within the scoped stream (2.2.x):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | fixed at threshold |
| 2.2.4 | 0.11.14 | NO | fixed at threshold |

Three versions in the 2.2.x stream are affected (2.2.0, 2.2.1, 2.2.2). Two versions (2.2.3, 2.2.4) already ship the fixed version.

Cross-stream: all 2.1.x versions (2.1.0, 2.1.1) are also affected, shipping quinn-proto 0.11.9.

## Affects Versions Correction

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Corrected (lock file evidence)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

The PSIRT-assigned version RHTPA 2.0.0 is incorrect -- no 2.0.x version stream exists in the Security Configuration. The correction is scoped to the 2.2.x stream per the issue suffix. Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14 (at or above the fix threshold).

## Triage Decision: Case A + Case B (with Step 7 gate)

### Case A -- Affected: Remediation Required (2.2.x stream)

Supported versions within the issue's stream scope are affected. Remediation tasks would be created:

- **Upstream backport task**: Bump quinn-proto to >= 0.11.14 in the `backend` source repository on the `release/0.4.z` branch. The upstream fix PR [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) provides the patch.
- **Downstream propagation subtask**: Update the backend source tag in `artifacts.lock.yaml` in the Konflux release repo (`rhtpa-release.0.4.z`) to pick up the bumped dependency. Blocked by the upstream task.

Ecosystem: Cargo (source dependency) -- produces 2 tasks (upstream + downstream).

### Case B -- Cross-Stream Impact (2.1.x stream)

The version impact analysis reveals that stream **2.1.x** is also affected (all versions ship quinn-proto 0.11.9). This issue is scoped to 2.2.x, so 2.1.x impact is handled as cross-stream:

- A cross-stream impact comment would be posted on TC-8020 noting that 2.1.x is affected.
- If no companion CVE Jira exists for 2.1.x, proactive (preemptive) remediation tasks would be created with the `security-preemptive` label and "Related" link type.
- If a companion CVE Jira already exists for 2.1.x (e.g., with suffix `[rhtpa-2.1]`), task creation for that stream is skipped.

### Step 7 Gate -- Concurrent Triage Detected

Before creating any remediation tasks, Step 7 detected a concurrent triage:

- **TC-8019** is In Progress, assigned to `engineer-b@example.com`, and also targets `quinn-proto` (same Upstream Affected Component value).

The engineer must choose before remediation proceeds:

1. **Wait** -- Pause until TC-8019 completes. If TC-8019's remediation bumps quinn-proto past 0.11.14, TC-8020 may already be covered (detectable via Step 4.3 cross-CVE overlap on re-run).
2. **Skip** -- Skip task creation entirely and document the reason in a Jira comment.
3. **Proceed** -- Create tasks with a `concurrent-triage-overlap` label so TC-8019's triage can detect the overlap.

## Post-Triage Actions (pending engineer choice on Step 7)

Once the engineer resolves the concurrent triage gate:

1. **Affects Versions**: Update from `[RHTPA 2.0.0]` to `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
2. **Label**: Add `ai-cve-triaged` to TC-8020
3. **Remediation tasks**: Create upstream + downstream tasks for 2.2.x (if proceeding)
4. **Cross-stream notice**: Post comment about 2.1.x impact; create preemptive tasks if no companion CVE Jira exists
5. **Summary comment**: Post triage summary with version impact table, corrections, and remediation task links; @mention the issue reporter
