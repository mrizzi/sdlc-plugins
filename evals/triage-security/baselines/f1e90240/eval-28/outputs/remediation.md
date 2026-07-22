# Step 8 — Remediation: CVE-2026-99010 (h2)

## Triage Outcome

**Case A: Affected** — versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship h2 0.4.4, which is within the affected range (< 0.4.5). Remediation tasks are required.

**Cross-stream (Case B)**: Not applicable — the 2.1.x stream ships h2 0.4.5 and is NOT affected. No cross-stream impact notice or preemptive tasks needed.

## Ecosystem: Cargo (source dependency)

Since h2 is a Cargo (source-level) dependency, two remediation tasks are created:

1. **Upstream backport task** — fix in the source repo (rhtpa-backend)
2. **Downstream propagation subtask** — update the source reference in the Konflux release repo (rhtpa-release.0.4.z)

## Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-99010: bump h2 to 0.4.5 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99010: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.5) must be updated to the fixed version (0.4.5+).

h2 is a **transitive dependency** (3 levels deep) pulled in through the following chain:

```
backend (workspace) -> reqwest 0.12.5 -> hyper 1.4.1 -> h2 0.4.4
```

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1), v0.4.9 (2.2.2, retag of 2.2.1)

Upstream fix: https://github.com/hyperium/h2/pull/800
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99010

## Implementation Notes

- Target branch: `release/0.4.z`
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2)
- h2 is NOT a direct dependency -- it enters through `reqwest = { version = "0.12", features = ["json"] }` in backend/Cargo.toml

### Remediation approach (transitive dependency)

The vulnerable package h2 is a **transitive** dependency pulled in through intermediate packages (reqwest -> hyper -> h2). Use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2: **reqwest** (version 0.12.5)
- Bump reqwest to a version whose transitive closure includes h2 >= 0.4.5
- Check reqwest's Cargo.lock or dependency tree to verify which reqwest version resolves h2 >= 0.4.5
- Verify the bump does not introduce breaking API changes to reqwest

**Fallback: pin the transitive dependency directly**
If bumping reqwest is not viable (breaking API changes, no reqwest release available with h2 >= 0.4.5):
- Run `cargo add h2@0.4.5` to add h2 as a direct dependency, overriding the transitive resolution
- Document why the reqwest bump was not viable in the PR description
- This approach adds h2 to the direct dependencies in Cargo.toml, which should be noted for future dependency maintenance

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.5 (verify via `cargo tree -p h2`)
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8060 (parent tracking issue)

---

## Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-99010 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99010`

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99010 fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.5 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- **Dependency type**: transitive (chain: backend -> reqwest -> hyper -> h2) -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag that includes h2 >= 0.4.5
- If the upstream fix pinned h2 directly as a transitive dependency override (fallback approach), verify the pinning is reflected in the downstream build's Cargo.lock after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the h2 >= 0.4.5 fix
- [ ] Konflux rebuild triggers new container image
- [ ] New container image ships h2 >= 0.4.5

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8060 (parent tracking issue)

---

## Jira Linkage Plan

After creating both tasks:

1. **Link upstream task** to TC-8060:
   - Link type: "Depend" (TC-8060 -> upstream task)

2. **Link downstream subtask** as blocked by upstream task:
   - Link type: "Blocks" (upstream task -> downstream task)

3. **Link downstream subtask** to TC-8060:
   - Link type: "Depend" (TC-8060 -> downstream task)

4. **Transition** TC-8060 to In Progress

5. **Post summary comment** to TC-8060 listing both created tasks:
   > Remediation tasks created:
   > - [upstream-task-key] (upstream backport: bump h2 to 0.4.5 via reqwest in rhtpa-backend on release/0.4.z)
   > - [downstream-task-key] (downstream propagation: update rhtpa-backend ref in rhtpa-release.0.4.z, blocked by [upstream-task-key])
   >
   > Dependency chain: backend -> reqwest -> hyper -> h2 (transitive, 3 levels deep)
   > Remediation approach: two-tier (prefer bumping reqwest; fall back to pinning h2 directly)

6. **Add label** `ai-cve-triaged` to TC-8060
