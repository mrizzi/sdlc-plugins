# Step 7 -- Remediation

## Triage Outcome

The issue is scoped to the **2.2.x** stream. Within this stream:
- Versions 2.2.0, 2.2.1, 2.2.2 are **affected** (quinn-proto < 0.11.14)
- Versions 2.2.3, 2.2.4 are **not affected** (quinn-proto 0.11.14, the fixed version)

Since versions 2.2.3 and 2.2.4 already ship the fix, the vulnerability is **already fixed** in the latest releases of the 2.2.x stream. However, versions 2.2.0 through 2.2.2 remain affected.

Additionally, the **2.1.x stream** is also affected (cross-stream impact -- Case B).

## Case A -- Remediation Tasks for 2.2.x Stream (Scoped Stream)

Since the latest 2.2.x versions (2.2.3, 2.2.4) already ship quinn-proto 0.11.14 (the fixed version), no new remediation tasks are needed for the 2.2.x stream. The Affects Versions should be corrected to reflect that only 2.2.0, 2.2.1, and 2.2.2 were affected, and the fix was delivered in 2.2.3.

## Case B -- Cross-Stream Impact: 2.1.x Stream

The 2.1.x stream is affected (all versions ship quinn-proto 0.11.9), and this stream is outside the issue's scope. This triggers Case B (cross-stream impact).

### Cross-stream impact comment (to be posted on TC-8001):

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis:
- 2.1.0 (v0.3.8): quinn-proto 0.11.9
- 2.1.1 (v0.3.12): quinn-proto 0.11.9

This stream is tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

### Preemptive Remediation Tasks for 2.1.x Stream

Since no companion CVE Jira exists for the 2.1.x stream, create preemptive remediation tasks.

The ecosystem is **Cargo** (source dependency), so **two tasks** are needed:

#### Task 1: Upstream Backport Task (2.1.x)

- **Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Link type**: Related (to TC-8001)

**Description:**

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
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
```

#### Task 2: Downstream Propagation Subtask (2.1.x)

- **Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Link type**: Related (to TC-8001); Blocked by upstream backport task

**Description:**

```
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
- Depends on: TC-8001 (parent tracking issue)
```

## Post-Triage Actions

1. **Add `ai-cve-triaged` label** to TC-8001
2. **Correct Affects Versions**: Remove `RHTPA 2.0.0`, add `RHTPA 2.2.0`, `RHTPA 2.2.1`, `RHTPA 2.2.2`
3. **Post summary comment** on TC-8001 with:
   - Version impact table
   - Affects Versions correction
   - Note that 2.2.x is already fixed in 2.2.3+ (quinn-proto 0.11.14)
   - Cross-stream impact on 2.1.x
   - Links to preemptive remediation tasks created for 2.1.x
   - @mention of the issue reporter
4. **Post preemptive tasks comment** on TC-8001 listing tasks created for 2.1.x
