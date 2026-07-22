# Step 8 -- Remediation

## Triage Outcome

### Issue Scope: 2.2.x stream

**No supported versions in the 2.2.x stream are affected.**

All versions in the issue's scoped stream (2.2.x) ship h2 >= 0.4.8, which is at
or above the fix threshold. The version impact table shows NO for every 2.2.x version.

### Case C: Close as Not a Bug (for the 2.2.x scope)

**Recommendation**: Close TC-8030 as Not a Bug (not affected).

**Rationale**: No supported versions in the 2.2.x stream ship a vulnerable version
of h2. Version impact analysis confirms all 2.2.x versions (2.2.0 through 2.2.4)
include h2 >= 0.4.8, which is at or above the CVE-2026-48901 fix threshold.

**VEX Justification**: Component not Present (the vulnerable version of h2 is not
shipped in any 2.2.x version). The VEX Justification custom field
(customfield_12345) would be set to "Component not Present".

**Jira close comment** (would be posted to TC-8030):

> No supported versions in the 2.2.x stream ship a vulnerable version of h2.
> Version impact analysis:
>
> | Version | h2 version | Affected? |
> |---------|------------|-----------|
> | 2.2.0 | 0.4.8 | NO |
> | 2.2.1 | 0.4.8 | NO |
> | 2.2.2 | -- | NO (retag of 2.2.1) |
> | 2.2.3 | 0.4.9 | NO |
> | 2.2.4 | 0.4.9 | NO |
>
> All 2.2.x versions ship h2 >= 0.4.8, which is outside the affected range (< 0.4.8).
> Enriched fix threshold from MITRE CVE API and OSV.dev (cross-validated).
>
> Closing as Not a Bug with VEX Justification: Component not Present.

---

## Case B: Cross-Stream Impact

The version impact analysis reveals that the **2.1.x stream** (outside the issue's
2.2.x scope) IS affected:

| Stream | Version | h2 version | Affected? |
|--------|---------|------------|-----------|
| 2.1.x | 2.1.0 | 0.4.5 | **YES** |
| 2.1.x | 2.1.1 | 0.4.5 | **YES** |

**Cross-stream impact comment** (would be posted to TC-8030):

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file
> analysis. Both 2.1.0 and 2.1.1 ship h2 0.4.5 which is below the fix threshold.
> This stream is tracked by companion issues (see Related links) or may require
> separate PSIRT triage.

### Preemptive Remediation Tasks for 2.1.x

Since the 2.1.x stream is affected and (assuming) has no existing CVE Jira for
CVE-2026-48901, preemptive remediation tasks would be created with the
`security-preemptive` label and "Related" link type.

#### Task 1: Upstream Backport (Preemptive -- 2.1.x)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link**: Related to TC-8030 (originating CVE Jira, different stream)

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

## Repository

backend (rhtpa-backend)

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: source dependency (Cargo)
- Update h2 dependency to >= 0.4.8 in Cargo.toml / Cargo.lock

### Remediation approach

Update h2 to >= 0.4.8 in the Cargo workspace. Run `cargo update -p h2` or
explicitly set the version constraint in Cargo.toml to `>= 0.4.8`.

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

- Related to: TC-8030 (originating CVE Jira for stream 2.2.x)

---

#### Task 2: Downstream Propagation (Preemptive -- 2.1.x)

**Summary**: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`

**Link**: Related to TC-8030; Blocked by upstream backport task above

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-48901
fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges,
update the source pinning in this Konflux release repo so the next build ships
the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
- **Dependency type**: source dependency (Cargo) -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the h2 >= 0.4.8 fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: upstream backport task (upstream fix must merge first)
- Related to: TC-8030 (originating CVE Jira for stream 2.2.x)

---

## Post-Triage Summary

**Triage outcome for TC-8030 (CVE-2026-48901, h2 HTTP/2 CONTINUATION flood)**:

1. **Version impact**: No 2.2.x versions are affected (all ship h2 >= 0.4.8).
   The 2.1.x stream (outside issue scope) IS affected (ships h2 0.4.5).
2. **Affects Versions correction**: The PSIRT-assigned "RHTPA 2.2.0" would be
   removed since 2.2.0 is not actually affected.
3. **Issue disposition**: Close TC-8030 as Not a Bug with VEX Justification
   "Component not Present" (for the 2.2.x scope).
4. **Cross-stream impact**: 2.1.x stream affected -- preemptive remediation
   tasks created (upstream backport + downstream propagation) with
   `security-preemptive` label and "Related" link to TC-8030.
5. **Label**: `ai-cve-triaged` would be added to TC-8030.
