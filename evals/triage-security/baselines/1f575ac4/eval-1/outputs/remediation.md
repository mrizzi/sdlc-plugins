# Step 7 -- Remediation

## Triage Outcome

**Case A + Case B**: The issue's scoped stream (2.2.x) has affected versions (2.2.0, 2.2.1, 2.2.2), so remediation tasks are needed. Additionally, the 2.1.x stream is also affected (cross-stream impact), triggering Case B proactive remediation.

The ecosystem is **Cargo** (source dependency), so **two tasks** are created per affected stream: an upstream backport task and a downstream propagation subtask.

However, the upstream branch for 2.2.x (`release/0.4.z`) already has the fix (quinn-proto 0.11.14 at tag v0.4.11+), so the 2.2.x stream only needs a downstream propagation task -- the upstream fix already exists.

---

## Task 1: Downstream Propagation for 2.2.x Stream (Scoped -- Case A)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-31812 fix.

The upstream branch release/0.4.z already ships quinn-proto 0.11.14 (the fixed version) as of tag v0.4.11. The affected product versions (2.2.0, 2.2.1, 2.2.2) were built from earlier tags (v0.4.5, v0.4.8, v0.4.9) that shipped vulnerable quinn-proto versions (0.11.9, 0.11.12). Since v0.4.11+ already includes the fix, no upstream backport is needed -- only a downstream reference update to ensure future rebuilds of the affected versions pick up the patched dependency.

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (v0.4.9, retag of 2.2.1)

Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq
Upstream fix PR: https://github.com/quinn-rs/quinn/pull/2048

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- Update the backend reference to tag v0.4.11 or later (which includes quinn-proto 0.11.14)
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to a tag that includes quinn-proto >= 0.11.14
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Task 2: Upstream Backport for 2.1.x Stream (Cross-stream -- Case B Preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001, since this is a preemptive task for a different stream)

### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8, quinn-proto 0.11.9), RHTPA 2.1.1 (v0.3.12, quinn-proto 0.11.9)
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

- Depends on: TC-8001 (parent tracking issue -- Related link, cross-stream)

---

## Task 3: Downstream Propagation for 2.1.x Stream (Cross-stream -- Case B Preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link type**: Related (to TC-8001, since this is a preemptive task for a different stream)

**Blocked by**: Task 2 (upstream backport for 2.1.x must merge first)

### Description

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

The upstream backport task bumps quinn-proto to 0.11.14
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

- Depends on: Task 2 (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue -- Related link, cross-stream)

---

## Jira Operations Summary

### For 2.2.x stream (scoped -- Case A):
1. Create downstream propagation task (Task 1)
2. Link Task 1 to TC-8001 with "Depend" link type
3. Post description digest comment on Task 1

### For 2.1.x stream (cross-stream -- Case B preemptive):
1. Create upstream backport task (Task 2) with `security-preemptive` label
2. Create downstream propagation task (Task 3) with `security-preemptive` label
3. Link Task 2 to TC-8001 with "Related" link type (preemptive)
4. Link Task 3 to TC-8001 with "Related" link type (preemptive)
5. Link Task 3 as "Blocks" by Task 2 (downstream blocked by upstream)
6. Post description digest comments on both tasks
7. Post cross-stream impact comment on TC-8001:
   "Preemptive remediation tasks created for streams without CVE Jiras:
   - 2.1.x: Task 2 (upstream backport, security-preemptive), Task 3 (downstream propagation, security-preemptive)"

### Post-triage:
1. Add `ai-cve-triaged` label to TC-8001
2. Post summary comment on TC-8001 with version impact table, Affects Versions correction, and links to all created tasks
3. Transition TC-8001 to In Progress
4. Assign TC-8001 to current user
