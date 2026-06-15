# Step 7: Remediation Tasks

## Triage Decision

**Case A — Remediation Required**: The 2.1.x stream is affected (ships h2 < 0.4.8). The 2.2.x stream already ships the patched version (h2 >= 0.4.8) and requires no action.

**Ecosystem**: Cargo (source dependency) — create two tasks: upstream backport + downstream propagation.

**Streams requiring remediation**: 2.1.x only.

No cross-stream impact notice is needed because the issue is UNSCOPED — it already covers all streams by definition.

---

## Task 1: Upstream Backport (2.1.x)

**Proposed Jira summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

### Task Description

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: memory exhaustion via CONTINUATION frames in h2.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.1.0 (tag v0.3.8), 2.1.1 (tag v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: [hyperium/h2#812](https://github.com/hyperium/h2/pull/812)
Advisory: [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7)

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)

---

## Task 2: Downstream Propagation (2.1.x)

**Proposed Jira summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

**Blocked by**: Task 1 (upstream backport)

### Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)

---

## Jira Linkage Plan

1. Link Task 1 (upstream backport) to TC-8004 with link type "Depend"
2. Link Task 2 (downstream propagation) to TC-8004 with link type "Depend"
3. Link Task 2 as blocked by Task 1 with link type "Blocks"
4. Transition TC-8004 to In Progress
5. Assign TC-8004 to the current user

## Note on 2.2.x Stream

No remediation tasks are created for the 2.2.x stream. All 2.2.x versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8, which is the fixed version. The vulnerability does not affect this stream.
