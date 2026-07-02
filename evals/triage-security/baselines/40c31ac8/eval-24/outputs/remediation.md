# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

- **Issue stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Ecosystem**: Cargo (source dependency -- two tasks per stream: upstream backport + downstream propagation)
- **Affected versions in-scope (2.2.x)**: 2.2.0, 2.2.1, 2.2.2
- **Already fixed in-scope**: 2.2.3, 2.2.4 (ship quinn-proto 0.11.14)
- **Cross-stream impact (2.1.x)**: 2.1.0, 2.1.1 both affected

**Case A** applies: supported versions within the scoped stream (2.2.x) are affected.
**Case B** applies: stream 2.1.x is also affected (outside this issue's scope).

No Deployment Context column in Source Repositories -- coordination guidance omitted from all task descriptions.

---

## Case A: Remediation Tasks for Stream 2.2.x (Scoped Stream)

### Task 1: Upstream Backport Task (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (retag of v0.4.8)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

Note: The upstream branch release/0.4.z already has the fix as of v0.4.11
(quinn-proto 0.11.14). Versions 2.2.3+ already ship the fixed dependency.
Verify that no further action is needed on this branch.

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

### Task 2: Downstream Propagation Task (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

Note: Versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already reference
commits that include quinn-proto 0.11.14. This propagation may already
be complete. Verify current state before making changes.

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

## Case B: Preemptive Remediation Tasks for Stream 2.1.x (Cross-Stream)

These tasks are created proactively because the cross-stream impact analysis
found that stream 2.1.x is affected but has no stream-specific CVE Jira.

### Task 3: Preemptive Upstream Backport Task (2.1.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001, not Depend -- originating CVE belongs to a different stream)

**Description**:

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

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

The upstream branch release/0.3.z does NOT currently have the fix.
The latest pinned tag (v0.3.12) ships quinn-proto 0.11.9.
An upstream PR is required to bump quinn-proto to >= 0.11.14 on this branch.

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

- Depends on: TC-8001 (parent tracking issue, cross-stream -- Related link)

---

### Task 4: Preemptive Downstream Propagation Task (2.1.x)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001, not Depend -- originating CVE belongs to a different stream)

**Description**:

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

The upstream backport bumps quinn-proto to 0.11.14 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

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
- Depends on: TC-8001 (parent tracking issue, cross-stream -- Related link)

---

## Jira Linkage Summary

### Standard remediation (2.2.x -- Case A):
- Upstream backport task --> TC-8001: link type **Depend**
- Downstream propagation task --> upstream backport task: link type **Blocks**
- Downstream propagation task --> TC-8001: link type **Depend**

### Preemptive remediation (2.1.x -- Case B):
- Preemptive upstream backport task --> TC-8001: link type **Related**
- Preemptive downstream propagation task --> preemptive upstream backport task: link type **Blocks**
- Preemptive downstream propagation task --> TC-8001: link type **Related**

## Post-Triage Actions

1. Add label `ai-cve-triaged` to TC-8001
2. Post summary comment to TC-8001 with:
   - Version impact table
   - Affects Versions correction: `[RHTPA 2.0.0]` --> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
   - Remediation tasks created (upstream + downstream for 2.2.x, preemptive for 2.1.x)
   - Cross-stream impact notice for 2.1.x
   - @mention of the issue reporter
3. Post cross-stream impact comment noting 2.1.x is also affected
4. Post preemptive task comment listing tasks created for 2.1.x
