# Step 8 -- Remediation

## Triage Outcome for TC-8030 (CVE-2026-48901, h2, stream 2.2.x)

### Case C: No supported versions affected in issue scope

The version impact analysis (Step 2) shows that **no 2.2.x versions** ship a vulnerable version of h2. All versions in the 2.2.x stream ship h2 >= 0.4.8 (the enriched fix threshold from Step 1.5).

**Recommendation**: Close TC-8030 as **Not a Bug** (not affected).

#### Close Actions (pending engineer confirmation)

1. **Add comment** to TC-8030:

   > No supported versions in the 2.2.x stream ship a vulnerable version of h2.
   > Version impact analysis shows all 2.2.x releases (2.2.0 through 2.2.4)
   > include h2 0.4.8 or later, which is at or above the fix threshold (< 0.4.8).
   >
   > | Version | h2 version | Affected? |
   > |---------|------------|-----------|
   > | 2.2.0 | 0.4.8 | NO |
   > | 2.2.1 | 0.4.8 | NO |
   > | 2.2.2 | -- | NO (retag of 2.2.1) |
   > | 2.2.3 | 0.4.9 | NO |
   > | 2.2.4 | 0.4.9 | NO |
   >
   > Fix threshold source: MITRE CVE API (lessThan 0.4.8) and OSV.dev (fixed 0.4.8), cross-validated.

2. **Transition** TC-8030 to Closed with resolution **Not a Bug**.

3. **VEX Justification**: Set `customfield_12345` to **Component not Present** -- the vulnerable version of h2 (< 0.4.8) is not included in any 2.2.x release. (Note: while the h2 crate is present, only the fixed version ships, so the vulnerable component version is not present.)

4. **Add label** `ai-cve-triaged` to TC-8030.

---

### Case B: Cross-stream impact -- 2.1.x stream is affected

The version impact analysis reveals that the **2.1.x stream** (outside this issue's scope) IS affected:

| Version | Build Tag | h2 version | Affected? |
|---------|-----------|------------|-----------|
| 2.1.0 | v0.3.8 | 0.4.5 | YES |
| 2.1.1 | v0.3.12 | 0.4.5 | YES |

#### Cross-stream impact comment (to be posted on TC-8030)

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file
> analysis. Both 2.1.0 (h2 0.4.5) and 2.1.1 (h2 0.4.5) ship a vulnerable version.
> This stream is tracked by a companion issue (see Related links) or may require
> separate PSIRT triage.

#### Preemptive remediation tasks (if no sibling CVE Jira exists for 2.1.x)

If no sibling Vulnerability issue with label `CVE-2026-48901` and stream suffix `[rhtpa-2.1]` exists, create preemptive remediation tasks for the 2.1.x stream:

##### Task 1: Upstream Backport (preemptive)

- **Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.1)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`
- **Link type**: Related (to TC-8030, not Depend, since TC-8030 belongs to a different stream)

**Description**:

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

Affected versions: 2.1.0 (h2 0.4.5), 2.1.1 (h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock (and Cargo.toml if directly specified)
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8030 (originating CVE Jira, different stream)

---

##### Task 2: Downstream Propagation (preemptive)

- **Summary**: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`
- **Link type**: Related (to TC-8030)
- **Blocked by**: upstream backport task (Task 1 above)

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

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

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

- Blocked by: upstream backport task (must merge first)
- Related to: TC-8030 (originating CVE Jira, different stream)
