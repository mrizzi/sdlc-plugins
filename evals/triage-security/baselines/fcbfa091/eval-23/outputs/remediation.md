# Step 8 -- Remediation: TC-8001

## Triage Outcome

**Issue**: TC-8001 -- CVE-2026-31812 quinn-proto (scoped to 2.2.x stream)
**Ecosystem**: Cargo (source dependency) -- requires two tasks per stream: upstream backport + downstream propagation
**Deployment context**: customer-shipped

### Case A: Affected versions in scoped stream (2.2.x)

Versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable quinn-proto (< 0.11.14).
The fix was already picked up in 2.2.3+ (quinn-proto 0.11.14 via build 0.4.11).
The upstream branch `release/0.4.z` already contains the fix.

### Case B: Cross-stream impact (2.1.x)

All 2.1.x versions (2.1.0, 2.1.1) ship vulnerable quinn-proto 0.11.9.
No stream-specific CVE Jira exists for 2.1.x. Preemptive remediation tasks are required.

---

## Remediation Task 1: Upstream Backport (2.2.x stream)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812

### Repository

backend

### Target Branch

release/0.4.z

### Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5, quinn-proto 0.11.9), 2.2.1 (v0.4.8, quinn-proto 0.11.12), 2.2.2 (v0.4.9, retag of v0.4.8, quinn-proto 0.11.12)
Source commit(s): v0.4.5, v0.4.8

Note: The fix is already present in builds v0.4.11+ (quinn-proto 0.11.14), which shipped in versions 2.2.3 and 2.2.4. This task formalizes the remediation for advisory tracking.

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

### Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

#### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

### Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

### Test Requirements

- [ ] Existing test suite passes with the updated dependency

### Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Remediation Task 2: Downstream Propagation (2.2.x stream)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812

### Repository

rhtpa-release.0.4.z

### Target Branch

main

### Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

Note: Builds 0.4.11+ already include quinn-proto 0.11.14. This task ensures the reference is formally tracked for advisory purposes.

### Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

#### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

### Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

### Test Requirements

- [ ] Container image builds successfully with the updated reference

### Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Remediation Task 3: Upstream Backport -- Preemptive (2.1.x stream)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

### Repository

backend

### Target Branch

release/0.3.z

### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8, quinn-proto 0.11.9), 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

### Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

#### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

### Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

### Test Requirements

- [ ] Existing test suite passes with the updated dependency

### Dependencies

- Related to: TC-8001 (originating CVE from 2.2.x stream -- preemptive)

---

## Remediation Task 4: Downstream Propagation -- Preemptive (2.1.x stream)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

### Repository

rhtpa-release.0.3.z

### Target Branch

main

### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

### Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

#### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

### Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

### Test Requirements

- [ ] Container image builds successfully with the updated reference

### Dependencies

- Depends on: upstream backport preemptive task for 2.1.x (upstream backport must merge first)
- Related to: TC-8001 (originating CVE from 2.2.x stream -- preemptive)

---

## Jira Linkage Summary

### Standard remediation (2.2.x -- scoped stream)
- Upstream backport task -> TC-8001 via "Depend" link
- Downstream propagation subtask -> upstream backport task via "Blocks" link
- Downstream propagation subtask -> TC-8001 via "Depend" link

### Preemptive remediation (2.1.x -- cross-stream)
- Upstream backport preemptive task -> TC-8001 via "Related" link
- Downstream propagation preemptive subtask -> upstream backport preemptive task via "Blocks" link
- Downstream propagation preemptive subtask -> TC-8001 via "Related" link

## Cross-Stream Impact Comment

To be posted on TC-8001:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis.
> All 2.1.x versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9.
> No stream-specific CVE Jira exists for 2.1.x.
>
> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: upstream backport task + downstream propagation task (security-preemptive)
>
> These tasks use the "Related" link type and carry the security-preemptive
> label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
> reconciliation will link them and remove the label.
