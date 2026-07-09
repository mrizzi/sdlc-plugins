# Step 8 -- Remediation: CVE-2026-31812

## Triage Outcome

This issue is **scoped** to stream 2.2.x (suffix `[rhtpa-2.2]`).

- **Affected versions within scope (2.2.x)**: 2.2.0, 2.2.1, 2.2.2
- **Affected versions outside scope (2.1.x)**: 2.1.0, 2.1.1

This triggers **Case A** (affected -- create remediation tasks for the scoped
stream) and **Case B** (cross-stream impact -- 2.1.x is also affected).

## Case A: Remediation Tasks for Stream 2.2.x

Ecosystem: **Cargo** (source dependency) -- requires TWO tasks:
1. Upstream backport task (fix in rhtpa-backend source repo)
2. Downstream propagation subtask (update reference in Konflux release repo)

---

### Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct
- quinn-proto is a direct runtime dependency of the backend workspace

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- Run `cargo update -p quinn-proto` to update Cargo.lock
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
```

---

### Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## Jira Linkage for Stream 2.2.x

1. Link upstream backport task to TC-8001 with type "Depend"
2. Link downstream propagation subtask as blocked by upstream backport task with type "Blocks"
3. Transition TC-8001 to In Progress
4. Post comment to TC-8001 listing created tasks:
   "Remediation tasks created: [upstream-task-key] (upstream backport),
   [downstream-task-key] (downstream propagation, blocked by [upstream-task-key])"

---

## Case B: Cross-Stream Impact (2.1.x)

The version impact analysis reveals that stream **2.1.x** (outside the issue's
scope) is also affected:
- 2.1.0: quinn-proto 0.11.9 -- AFFECTED
- 2.1.1: quinn-proto 0.11.9 -- AFFECTED

### Cross-stream impact comment on TC-8001

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. This stream is tracked by companion issues
(see Related links) or may require separate PSIRT triage.
```

### Proactive remediation for 2.1.x

If no existing CVE Jira for CVE-2026-31812 scoped to stream 2.1.x is found,
create **preemptive** remediation tasks for stream 2.1.x:

#### Preemptive Upstream Backport Task (2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0, 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct
- quinn-proto is a direct runtime dependency of the backend workspace

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml
- Run `cargo update -p quinn-proto` to update Cargo.lock
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
```

**Link type**: "Related" to TC-8001 (not "Depend", because the originating CVE belongs to a different stream)

#### Preemptive Downstream Propagation Subtask (2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: preemptive upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Link type**: "Related" to TC-8001

### Comment on TC-8001 for preemptive tasks

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: [upstream-task-key] (security-preemptive, upstream backport)
- 2.1.x: [downstream-task-key] (security-preemptive, downstream propagation)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Post-Triage Summary

After all actions complete:

1. **Add `ai-cve-triaged` label** to TC-8001
2. **Post summary comment** to TC-8001 documenting:
   - Version impact table (all versions across both streams)
   - Affects Versions correction: `RHTPA 2.0.0` -> `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2`
   - Triage outcome: remediation tasks created for 2.2.x, preemptive tasks for 2.1.x
   - Links to all remediation tasks
   - @mention of the vulnerability issue reporter
