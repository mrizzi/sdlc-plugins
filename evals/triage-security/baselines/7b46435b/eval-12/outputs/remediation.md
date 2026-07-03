# Step 8 -- Remediation

## Scoped Stream 2.2.x: Case C -- Close as Not a Bug

No supported versions in the scoped stream 2.2.x ship a vulnerable version of h2.
All versions ship h2 >= 0.4.8 (the fix threshold from Step 1.5 enrichment).

### Recommendation

Close TC-8030 as **Not a Bug** (not affected).

**Proposed Jira actions (pending engineer confirmation):**

1. Add comment to TC-8030:

   > No supported versions in stream 2.2.x ship a vulnerable version of h2.
   > Version impact analysis shows all 2.2.x versions ship h2 >= 0.4.8,
   > which is at or above the fix threshold.
   >
   > | Version | h2 Version | Affected? |
   > |---------|------------|-----------|
   > | 2.2.0 | 0.4.8 | NO |
   > | 2.2.1 | 0.4.8 | NO |
   > | 2.2.2 | 0.4.8 | NO (retag of 2.2.1) |
   > | 2.2.3 | 0.4.9 | NO |
   > | 2.2.4 | 0.4.9 | NO |
   >
   > Fix threshold determined via external CVE data enrichment:
   > MITRE CVE API (lessThan 0.4.8) and OSV.dev (fixed 0.4.8) agree.
   > Jira description was imprecise ("versions prior to the fix").

2. Transition TC-8030 to **Closed** with resolution **Not a Bug**.

3. Set VEX Justification (customfield_12345) to **Component not Present** --
   the vulnerable version of h2 (< 0.4.8) is not shipped in any 2.2.x version.
   All versions ship h2 at the fix threshold or above.

4. Add label `ai-cve-triaged` to TC-8030.

## Cross-Stream Impact: Case B -- Stream 2.1.x Affected

The cross-stream version impact analysis reveals that stream **2.1.x** ships
h2 0.4.5, which is below the fix threshold of 0.4.8. Both versions (2.1.0 and
2.1.1) are affected.

### Cross-Stream Impact Comment

Proposed comment on TC-8030:

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock
> file analysis. Versions 2.1.0 and 2.1.1 both ship h2 0.4.5.
> This stream is tracked by a companion issue (see Related links)
> or may require separate PSIRT triage.

### Preemptive Remediation Tasks for Stream 2.1.x

If no companion CVE Jira exists for CVE-2026-48901 in stream 2.1.x (verified
via Step 4 JQL search), create preemptive remediation tasks:

#### Task 1: Upstream Backport (Preemptive)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

**Link**: Related to TC-8030 (originating CVE Jira, different stream)

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version
(0.4.8+).

Affected versions: 2.1.0 (h2 0.4.5), 2.1.1 (h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (parent tracking issue)

---

#### Task 2: Downstream Propagation (Preemptive)

**Summary**: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

**Link**: Related to TC-8030; Blocks relationship with upstream task

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-48901
fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8030 (parent tracking issue)
