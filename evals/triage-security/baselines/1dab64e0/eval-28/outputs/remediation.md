# Step 8 -- Remediation

## Triage Outcome

**Case A: Affected -- create remediation tasks**

The 2.2.x stream has affected versions (2.2.0, 2.2.1, 2.2.2). The 2.1.x stream is NOT affected (h2 0.4.5 in all versions), so no cross-stream impact (Case B does not apply).

Since h2 is a **Cargo** source dependency, two tasks are required:
1. Upstream backport task (fix in the source repo)
2. Downstream propagation subtask (update the reference in the Konflux release repo)

Since h2 is a **transitive** dependency (3 levels deep: reqwest -> hyper -> h2), the remediation tasks use the **two-tier remediation approach**.

---

## Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-99010: bump h2 to 0.4.5 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: h2 - Memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.5) must be updated to the fixed version (0.4.5+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is a retag of v0.4.8)

Upstream fix: https://github.com/hyperium/h2/pull/800
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2)
- **Dependency chain**: h2 is NOT a direct dependency of the backend workspace. It is pulled in transitively through 3 levels: `reqwest` (direct dep) -> `hyper` -> `h2`.

### Remediation approach (transitive dependency)

The vulnerable package h2 is a **transitive** dependency pulled in through intermediate packages. Use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2: `reqwest` (version 0.12.5)
- Bump `reqwest` to a version whose transitive closure includes h2 >= 0.4.5
- The dependency chain is: reqwest -> hyper -> h2
- Verify the bump does not introduce breaking API changes to reqwest
- Check reqwest release notes for a version that ships with h2 >= 0.4.5

**Fallback: pin the transitive dependency directly**
If bumping reqwest is not viable (breaking API changes, no release available with the fix):
- Cargo: `cargo add h2@0.4.5` to add as a direct dependency, overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

**Note**: The upstream branch `release/0.4.z` already contains commits (v0.4.11, v0.4.12) with h2 0.4.5. The fix may already be present at branch HEAD. Verify before creating a new commit.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)

---

## Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-99010 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99010 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.5 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2) -- carried forward from upstream task
- **Dependency chain**: h2 is a transitive dependency pulled in through reqwest -> hyper -> h2. The upstream task bumps h2 to >= 0.4.5 by either bumping reqwest or pinning h2 directly.
- Update the rhtpa-backend reference to the merged commit or new release tag that includes h2 >= 0.4.5
- If the upstream fix pinned h2 directly (fallback approach), verify the pinning is reflected in the downstream build's Cargo.lock after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image
- [ ] Rebuilt container image contains h2 >= 0.4.5

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8060 (parent tracking issue)

---

## Jira Linkage Plan

1. Link upstream backport task to TC-8060 with link type "Depend"
2. Link downstream propagation subtask to TC-8060 with link type "Depend"
3. Link downstream propagation subtask as blocked by upstream backport task with link type "Blocks"
4. Transition TC-8060 to In Progress
5. Add `ai-cve-triaged` label to TC-8060

## Post-Triage Summary Comment

Version impact analysis for CVE-2026-99010 (h2 < 0.4.5):

| Version | h2 version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.2.0 | 0.4.4 | YES | |
| 2.2.1 | 0.4.4 | YES | |
| 2.2.2 | 0.4.4 | YES | retag of 2.2.1 |
| 2.2.3 | 0.4.5 | NO | fixed |
| 2.2.4 | 0.4.5 | NO | fixed |

Dependency chain: backend -> reqwest -> hyper -> h2 (transitive, 3 levels deep)

Affects Versions correction: [RHTPA 2.2.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

Remediation tasks created:
- Upstream backport task: bump h2 to 0.4.5 (rhtpa-2.2)
- Downstream propagation task: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2), blocked by upstream task

Cross-stream check: 2.1.x stream is NOT affected (all versions ship h2 0.4.5).

@psirt-analyst (557058:psirt-analyst-mock-id)
