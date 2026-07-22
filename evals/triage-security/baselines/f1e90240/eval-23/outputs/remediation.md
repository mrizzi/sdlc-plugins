# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

- **Issue scope**: 2.2.x stream (suffix `[rhtpa-2.2]`)
- **Ecosystem**: Cargo (source dependency)
- **Affected versions in scope**: RHTPA 2.2.0, 2.2.1, 2.2.2
- **Not affected in scope**: RHTPA 2.2.3, 2.2.4 (ship quinn-proto 0.11.14)
- **Cross-stream impact**: 2.1.x also affected (2.1.0, 2.1.1)
- **Deployment context**: customer-shipped

**Case A** applies for the 2.2.x stream (affected versions exist within scope).
**Case B** applies because the 2.1.x stream is also affected (cross-stream impact from a scoped issue).

Since the ecosystem is Cargo (source dependency), **two tasks** are created per affected stream: an upstream backport task and a downstream propagation subtask.

---

## Remediation Tasks -- Stream 2.2.x (Scoped -- Case A)

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8, v0.4.9

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

Note: The upstream fix is already present on release/0.4.z at v0.4.11+ (quinn-proto 0.11.14). Versions 2.2.3 and 2.2.4 already ship the fixed version. This task confirms the fix is correctly integrated and no additional backport is needed.

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (or transitive -- verify via Cargo.lock dependency chain)
- The fix is already present at tag v0.4.11 on this branch. Verify that quinn-proto >= 0.11.14 is in the Cargo.lock at branch HEAD.
- If the fix is already at HEAD, this task may only require verification and no code change.

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (see dependency chain)
- Bump the direct dependency to a version whose transitive closure includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable:
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct dependency, overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

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

### Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges (or the fix is confirmed at HEAD), update the source pinning in this
Konflux release repo so the next build ships the fix.

Note: Versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already include quinn-proto 0.11.14. This task ensures the Konflux release repo references are up to date and the fix is formally tracked.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: direct or transitive -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag that includes quinn-proto >= 0.11.14
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Preemptive Remediation Tasks -- Stream 2.1.x (Cross-Stream -- Case B)

The 2.1.x stream is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9), but no stream-specific CVE Jira exists for 2.1.x. Preemptive remediation tasks are created with the `security-preemptive` label and linked to the originating CVE Jira (TC-8001) with "Related" link type.

### Task 3: Upstream Backport -- Preemptive (2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001)

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8, quinn-proto 0.11.9), RHTPA 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

Note: The upstream fix is NOT yet present on release/0.3.z. The latest tag (v0.3.12) ships quinn-proto 0.11.9. An upstream backport is required.

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (or transitive -- verify via Cargo.lock dependency chain)
- The fix is NOT present on this branch. quinn-proto must be bumped from 0.11.9 to >= 0.11.14 on release/0.3.z.
- This is a multi-minor-version bump (0.11.9 to 0.11.14) -- review the quinn-proto changelog for breaking changes between these versions.

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (see dependency chain)
- Bump the direct dependency to a version whose transitive closure includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable:
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct dependency, overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8001 (originating CVE Jira, stream 2.2.x)

---

### Task 4: Downstream Propagation -- Preemptive (2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001)

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: direct or transitive -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag that includes quinn-proto >= 0.11.14
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: upstream backport task for 2.1.x (upstream backport must merge first)
- Related to: TC-8001 (originating CVE Jira, stream 2.2.x)

---

## Cross-Stream Impact Comment (for TC-8001)

Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: upstream backport task (security-preemptive) + downstream propagation task (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label.

---

## Coordination Guidance Summary

All remediation tasks for this CVE include the following coordination guidance in their Implementation Notes, because the affected repository (rhtpa-backend) has deployment context **customer-shipped**:

> This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

This guidance is derived from the Source Repositories table in the project CLAUDE.md Security Configuration, which specifies `customer-shipped` as the Deployment Context for rhtpa-backend.

---

## Post-Triage Summary

1. **Version impact**: quinn-proto < 0.11.14 affects RHTPA 2.1.0, 2.1.1 (stream 2.1.x) and RHTPA 2.2.0, 2.2.1, 2.2.2 (stream 2.2.x). Versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14).
2. **Affects Versions correction**: RHTPA 2.0.0 (incorrect PSIRT assignment) corrected to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (scoped to 2.2.x stream).
3. **Triage outcome**: Remediation tasks created (Case A for 2.2.x, Case B preemptive for 2.1.x).
4. **Remediation tasks created**:
   - 2.2.x: upstream backport task + downstream propagation subtask (blocked by upstream)
   - 2.1.x: preemptive upstream backport task + preemptive downstream propagation subtask (security-preemptive, Related to TC-8001)
5. **Label added**: `ai-cve-triaged` on TC-8001
