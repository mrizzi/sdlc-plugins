# Triage Outcome for TC-8020

## Issue Summary

- **Issue**: TC-8020
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto (Cargo ecosystem)
- **Fix threshold**: >= 0.11.14
- **CVSS**: 7.5 (High)
- **Stream scope**: 2.2.x (per summary suffix `[rhtpa-2.2]`)

## Version Impact Summary

### Stream 2.2.x (in scope)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | fixed version |
| 2.2.4 | 0.11.14 | NO | fixed version |

### Stream 2.1.x (outside scope -- cross-stream impact)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |

## Affects Versions Correction (Step 3)

PSIRT assigned **RHTPA 2.0.0**, which does not correspond to any configured version stream. The correct Affects Versions for the 2.2.x-scoped issue are:

- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14 (the fixed version). Versions from stream 2.1.x are excluded because this issue is scoped to 2.2.x.

## Triage Decision

### Primary: Case A -- Affected (remediation required)

Supported versions 2.2.0, 2.2.1, and 2.2.2 within the issue's scoped stream (2.2.x) ship a vulnerable version of quinn-proto (< 0.11.14). Remediation is required.

Since quinn-proto is a **Cargo** (source dependency) ecosystem package, the standard remediation path creates **two tasks** per affected stream:

1. **Upstream backport task**: Bump quinn-proto to >= 0.11.14 in the `rhtpa-backend` source repository on branch `release/0.4.z`
2. **Downstream propagation subtask**: Update the backend source reference in `rhtpa-release.0.4.z` to pick up the upstream fix (blocked by the upstream task)

Note: The upstream fix PR (quinn-rs/quinn#2048) already exists, so the upstream backport task involves pulling this fix into the product's source repo branch.

### Secondary: Case B -- Cross-stream impact

The issue is scoped to stream 2.2.x, but the version impact analysis reveals that stream **2.1.x** is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). This triggers Case B cross-stream impact handling:

1. Post a cross-stream impact comment on TC-8020
2. Search for existing CVE Jiras for CVE-2026-31812 in stream 2.1.x
3. If no 2.1.x CVE Jira exists, create preemptive remediation tasks with the `security-preemptive` label for stream 2.1.x

### Step 7 Gate: Concurrent Triage Detected

Before proceeding to Case A/B task creation, Step 7 detected that **TC-8019** (In Progress, assigned to engineer-b@example.com) is actively being triaged for the same upstream component (`quinn-proto`). The engineer must choose one of three options:

1. **Wait** (recommended) -- pause until TC-8019 triage completes, then re-run to detect overlap
2. **Skip** -- skip remediation task creation entirely
3. **Proceed** -- create tasks with `concurrent-triage-overlap` label

**Recommendation**: Wait for TC-8019 to complete. The concurrent triage on the same component means TC-8019's remediation tasks may already cover the quinn-proto bump to >= 0.11.14. After TC-8019 completes, re-running Step 4.3 (Cross-CVE Overlap Detection) will determine if the existing remediation covers TC-8020's fix threshold, potentially allowing TC-8020 to be resolved without creating duplicate tasks.

## Proposed Actions (pending Step 7 resolution)

If the engineer proceeds (Option 3) or after wait (Option 1) confirms no overlap:

1. **Correct Affects Versions**: `[RHTPA 2.0.0]` -> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
2. **Create upstream backport task** for stream 2.2.x: bump quinn-proto to >= 0.11.14 in rhtpa-backend on release/0.4.z
3. **Create downstream propagation subtask** for stream 2.2.x: update backend ref in rhtpa-release.0.4.z (blocked by upstream task)
4. **Post cross-stream impact comment**: stream 2.1.x is also affected
5. **Create preemptive remediation tasks for stream 2.1.x** (if no 2.1.x CVE Jira exists): upstream + downstream tasks with `security-preemptive` label
6. **Link** all tasks to TC-8020
7. **Add `ai-cve-triaged` label** to TC-8020
8. **Post summary comment** with version impact table, Affects Versions correction, and remediation task links

If TC-8019's remediation already covers the fix (after wait/re-check):

1. **Correct Affects Versions** as above
2. **Link** TC-8020 to TC-8019 (Related) and to TC-8019's covering remediation task (Depend)
3. **Post cross-CVE overlap comment** documenting that the existing remediation covers this CVE
4. **Recommend close** as covered by existing remediation
5. **Add `ai-cve-triaged` label** to TC-8020
