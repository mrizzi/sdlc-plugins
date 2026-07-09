# Step 8 -- Remediation for TC-8060

CVE-2026-99010: h2 memory exhaustion via CONTINUATION frames

## Triage Outcome

**Case A: Affected -- create remediation tasks**

Versions 2.2.0, 2.2.1, and 2.2.2 in the scoped 2.2.x stream ship h2 0.4.4 (vulnerable, < 0.4.5). Versions 2.2.3 and 2.2.4 already ship h2 0.4.5 (fixed).

Cross-stream check (Case B): The 2.1.x stream is NOT affected (all versions ship h2 0.4.5). No cross-stream remediation tasks are needed.

## Ecosystem and Task Structure

Ecosystem: **Cargo** (source dependency)
Task structure: **Two tasks** -- upstream backport + downstream propagation

The vulnerable library h2 is a **transitive dependency** (3 levels deep: backend -> reqwest -> hyper -> h2). The remediation tasks use the two-tier remediation approach for transitive dependencies.

---

## Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-99010: bump h2 to 0.4.5 (2.2.x)
**Labels**: ai-generated-jira, Security, CVE-2026-99010
**Link**: Depend (inward: TC-8060, outward: this task)

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.5) must be updated to the fixed version (0.4.5+).

h2 is a **transitive dependency** pulled in through the following chain:
```
backend (workspace) -> reqwest -> hyper -> h2
```

Affected versions: 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (v0.4.8 retag)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/hyperium/h2/pull/800
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2, 3 levels deep)
- Profile: production (reqwest is a runtime dependency)

### Remediation approach (transitive dependency)

The vulnerable package h2 is a **transitive** dependency pulled in through reqwest -> hyper -> h2. Use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2: **reqwest** (version 0.12.5)
- Bump reqwest to a version whose transitive closure includes h2 >= 0.4.5
- Verify the bump does not introduce breaking API changes to reqwest
- After bumping, verify with `cargo tree -i h2` that h2 resolves to >= 0.4.5

**Fallback: pin the transitive dependency directly**
If bumping reqwest is not viable (breaking API changes, no release available with the fix):
- Run `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding the transitive resolution
- Document why the reqwest bump was not viable in the PR description

Note: The upstream branch release/0.4.z already contains h2 0.4.5 as of the commits backing versions 2.2.3+. The fix may already be present on the branch HEAD -- verify before creating a new PR.

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

**Summary**: Propagate CVE-2026-99010 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)
**Labels**: ai-generated-jira, Security, CVE-2026-99010
**Links**:
  - Depend (inward: TC-8060, outward: this task)
  - Blocks (inward: upstream task, outward: this task) -- blocked by upstream backport

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99010 fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.5 (via reqwest/hyper dependency chain) on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

Full dependency chain: backend -> reqwest -> hyper -> h2 (transitive, 3 levels deep)

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: transitive -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly as a transitive dependency override (fallback approach), verify the pinning is reflected in the downstream build's Cargo.lock after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8060 (parent tracking issue)

---

## Post-Triage Actions

1. **Add label**: `ai-cve-triaged` to TC-8060
2. **Post summary comment** to TC-8060 documenting:
   - Version impact table (2.2.0-2.2.2 affected, 2.2.3-2.2.4 not affected)
   - Dependency chain: backend -> reqwest -> hyper -> h2 (transitive, 3 levels deep)
   - Affects Versions correction: RHTPA 2.2.0 is correct (already set by PSIRT); versions 2.2.1 and 2.2.2 should also be added
   - Remediation tasks created: upstream backport + downstream propagation
   - Two-tier remediation approach for transitive dependency documented
   - @mention reporter psirt-analyst (557058:psirt-analyst-mock-id)
3. **Transition** TC-8060 to In Progress

## Affects Versions Correction (Step 3)

PSIRT set Affects Versions to: RHTPA 2.2.0
Version impact analysis shows affected: 2.2.0, 2.2.1, 2.2.2

Correction needed: Add RHTPA 2.2.1 and RHTPA 2.2.2 to Affects Versions (if these Jira versions exist). Versions 2.2.3 and 2.2.4 are NOT affected and should not be added.
