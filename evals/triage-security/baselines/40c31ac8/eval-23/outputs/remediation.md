# Step 8 — Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

- **Case A** applies: stream 2.2.x has affected versions (2.2.0, 2.2.1, 2.2.2)
- **Case B** also applies: stream 2.1.x is affected but outside the issue's scope

Ecosystem: **Cargo** (source dependency) — two tasks per stream: upstream backport + downstream propagation.

---

## Case A — Remediation Tasks for Stream 2.2.x (Issue Scope)

### Task 1: Upstream Backport Task (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Link**: Depend → TC-8001

#### Task Description

## Repository

backend

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

Note: The fix is already present on release/0.4.z at v0.4.11+ (quinn-proto 0.11.14). No new backport PR is needed — the upstream branch already ships the fixed version.

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- The fix is already present at tag v0.4.11 and later on this branch
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

### Task 2: Downstream Propagation Subtask (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Link**: Depend → TC-8001, Blocks → upstream backport task (Task 1)

#### Task Description

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

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Case B — Preemptive Remediation Tasks for Stream 2.1.x (Cross-Stream)

Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. Versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9.

The upstream fix is NOT present on the 2.1.x branch (release/0.3.z still ships quinn-proto 0.11.9). An upstream PR is required first.

These tasks are created with the **preemptive variant** because no stream-specific CVE Jira exists for 2.1.x.

### Preemptive Task 1: Upstream Backport Task (2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related → TC-8001 (not Depend, because originating CVE belongs to a different stream)

#### Task Description

## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8, quinn-proto 0.11.9), RHTPA 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

Note: The fix is NOT present on release/0.3.z (branch HEAD still ships quinn-proto 0.11.9). An upstream backport PR is required.

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
- The fix is NOT present upstream on this branch — a backport PR is required
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

### Preemptive Task 2: Downstream Propagation Subtask (2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related → TC-8001, Blocks → preemptive upstream backport task (Preemptive Task 1)

#### Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: preemptive upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Cross-Stream Impact Comment

The following comment would be posted to TC-8001:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. Versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9. Stream 2.1.x is not tracked by a companion CVE Jira.
>
> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: upstream backport task + downstream propagation task (security-preemptive)
>
> These tasks use the "Related" link type and carry the security-preemptive label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label.

## Post-Triage Summary

The following summary comment would be posted to TC-8001:

> **Triage summary for CVE-2026-31812 (quinn-proto < 0.11.14)**
>
> **Version impact:**
>
> | Version | Stream | quinn-proto | Affected? | Notes |
> |---------|--------|-------------|-----------|-------|
> | 2.1.0 | 2.1.x | 0.11.9 | YES | |
> | 2.1.1 | 2.1.x | 0.11.9 | YES | |
> | 2.2.0 | 2.2.x | 0.11.9 | YES | |
> | 2.2.1 | 2.2.x | 0.11.12 | YES | |
> | 2.2.2 | 2.2.x | — | YES | retag of 2.2.1 |
> | 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
> | 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |
>
> **Affects Versions correction:** `[RHTPA 2.0.0]` → `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]` (scoped to stream 2.2.x per issue suffix)
>
> **Triage outcome:** Remediation tasks created (Case A + Case B)
>
> **Remediation tasks (2.2.x — scoped stream):**
> - Upstream backport task (upstream backport on release/0.4.z)
> - Downstream propagation task (downstream propagation, blocked by upstream task)
>
> **Preemptive remediation tasks (2.1.x — cross-stream):**
> - Preemptive upstream backport task (security-preemptive, upstream backport on release/0.3.z)
> - Preemptive downstream propagation task (security-preemptive, downstream propagation, blocked by upstream task)
>
> Label `ai-cve-triaged` added.
