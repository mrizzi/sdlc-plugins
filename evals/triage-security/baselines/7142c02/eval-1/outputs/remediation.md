# Step 7 -- Remediation: TC-8001

## Triage Outcome

**Case A + Case B**: The issue's scoped stream (2.2.x) has affected versions (2.2.0, 2.2.1, 2.2.2), though the fix is already present in versions 2.2.3 and 2.2.4. Additionally, the 2.1.x stream is affected across all versions (cross-stream impact).

Since quinn-proto is a **Cargo** (source dependency) ecosystem package, each affected stream requires **two tasks**: an upstream backport task and a downstream propagation subtask.

---

## Case A: Remediation Tasks for Scoped Stream (2.2.x)

The 2.2.x stream already ships the fix starting from version 2.2.3 (build tag v0.4.11). The upstream branch `release/0.4.z` already contains the fix. No new upstream backport is needed for this stream since the fix is already present on the branch and in recent releases.

However, versions 2.2.0, 2.2.1, and 2.2.2 remain affected in their shipped form. Since 2.2.3+ already includes the fix, the remediation path for 2.2.x is already complete -- no additional tasks are needed for this stream. The Affects Versions correction (Step 3) accurately documents which versions were affected.

**Recommendation for 2.2.x**: No remediation tasks needed. The vulnerability was fixed in version 2.2.3 (build 0.4.11) which ships quinn-proto 0.11.14. The Affects Versions field has been corrected to reflect 2.2.0, 2.2.1, and 2.2.2 as the affected versions.

---

## Case B: Cross-Stream Impact -- Preemptive Remediation for 2.1.x

The version impact analysis reveals that the **2.1.x** stream (outside this issue's scope) is also affected. All 2.1.x versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is within the vulnerable range (< 0.11.14).

Since no stream-specific CVE Jira exists for the 2.1.x stream, preemptive remediation tasks are created with the `security-preemptive` label and "Related" link type.

### Task 1: Upstream Backport (2.1.x stream)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

### Task 2: Downstream Propagation (2.1.x stream)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Proposed Jira Linkage

### For preemptive tasks (2.1.x stream):

```
# Link upstream backport task to TC-8001 as Related (preemptive)
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: "<upstream-task-key>",
  type: "Related"
)

# Link downstream propagation task to TC-8001 as Related (preemptive)
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: "<downstream-task-key>",
  type: "Related"
)

# Link downstream as blocked by upstream
jira.create_link(
  inwardIssue: "<upstream-task-key>",
  outwardIssue: "<downstream-task-key>",
  type: "Blocks"
)
```

## Proposed Cross-Stream Impact Comment on TC-8001

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. All versions in the 2.1.x stream (2.1.0, 2.1.1)
ship quinn-proto 0.11.9.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-key> (upstream backport, security-preemptive)
- 2.1.x: <downstream-task-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8001
2. Post summary comment to TC-8001 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 removed, RHTPA 2.2.0/2.2.1/2.2.2 added)
   - 2.2.x stream already fixed in 2.2.3+ (no remediation tasks needed for 2.2.x)
   - Cross-stream impact on 2.1.x with preemptive remediation tasks
   - @mention of issue reporter
3. Transition TC-8001 to In Progress
4. Assign TC-8001 to current user
