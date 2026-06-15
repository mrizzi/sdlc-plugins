# Step 7 - Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome: Case A - Affected, create remediation tasks

The 2.2.x stream has affected versions (2.2.0, 2.2.1, 2.2.2). The fix is already available upstream (quinn-proto 0.11.14 ships in v0.4.11+), so remediation involves a source repo backport and a Konflux release repo propagation.

Ecosystem: **Cargo** (source dependency) -- two tasks required per stream.

Additionally, **Case B applies**: cross-stream impact detected in the 2.1.x stream (versions 2.1.0, 2.1.1 ship quinn-proto 0.11.9). A cross-stream impact comment would be posted.

---

## Task 1: Upstream Backport Task (2.2.x stream)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is a retag of v0.4.8)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)
- Note: versions 2.2.3+ (v0.4.11+) already ship quinn-proto 0.11.14,
  confirming the upgrade path is viable on this branch

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Task 2: Downstream Propagation Subtask (2.2.x stream)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully
- The backend tag must point to a commit that includes quinn-proto >= 0.11.14

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Jira Linkage (would execute after task creation)

1. Link upstream backport task to TC-8001 with "Depend" link type
2. Link downstream propagation task to TC-8001 with "Depend" link type
3. Link downstream propagation task as blocked by upstream backport task with "Blocks" link type
4. Transition TC-8001 to In Progress
5. Assign TC-8001 to current user
6. Add ai-cve-triaged label to TC-8001

## Cross-Stream Impact Comment (would be posted to TC-8001)

```
Cross-stream impact: quinn-proto (versions before 0.11.14) also affects stream 2.1.x
based on lock file analysis:
- 2.1.0 (v0.3.8): quinn-proto 0.11.9
- 2.1.1 (v0.3.12): quinn-proto 0.11.9

These versions are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```
