# Step 8 -- Remediation

## Triage Outcome

### Stream 2.2.x (issue scope)

The version impact analysis shows that versions 2.2.0, 2.2.1, and 2.2.2 shipped
the vulnerable quinn-proto (< 0.11.14), but versions 2.2.3 and 2.2.4 already
ship quinn-proto 0.11.14 (the fixed version). The upstream branch release/0.4.z
already contains the fix.

**No new remediation task is needed for the 2.2.x stream.** The fix was
incorporated starting from build 0.4.11 (version 2.2.3, released 2026-03-23).
The Affects Versions have been corrected to [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
to accurately reflect which versions shipped the vulnerable dependency.

### Stream 2.1.x (Case B -- cross-stream impact)

The version impact analysis reveals that stream 2.1.x is also affected:
- 2.1.0 ships quinn-proto 0.11.9 (vulnerable)
- 2.1.1 ships quinn-proto 0.11.9 (vulnerable)

Since this issue is scoped to stream 2.2.x (suffix `[rhtpa-2.2]`), the 2.1.x
stream is outside the issue's scope. Case B applies: post a cross-stream impact
comment and create preemptive remediation tasks for stream 2.1.x (assuming no
existing CVE Jira exists for this CVE in the 2.1.x stream).

## Cross-Stream Impact Comment

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on
lock file analysis. All versions in stream 2.1.x (2.1.0, 2.1.1) ship
quinn-proto 0.11.9.

These streams are tracked by companion issues (see Related links) or may
require separate PSIRT triage.
```

## Preemptive Remediation Tasks for Stream 2.1.x

Since the ecosystem is Cargo (source dependency), two tasks are created:
an upstream backport task and a downstream propagation subtask.

### Task 1: Upstream Backport (preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

## Repository

rhtpa-backend

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

- Target branch: release/0.3.z
- **Dependency type**: to be determined via lock file analysis
  (check Cargo.toml for direct vs transitive)
- Update quinn-proto dependency to >= 0.11.14

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

**Link type**: Related (to TC-8001, not Depend, because TC-8001 belongs to a
different stream)

---

### Task 2: Downstream Propagation (preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Link type**: Related (to TC-8001), Blocks (downstream is blocked by upstream backport task)

---

## Jira Actions Summary

1. **Post cross-stream impact comment** on TC-8001 noting that stream 2.1.x
   is also affected
2. **Create upstream backport task** for stream 2.1.x with `security-preemptive` label
3. **Post description digest comment** on upstream task
4. **Create downstream propagation task** for stream 2.1.x with `security-preemptive` label
5. **Post description digest comment** on downstream task
6. **Link upstream task** to TC-8001 with "Related" link type
7. **Link downstream task** to TC-8001 with "Related" link type
8. **Link downstream task** as blocked by upstream task with "Blocks" link type
9. **Post comment** on TC-8001 listing the preemptive tasks created
10. **Add `ai-cve-triaged` label** to TC-8001
