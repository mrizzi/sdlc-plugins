# Triage Outcome for TC-8020

## Issue Summary

- **Issue**: TC-8020
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Affected range**: versions before 0.11.14
- **Fixed version**: 0.11.14
- **CVSS**: 7.5 (High)
- **Stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Ecosystem**: Cargo (Rust crate)

## Version Impact Summary

### Stream 2.2.x (scoped -- this issue's stream)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 0.11.14 | NO | ships fixed version |

### Stream 2.1.x (cross-stream impact)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |

## Triage Decision

### Primary: Case A -- Affected (stream 2.2.x)

Versions 2.2.0, 2.2.1, and 2.2.2 within the scoped stream 2.2.x ship vulnerable versions of quinn-proto (0.11.9 and 0.11.12, both below the fix threshold of 0.11.14). Remediation is required.

**However**, versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (the fixed version). This means the vulnerability has already been resolved in the latest releases of the 2.2.x stream. The fix was incorporated starting from build v0.4.11 (version 2.2.3).

### Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is `RHTPA 2.0.0`, which is incorrect -- there is no 2.0.x stream configured. Based on lock file analysis, the correct Affects Versions for stream 2.2.x are:

- **Current**: `[RHTPA 2.0.0]`
- **Proposed**: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are excluded because they ship the fixed quinn-proto 0.11.14.

### Cross-Stream Impact: Case B (stream 2.1.x)

This issue is scoped to stream 2.2.x, but the version impact analysis reveals that stream 2.1.x is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). This triggers Case B -- cross-stream impact:

1. Post a cross-stream impact comment on TC-8020:
   > Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

2. Check for existing sibling CVE Jiras for stream 2.1.x with the same CVE label (CVE-2026-31812).

3. If no sibling exists for stream 2.1.x: create preemptive remediation tasks with the `security-preemptive` label and "Related" link type to TC-8020.

4. If a sibling already exists for stream 2.1.x: skip preemptive task creation for that stream (it will be triaged through its own CVE issue).

### Remediation Tasks (pending concurrent triage resolution)

Since this is a **Cargo** (source dependency) ecosystem, remediation would create **two tasks per affected stream**:

**For stream 2.2.x (Case A):**
1. **Upstream backport task**: Bump quinn-proto to >= 0.11.14 in the backend source repo on branch `release/0.4.z`
2. **Downstream propagation subtask**: Update the backend source reference in the Konflux release repo `rhtpa-release.0.4.z` to pick up the upstream fix (blocked by upstream task)

**For stream 2.1.x (Case B, preemptive -- if no sibling CVE exists):**
1. **Upstream backport task**: Bump quinn-proto to >= 0.11.14 in the backend source repo on branch `release/0.3.z` (with `security-preemptive` label)
2. **Downstream propagation subtask**: Update the backend source reference in the Konflux release repo `rhtpa-release.0.3.z` (with `security-preemptive` label, blocked by upstream task)

### Concurrent Triage Gate (Step 7)

Remediation task creation is **blocked** by concurrent triage detection. TC-8019 is actively being triaged by `engineer-b@example.com` and affects the same upstream component (`quinn-proto`). The engineer must choose one of:

1. **Wait** -- pause until TC-8019's triage completes, then re-run to detect overlap
2. **Skip** -- skip remediation task creation entirely
3. **Proceed** -- create tasks with `concurrent-triage-overlap` label for deduplication

Until the engineer makes this choice, no remediation tasks are created.

### Upstream Fix Status

The fix (quinn-proto 0.11.14) is already present in versions 2.2.3+ (build v0.4.11+), indicating that the upstream fix has already been applied to the `release/0.4.z` branch at some point. The upstream fix PR is available at [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048).

For stream 2.1.x, the upstream branch `release/0.3.z` would need to be checked at HEAD to determine if the fix has been applied there.

## Post-Triage Actions (after concurrent triage resolution)

1. **Add `ai-cve-triaged` label** to TC-8020
2. **Post summary comment** to TC-8020 with:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, 2.2.1, 2.2.2)
   - Triage outcome and remediation task links
   - @mention of the issue reporter
3. **Transition** TC-8020 to In Progress (after remediation tasks are created)
