# Step 8 -- Remediation

## Triage Outcome

This is **Case A + Case B**: the issue's scoped stream (2.2.x) has affected
versions requiring remediation (Case A), and a cross-stream analysis reveals
that the 2.1.x stream is also affected (Case B).

- **Case A** (2.2.x -- scoped stream): Versions 2.2.0, 2.2.1, and 2.2.2
  ship quinn-proto < 0.11.14. Create standard remediation tasks.
- **Case B** (2.1.x -- cross-stream impact): Versions 2.1.0 and 2.1.1 ship
  quinn-proto 0.11.9. Create preemptive remediation tasks (if no existing
  CVE Jira covers 2.1.x).

Ecosystem: **Cargo** (source dependency) -- two tasks per affected stream:
1. Upstream backport task (fix in the source repo)
2. Downstream propagation subtask (update reference in Konflux release repo)

---

## Case A: Remediation Tasks for 2.2.x Stream (Scoped)

### Task 1: Upstream Backport Task (2.2.x)

**PROPOSAL: Create Jira Task with the following details.**

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9),
RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12),
RHTPA 2.2.2 (v0.4.9, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Jira API call**:
```
upstream_task_2_2 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <upstream-task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Post-creation**: Post description digest comment, then link to TC-8001
with "Depend" link type.

---

### Task 2: Downstream Propagation Subtask (2.2.x)

**PROPOSAL: Create Jira Task with the following details.**

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Jira API call**:
```
downstream_task_2_2 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <downstream-task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Post-creation**: Post description digest comment, then:
- Link to TC-8001 with "Depend" link type
- Link as blocked by upstream task with "Blocks" link type

---

## Case B: Cross-Stream Impact -- 2.1.x Preemptive Remediation

**Cross-stream impact comment** proposed for TC-8001:
```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. Versions 2.1.0 and 2.1.1 both ship
quinn-proto 0.11.9.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

If no existing CVE Jira covers the 2.1.x stream for CVE-2026-31812,
the following preemptive remediation tasks would be created:

### Task 3: Upstream Backport Task (2.1.x -- Preemptive)

**PROPOSAL: Create Jira Task with the following details.**

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from
> cross-stream impact analysis of TC-8001 (stream 2.2.x). No
> stream-specific CVE Jira exists yet for this stream. When PSIRT
> creates one, this task will be linked and the `security-preemptive`
> label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8, quinn-proto 0.11.9),
RHTPA 2.1.1 (v0.3.12, quinn-proto 0.11.9)
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

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Jira API call**:
```
upstream_task_2_1 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <upstream-task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Post-creation**: Post description digest comment, then link to TC-8001
with "Related" link type (not "Depend", because this is a preemptive task
from a different stream).

---

### Task 4: Downstream Propagation Subtask (2.1.x -- Preemptive)

**PROPOSAL: Create Jira Task with the following details.**

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from
> cross-stream impact analysis of TC-8001 (stream 2.2.x). No
> stream-specific CVE Jira exists yet for this stream. When PSIRT
> creates one, this task will be linked and the `security-preemptive`
> label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <upstream-task-key-2.1>.

The upstream backport (<upstream-task-key-2.1>) bumps quinn-proto to
0.11.14 on release/0.3.z. Once that PR merges, update the source pinning
in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key-2.1> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Jira API call**:
```
downstream_task_2_1 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <downstream-task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Post-creation**: Post description digest comment, then:
- Link to TC-8001 with "Related" link type (preemptive)
- Link as blocked by upstream task (2.1.x) with "Blocks" link type

---

## Preemptive Task Comment on TC-8001

**PROPOSAL: Post comment to TC-8001 listing the preemptive tasks.**

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-key-2.1> (security-preemptive, upstream backport)
- 2.1.x: <downstream-task-key-2.1> (security-preemptive, downstream propagation)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Linkage Summary

After all tasks are created, the following links would be established:

| From | To | Link Type | Rationale |
|------|----|-----------|-----------|
| TC-8001 | upstream-task-2.2 | Depend | Standard remediation linkage |
| TC-8001 | downstream-task-2.2 | Depend | Standard remediation linkage |
| upstream-task-2.2 | downstream-task-2.2 | Blocks | Downstream blocked by upstream |
| TC-8001 | upstream-task-2.1 | Related | Preemptive (different stream) |
| TC-8001 | downstream-task-2.1 | Related | Preemptive (different stream) |
| upstream-task-2.1 | downstream-task-2.1 | Blocks | Downstream blocked by upstream |

## Post-Triage Label

**PROPOSAL: Add `ai-cve-triaged` label to TC-8001** to mark it as triaged.
