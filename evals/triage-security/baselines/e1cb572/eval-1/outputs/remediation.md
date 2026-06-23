# Step 7 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

This is **Case A + Case B**:
- **Case A**: The issue's stream-scoped versions (2.2.x) include affected versions (2.2.0, 2.2.1, 2.2.2) -- remediation tasks are needed for stream 2.2.x.
- **Case B**: Cross-stream impact detected -- stream 2.1.x is also affected (2.1.0, 2.1.1) but is outside this issue's scope. Preemptive remediation tasks are created for 2.1.x.

Ecosystem: **Cargo** (source dependency) -- requires **two tasks per stream** (upstream backport + downstream propagation).

---

## Case A: Stream 2.2.x Remediation Tasks

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

**Description**:

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

Note: The fix is already present on the release/0.4.z branch at tag v0.4.11+.
This task may already be resolved if the branch HEAD contains quinn-proto >= 0.11.14.

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
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

### Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

**Description**:

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
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

### Jira Linkage (2.2.x tasks)

```
# Link upstream task to Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)

# Link downstream task to Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

# Link downstream task as blocked by upstream task
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

---

## Case B: Cross-Stream Impact -- Stream 2.1.x Preemptive Remediation

Cross-stream impact detected: quinn-proto < 0.11.14 also affects stream 2.1.x (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9).

No sibling CVE Jira exists for stream 2.1.x (no issue with label CVE-2026-31812 and suffix [rhtpa-2.1] was found). Preemptive remediation tasks are created.

### Cross-Stream Impact Comment (posted to TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. Versions 2.1.0 and 2.1.1 both ship
quinn-proto 0.11.9. This stream is not tracked by a companion
CVE Jira and may require separate PSIRT triage.
```

### Task 3: Preemptive Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for stream 2.1.x. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
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

- Related to: TC-8001 (originating CVE Jira, different stream)

---

### Task 4: Preemptive Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for stream 2.1.x. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

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

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: preemptive upstream backport task (upstream backport must merge first)
- Related to: TC-8001 (originating CVE Jira, different stream)

---

### Jira Linkage (2.1.x preemptive tasks)

```
# Link preemptive upstream task to originating CVE with "Related" (not "Depend")
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <preemptive-upstream-task-key>,
  type: "Related"
)

# Link preemptive downstream task to originating CVE with "Related"
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Related"
)

# Link preemptive downstream as blocked by preemptive upstream
jira.create_link(
  inwardIssue: <preemptive-upstream-task-key>,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Blocks"
)
```

### Preemptive Tasks Comment (posted to TC-8001)

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-key> (security-preemptive, upstream backport)
- 2.1.x: <downstream-task-key> (security-preemptive, downstream propagation)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Post-Triage Actions

### Add ai-cve-triaged label

```
jira.edit_issue("TC-8001", fields={
  "labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### Transition to In Progress

```
jira.transition_issue("TC-8001", transition="In Progress")
```

### Post-Triage Summary Comment (posted to TC-8001)

```
## Triage Summary -- CVE-2026-31812 (quinn-proto)

### Version Impact

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0   | 0.11.9      | YES       |       |
| 2.1.1   | 0.11.9      | YES       |       |
| 2.2.0   | 0.11.9      | YES       |       |
| 2.2.1   | 0.11.12     | YES       |       |
| 2.2.2   | --          | YES       | retag of 2.2.1 |
| 2.2.3   | 0.11.14     | NO        | ships fixed version |
| 2.2.4   | 0.11.14     | NO        | ships fixed version |

### Affects Versions Correction

[RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

### Triage Outcome

Remediation tasks created for stream 2.2.x (Case A):
- <upstream-task-key>: upstream backport (bump quinn-proto to 0.11.14 on release/0.4.z)
- <downstream-task-key>: downstream propagation (update backend ref in rhtpa-release.0.4.z, blocked by upstream task)

Preemptive remediation tasks created for stream 2.1.x (Case B):
- <preemptive-upstream-key>: upstream backport (bump quinn-proto to 0.11.14 on release/0.3.z, security-preemptive)
- <preemptive-downstream-key>: downstream propagation (update backend ref in rhtpa-release.0.3.z, security-preemptive)

---
_This triage was performed by the triage-security skill._
```
