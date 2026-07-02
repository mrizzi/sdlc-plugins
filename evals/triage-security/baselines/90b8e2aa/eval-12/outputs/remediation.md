# Step 8 -- Remediation

## Triage Outcome: Case C -- No Supported Versions Affected (in scope)

TC-8030 is scoped to stream **2.2.x** via the summary suffix `[rhtpa-2.2]`.

The version impact analysis (Step 2) shows that **no 2.2.x versions ship a vulnerable version of h2**. All 2.2.x versions include h2 >= 0.4.8, which is at or above the fix threshold established by external CVE data enrichment (Step 1.5).

### Close Recommendation

- **Resolution**: Not a Bug
- **VEX Justification**: Vulnerable Code not Present
  - Rationale: h2 is present in all 2.2.x versions (it is a Cargo dependency), but at version 0.4.8+, which includes the fix for CVE-2026-48901. The vulnerable code path (unbounded CONTINUATION frame handling) was fixed in h2 0.4.8. The vulnerable code is not present in the shipped versions.
- **Comment**: "No supported 2.2.x versions ship a vulnerable version of h2. Version impact analysis shows all 2.2.x releases include h2 >= 0.4.8 (fix threshold), with the earliest version (2.2.0) already shipping h2 0.4.8. CVE-2026-48901 does not affect the 2.2.x stream."
- **Label**: Add `ai-cve-triaged` to TC-8030

### Jira Actions (require engineer confirmation)

1. Set VEX Justification field (`customfield_12345`) to "Vulnerable Code not Present"
2. Transition TC-8030 to Closed with resolution "Not a Bug"
3. Add `ai-cve-triaged` label
4. Post summary comment with version impact table and @mention of the reporter

## Cross-Stream Impact: 2.1.x Stream Affected

The version impact analysis reveals that the **2.1.x stream** (outside this issue's scope) IS affected:

| Version | Build Tag | h2 Version | Affected? |
|---------|-----------|------------|-----------|
| 2.1.0 | v0.3.8 | 0.4.5 | **YES** |
| 2.1.1 | v0.3.12 | 0.4.5 | **YES** |

Both 2.1.x versions ship h2 0.4.5, which is below the fix threshold of 0.4.8.

### Remediation Tasks for 2.1.x Stream (Preemptive)

Since TC-8030 is scoped to 2.2.x and is being closed as Case C, remediation tasks for the 2.1.x stream would be created as **preemptive tasks** (Case B variant) if no companion CVE Jira exists for the 2.1.x stream. These tasks carry the `security-preemptive` label and use a "Related" link type to TC-8030.

#### Upstream Backport Task (preemptive)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.1)
**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive
**Link**: Related to TC-8030

```markdown
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
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
```

#### Downstream Propagation Subtask (preemptive)

**Summary**: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive
**Link**: Related to TC-8030; Blocks relationship with the upstream backport task

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges,
update the source pinning in this Konflux release repo so the next build ships the fix.

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
```

## Post-Triage Summary

### Actions for TC-8030 (2.2.x stream)
1. Close as "Not a Bug" -- no 2.2.x versions ship vulnerable h2
2. Set VEX Justification to "Vulnerable Code not Present"
3. Add `ai-cve-triaged` label
4. Post summary comment with version impact table

### Actions for 2.1.x stream (cross-stream impact)
1. Create preemptive upstream backport task (bump h2 to >= 0.4.8 on release/0.3.z)
2. Create preemptive downstream propagation subtask (update backend ref in rhtpa-release.0.3.z)
3. Both tasks linked as "Related" to TC-8030
4. Both tasks carry `security-preemptive` label
5. Post cross-stream impact comment on TC-8030
