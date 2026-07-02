# Remediation Tasks for TC-8001 (CVE-2026-31812)

## Triage Decision

### Scoped stream: 2.2.x

The fix for CVE-2026-31812 is already present in the 2.2.x stream. Versions 2.2.3 (build 0.4.11) and 2.2.4 (build 0.4.12) ship quinn-proto 0.11.14, which is the fixed version. No new remediation tasks are required for this stream.

The Affects Versions field should be corrected from `RHTPA 2.0.0` to `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2` to accurately reflect which shipped versions contained the vulnerable dependency.

### Cross-stream impact: 2.1.x (Case B — Preemptive Remediation)

All 2.1.x versions (2.1.0 and 2.1.1) ship quinn-proto 0.11.9, which is within the affected range (< 0.11.14). The upstream branch `release/0.3.z` does not yet carry the fix. No existing CVE Jira was found for the 2.1.x stream.

Two preemptive remediation tasks are created for the 2.1.x stream with the `security-preemptive` label, linked to TC-8001 via "Related" (not "Depend").

---

## Task 1: Upstream Backport (2.1.x — Preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related to TC-8001

### Description

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

The quinn-proto crate before version 0.11.14 allows a remote attacker to cause
a panic by sending a QUIC transport frame that creates an excessive number of
streams, resulting in a denial of service (DoS). CVSS: 7.5 (High).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8 (2.1.0), v0.3.12 (2.1.1)

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

## Task 2: Downstream Propagation (2.1.x — Preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related to TC-8001; Blocked by Task 1 (upstream backport)

### Description

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

The upstream backport bumps quinn-proto to 0.11.14
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

- Depends on: Task 1 (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Cross-Stream Impact Comment (for TC-8001)

The following comment would be posted to TC-8001:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis.
> Stream 2.1.x is not tracked by a companion CVE Jira.
>
> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: [upstream-task-key] (upstream backport, security-preemptive)
> - 2.1.x: [downstream-task-key] (downstream propagation, security-preemptive)
>
> These tasks use the "Related" link type and carry the security-preemptive
> label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
> reconciliation will link them and remove the label.

## Post-Triage Summary (for TC-8001)

> **Triage summary for CVE-2026-31812 (quinn-proto < 0.11.14)**
>
> **Version impact:**
>
> | Version | Stream | quinn-proto | Affected? | Notes |
> |---------|--------|-------------|-----------|-------|
> | 2.1.0 | 2.1.x | 0.11.9 | YES | |
> | 2.1.1 | 2.1.x | 0.11.9 | YES | |
> | 2.2.0 | 2.2.x | 0.11.9 | YES | |
> | 2.2.1 | 2.2.x | 0.11.12 | YES | |
> | 2.2.2 | 2.2.x | — | YES | retag of 2.2.1 |
> | 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
> | 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |
>
> **Affects Versions correction:**
> Changed from `[RHTPA 2.0.0]` to `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`.
> Based on lock file analysis at pinned commits from security-matrix.md.
> Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`.
>
> **Triage outcome:**
> - 2.2.x stream: Already fixed in 2.2.3+ (quinn-proto 0.11.14). No remediation tasks needed.
> - 2.1.x stream: Preemptive remediation tasks created (upstream backport + downstream propagation).
>
> **Remediation tasks created:**
> - [upstream-task-key] — Upstream backport: bump quinn-proto to 0.11.14 on release/0.3.z (2.1.x, security-preemptive)
> - [downstream-task-key] — Downstream propagation: update backend ref in rhtpa-release.0.3.z (2.1.x, security-preemptive, blocked by upstream task)
