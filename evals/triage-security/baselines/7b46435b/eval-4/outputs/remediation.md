# Remediation — TC-8004 (CVE-2026-33501)

## Triage Outcome

**Case A: Affected -- create remediation tasks** for the 2.1.x stream only.

The 2.2.x stream is NOT affected (all versions ship h2 >= 0.4.8), so no remediation tasks are created for that stream.

## Sibling Check

JQL search for sibling Vulnerability issues with CVE-2026-33501 label returned empty. No duplicates or companion issues exist.

## Remediation Tasks (2.1.x stream only)

Since h2 is a **Cargo** (source dependency) ecosystem package, two tasks are required for the affected 2.1.x stream:

### Task 1: Upstream Backport

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

#### Repository

backend

#### Target Branch

release/0.3.z

#### Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (build v0.3.8), RHTPA 2.1.1 (build v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

#### Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

##### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

#### Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

#### Test Requirements

- [ ] Existing test suite passes with the updated dependency

#### Dependencies

- Depends on: TC-8004 (parent tracking issue)

---

### Task 2: Downstream Propagation

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

#### Repository

rhtpa-release.0.3.z

#### Target Branch

main

#### Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges,
update the source pinning in this Konflux release repo so the next build ships the fix.

#### Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

#### Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

#### Test Requirements

- [ ] Container image builds successfully with the updated reference

#### Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)

---

## Jira Linkage Plan

1. Link upstream backport task to TC-8004 with "Depend" link type
2. Link downstream propagation task to TC-8004 with "Depend" link type
3. Link downstream propagation task as blocked by upstream backport task with "Blocks" link type
4. Transition TC-8004 to In Progress
5. Assign TC-8004 to current user
6. Add ai-cve-triaged label to TC-8004

## 2.2.x Stream -- No Action Required

The 2.2.x stream requires no remediation. All versions in this stream ship h2 >= 0.4.8 (the fix version):

| Version | h2 version | Status |
|---------|------------|--------|
| 2.2.0 | 0.4.8 | Fixed |
| 2.2.1 | 0.4.8 | Fixed |
| 2.2.2 | (retag of 2.2.1) | Fixed |
| 2.2.3 | 0.4.9 | Fixed |
| 2.2.4 | 0.4.9 | Fixed |

No cross-stream impact notice is needed because the 2.2.x stream is already patched. No preemptive tasks are needed (Case B does not apply -- the other stream is not affected).

## Post-Triage Summary

CVE-2026-33501 (h2 memory exhaustion via CONTINUATION frames) affects only the 2.1.x stream. All 2.1.x versions (2.1.0, 2.1.1) ship h2 0.4.5, which is vulnerable (< 0.4.8). The 2.2.x stream is unaffected -- all versions ship h2 >= 0.4.8.

Affects Versions corrected from [RHTPA 2.1.0, RHTPA 2.2.0] to [RHTPA 2.1.0, RHTPA 2.1.1].

Two remediation tasks created for the 2.1.x stream:
1. Upstream backport: bump h2 to >= 0.4.8 on release/0.3.z in backend repo
2. Downstream propagation: update backend ref in rhtpa-release.0.3.z
