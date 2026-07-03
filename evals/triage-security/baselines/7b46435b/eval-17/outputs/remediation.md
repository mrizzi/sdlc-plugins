# Step 8 -- Remediation

## Triage Outcome

### Stream 2.2.x (scoped stream) -- Already Fixed in Latest

The 2.2.x stream's latest versions (2.2.3 and 2.2.4) already ship quinn-proto 0.11.14,
which is the fixed version. The upstream branch `release/0.4.z` already contains the fix.
No remediation tasks are needed for this stream.

- Affected historical versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- Fix incorporated in: RHTPA 2.2.3 (build 0.4.11, shipped 2026-03-23)
- Action: Correct Affects Versions and document the already-fixed status

### Stream 2.1.x (cross-stream) -- Case B: Preemptive Remediation

All versions in the 2.1.x stream ship vulnerable quinn-proto 0.11.9. No fix exists
on the upstream branch `release/0.3.z`. Since this issue is scoped to 2.2.x and there
is no separate CVE Jira for the 2.1.x stream, preemptive remediation tasks are created
per Case B.

## Remediation Tasks

### Task 1: Upstream Backport (2.1.x stream -- preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Link**: Related to TC-8001 (originating CVE Jira, different stream)

#### Task Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
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

- Depends on: TC-8001 (parent tracking issue)

---

### Task 2: Downstream Propagation (2.1.x stream -- preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive

**Link**: Related to TC-8001 (originating CVE Jira, different stream)

**Blocked by**: Task 1 (upstream backport must merge first)

#### Task Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., `v0.3.12`)
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

## Post-Triage Summary (proposed Jira comment for TC-8001)

### Version Impact

| Stream | Version | quinn-proto | Affected? |
|--------|---------|-------------|-----------|
| 2.2.x | 2.2.0 | 0.11.9 | Yes |
| 2.2.x | 2.2.1 | 0.11.12 | Yes |
| 2.2.x | 2.2.2 | 0.11.12 | Yes (retag of 2.2.1) |
| 2.2.x | 2.2.3 | 0.11.14 | No (fixed) |
| 2.2.x | 2.2.4 | 0.11.14 | No (fixed) |
| 2.1.x | 2.1.0 | 0.11.9 | Yes |
| 2.1.x | 2.1.1 | 0.11.9 | Yes |

### Affects Versions Correction

- Removed: RHTPA 2.0.0 (no corresponding version stream)
- Added: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

### Triage Outcome

- **2.2.x stream**: Already fixed in 2.2.3+ (quinn-proto 0.11.14). No remediation tasks needed.
- **2.1.x stream**: Cross-stream impact detected. All versions ship vulnerable quinn-proto 0.11.9.
  Preemptive remediation tasks created (security-preemptive label, Related link to TC-8001).

### Cross-Stream Impact Comment

Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file
analysis. Stream 2.1.x has no companion CVE Jira. Preemptive remediation tasks created.

### Preemptive Tasks Created

- 2.1.x: upstream backport task (security-preemptive) -- bump quinn-proto to 0.11.14 on release/0.3.z
- 2.1.x: downstream propagation task (security-preemptive) -- update backend ref in rhtpa-release.0.3.z

### Proposed Actions

All actions below are presented as proposals for engineer confirmation before execution:

1. **Affects Versions correction**: Replace RHTPA 2.0.0 with RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
2. **Add label**: ai-cve-triaged
3. **Post comment**: Post-triage summary comment with version impact table and triage outcome
4. **Create preemptive tasks**: Two remediation tasks for 2.1.x stream (upstream backport + downstream propagation) with security-preemptive label and Related link to TC-8001
