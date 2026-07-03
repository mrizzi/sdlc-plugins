# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome Summary

### Scoped Stream: 2.2.x

The 2.2.x stream has affected versions (2.2.0, 2.2.1, 2.2.2), but the fix is already present in the latest releases (2.2.3 and 2.2.4 ship quinn-proto 0.11.14). The upstream branch `release/0.4.z` already contains the fix. **No new remediation task is needed for the 2.2.x stream** -- the vulnerability was already remediated when quinn-proto was bumped to 0.11.14 in build v0.4.11 (shipped as version 2.2.3).

Affects Versions are corrected to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 for advisory tracking.

### Cross-Stream Impact: 2.1.x (Case B)

The 2.1.x stream is also affected. Both versions (2.1.0 and 2.1.1) ship quinn-proto 0.11.9, which is within the vulnerable range (< 0.11.14). The upstream branch `release/0.3.z` does NOT have the fix at HEAD.

No sibling CVE Jira exists for the 2.1.x stream, so **preemptive remediation tasks** are created below. These tasks carry the `security-preemptive` label and use "Related" link type to the originating CVE Jira TC-8001.

---

## Preemptive Remediation Tasks for 2.1.x Stream

### Task 1: Upstream Backport -- bump quinn-proto on release/0.3.z

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels:** ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Link:** Related to TC-8001

#### Task Description

## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

quinn-proto before version 0.11.14 allows a remote attacker to cause a panic by sending a QUIC transport frame that creates an excessive number of streams (denial of service).

Affected versions: 2.1.0 (build v0.3.8), 2.1.1 (build v0.3.12)
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

- Depends on: TC-8001 (parent tracking issue)

---

### Task 2: Downstream Propagation -- update backend ref in rhtpa-release.0.3.z

**Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels:** ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Link:** Related to TC-8001; Blocked by Task 1 (upstream backport)

#### Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
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

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
