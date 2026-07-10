# Step 8 -- Remediation for TC-8001

## Triage Outcome

**Case A** applies for the 2.2.x stream (issue scope): versions 2.2.0, 2.2.1, and 2.2.2 are affected.

**Case B** also applies: the 2.1.x stream (outside issue scope) is also affected (versions 2.1.0, 2.1.1 ship quinn-proto 0.11.9). A cross-stream impact comment would be posted, and preemptive remediation tasks created for the 2.1.x stream if no sibling CVE Jira exists for that stream.

Since quinn-proto is a **Cargo** (source dependency) ecosystem, **two tasks** are created per affected stream: an upstream backport task and a downstream propagation subtask.

---

## Task 1: Upstream Backport Task (2.2.x stream)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

Note: Versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already ship quinn-proto 0.11.14 and are not affected. The fix is already present on the release/0.4.z branch at later tags.

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct dependency (backend workspace -> quinn-proto)

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- The fix is already available upstream (quinn-rs/quinn#2048)
- Versions 2.2.3+ on this branch already include the fix, confirming compatibility

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Task 2: Downstream Propagation Subtask (2.2.x stream)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

### Task Description

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

---

## Case B: Cross-Stream Impact (2.1.x stream)

The 2.1.x stream is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). Since the issue TC-8001 is scoped to `[rhtpa-2.2]`, this is a cross-stream impact finding.

### Cross-stream impact comment (to be posted on TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. Versions affected: 2.1.0 (quinn-proto 0.11.9),
2.1.1 (quinn-proto 0.11.9).
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

### Preemptive Remediation Tasks (2.1.x stream)

If no sibling CVE Jira exists for the 2.1.x stream, create preemptive tasks:

#### Preemptive Task 3: Upstream Backport (2.1.x stream)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001, not Depend -- originating CVE belongs to a different stream)

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8, quinn-proto 0.11.9), RHTPA 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct dependency (backend workspace -> quinn-proto)

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- The fix is available upstream (quinn-rs/quinn#2048)
- Unlike the 2.2.x stream, no existing tag on release/0.3.z ships the fix yet

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8001 (originating CVE Jira, different stream)

#### Preemptive Task 4: Downstream Propagation (2.1.x stream)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001)

### Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

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

- Depends on: preemptive upstream backport task for 2.1.x (must merge first)
- Related to: TC-8001 (originating CVE Jira, different stream)

---

## Jira Linkage Summary

### Standard remediation (2.2.x stream -- Case A)

1. Link upstream backport task to TC-8001 with type "Depend"
2. Link downstream propagation subtask to TC-8001 with type "Depend"
3. Link downstream subtask as blocked by upstream task with type "Blocks"

### Preemptive remediation (2.1.x stream -- Case B)

1. Link preemptive upstream task to TC-8001 with type "Related" (not Depend)
2. Link preemptive downstream subtask to TC-8001 with type "Related"
3. Link preemptive downstream subtask as blocked by preemptive upstream task with type "Blocks"

### Post-triage actions

1. Add `ai-cve-triaged` label to TC-8001
2. Post summary comment on TC-8001 documenting version impact, Affects Versions correction, triage outcome, and links to all remediation tasks
3. @mention the issue reporter in the summary comment
