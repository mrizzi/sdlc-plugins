# Step 7 -- Remediation: CVE-2026-48901

## Triage Outcome

### Scoped Stream (2.2.x)

The version impact analysis shows that only **2.2.0** is affected within the scoped 2.2.x stream. All current versions (2.2.1 through 2.2.4) already ship h2 >= 0.4.8 and are NOT affected. The fix was incorporated through a routine dependency update in build v0.4.8 (product version 2.2.1, released 2026-02-05).

**Recommendation**: The 2.2.x stream's current versions are not affected. The only affected version (2.2.0) has been superseded by 2.2.1+, which include the fix. Affects Versions should be corrected to reflect that only RHTPA 2.2.0 is affected (not the broader "RHTPA 2.2.0" that PSIRT assigned, which could imply the entire stream).

Since all currently supported versions in the 2.2.x stream (2.2.1+) already contain the fix, no remediation tasks are needed for this stream. The Affects Versions correction and the cross-stream notice (below) are the primary actions.

### Cross-Stream Impact (2.1.x -- Case B)

The 2.1.x stream is **fully affected**: both 2.1.0 and 2.1.1 ship h2 0.4.5, which is below the fix threshold of 0.4.8. No build in the 2.1.x stream includes the fix.

**Cross-stream impact comment** (to be posted on TC-8030):

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis. All versions in the 2.1.x stream (2.1.0, 2.1.1) ship h2 0.4.5. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

## Remediation Tasks

### Task 1: Upstream Backport -- Bump h2 in backend for 2.1.x stream

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

**Link type**: Related (to TC-8030 -- preemptive, since 2.1.x is outside the issue's scoped stream)

#### Task Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.1.0 (build v0.3.8), 2.1.1 (build v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock (and Cargo.toml if directly specified)
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (parent tracking issue)

---

### Task 2: Downstream Propagation -- Update backend ref in Konflux release repo (2.1.x)

**Summary**: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

**Link type**: Related (to TC-8030), Blocks (blocked by Task 1)

#### Task Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to >= 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

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

---

## Post-Triage Actions Summary

1. **Affects Versions correction**: Verify RHTPA 2.2.0 is correct (only 2.2.0 affected in 2.2.x stream; 2.2.1+ already fixed)
2. **Cross-stream impact comment**: Post notice to TC-8030 about 2.1.x stream impact
3. **Preemptive remediation tasks**: Create 2 tasks for 2.1.x stream (upstream backport + downstream propagation) with `security-preemptive` label and "Related" link to TC-8030
4. **Label**: Add `ai-cve-triaged` to TC-8030
5. **Post-triage summary comment**: Document version impact table, Affects Versions status, triage outcome, and links to remediation tasks on TC-8030
