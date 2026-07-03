# Triage Outcome for TC-8020

## Summary

**CVE**: CVE-2026-31812
**Library**: quinn-proto
**Fix threshold**: 0.11.14
**Issue scope**: 2.2.x stream (from summary suffix `[rhtpa-2.2]`)
**Ecosystem**: Cargo (Rust crate)

## Version Impact Table

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | Cross-stream (outside scope) |
| 2.1.1 | 2.1.x | 0.11.9 | YES | Cross-stream (outside scope) |
| 2.2.0 | 2.2.x | 0.11.9 | YES | In scope |
| 2.2.1 | 2.2.x | 0.11.12 | YES | In scope |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | Fixed (>= 0.11.14) |
| 2.2.4 | 2.2.x | 0.11.14 | NO | Fixed (>= 0.11.14) |

## Affects Versions Correction (Step 3)

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Proposed (from lock file analysis, scoped to 2.2.x)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

The PSIRT-assigned version `RHTPA 2.0.0` is incorrect -- there is no 2.0.x stream. The correct Affects Versions are the 2.2.x versions where quinn-proto is below the fix threshold. Versions 2.2.3 and 2.2.4 are excluded because they already ship the fixed version (0.11.14).

## Triage Decision

### Case Classification

This issue falls under **Case A + Case B**:

- **Case A (Affected)**: Within the scoped 2.2.x stream, versions 2.2.0, 2.2.1, and 2.2.2 are affected and require remediation.
- **Case B (Cross-stream impact)**: The 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9). A cross-stream notice would be posted, and proactive remediation tasks would be created for the 2.1.x stream if no companion CVE Jira exists for that stream.

### Remediation Plan (Case A -- 2.2.x stream)

Since quinn-proto is a **Cargo** (source dependency) ecosystem, two tasks would be created:

1. **Upstream backport task**: Bump quinn-proto to >= 0.11.14 in the `backend` source repository on branch `release/0.4.z`.
   - Summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)"
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
   - Linked to TC-8020 with "Depend"

2. **Downstream propagation subtask**: Update the backend reference in `rhtpa-release.0.4.z` to pick up the upstream fix.
   - Summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)"
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
   - Blocked by the upstream backport task
   - Linked to TC-8020 with "Depend"

### Cross-Stream Notice (Case B -- 2.1.x stream)

A comment would be posted on TC-8020:

> Cross-stream impact: quinn-proto (versions before 0.11.14) also affects stream 2.1.x based on lock file analysis. All 2.1.x versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

If no companion CVE Jira exists for the 2.1.x stream, preemptive remediation tasks would be created with the `security-preemptive` label and "Related" link type to TC-8020.

## Step 7 -- Concurrent Triage Block

**Remediation task creation is currently blocked by Step 7 (Concurrent Triage Detection).**

TC-8019 is `In Progress` on the same upstream component (`quinn-proto`), assigned to `engineer-b@example.com`. The engineer must choose one of:

1. **Wait** -- pause until TC-8019 completes, then re-run to check for overlap
2. **Skip** -- skip task creation entirely
3. **Proceed** -- create tasks with `concurrent-triage-overlap` label

Until the engineer makes this choice, no remediation tasks are created and no further Jira mutations are performed.

### Rationale

The concurrent triage on TC-8019 may produce remediation tasks that bump `quinn-proto` to a version meeting or exceeding the fix threshold for both CVEs. Waiting allows Step 4.3 (cross-CVE overlap detection) to identify covering remediations and avoid duplicates. If the engineer chooses to proceed, the `concurrent-triage-overlap` label ensures the other triage's Step 4.3 will detect and reconcile the overlap.

## Post-Triage Actions (pending Step 7 resolution)

Once Step 7 is resolved and remediation proceeds:

1. Add `ai-cve-triaged` label to TC-8020
2. Post a summary comment on TC-8020 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 replaced with RHTPA 2.2.0, 2.2.1, 2.2.2)
   - Remediation tasks created (upstream + downstream for 2.2.x)
   - Cross-stream impact notice for 2.1.x
   - @mention of the issue reporter
3. Transition TC-8020 to In Progress
