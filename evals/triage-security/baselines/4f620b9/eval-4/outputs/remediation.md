# Step 7 -- Remediation

## Triage Decision

**Case A: Affected -- create remediation tasks**

The 2.1.x stream is affected (all versions ship h2 0.4.5, which is within the vulnerable range < 0.4.8). The 2.2.x stream is NOT affected (all versions ship h2 >= 0.4.8).

Since this is an unscoped issue (no stream suffix), all streams were analyzed. Remediation tasks are created only for the affected stream (2.1.x). No cross-stream impact notice is needed because the issue is unscoped -- it already covers all streams by definition.

## Ecosystem: Cargo (source dependency)

The h2 crate is a Cargo ecosystem dependency. Per the remediation template, this requires **two tasks**:

1. An upstream backport task (fix in the source repository)
2. A downstream propagation subtask (update the reference in the Konflux release repo)

## Proposed Remediation Task 1: Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

### Task Description

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 - Memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 versions before 0.4.8) must be updated
to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (build v0.3.8), RHTPA 2.1.1 (build v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- h2 is a transitive dependency (via hyper); updating may require bumping hyper or adjusting dependency constraints
- Check for pinned versions or transitive dependency constraints that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)

---

### Proposed Jira API Call

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <upstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

## Proposed Remediation Task 2: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

### Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.8
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

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

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)

---

### Proposed Jira API Call

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <downstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

## Proposed Linkage

After task creation:

1. Link upstream task to TC-8004:
   ```
   jira.create_link(inwardIssue: "TC-8004", outwardIssue: <upstream-task-key>, type: "Depend")
   ```

2. Link downstream task to TC-8004:
   ```
   jira.create_link(inwardIssue: "TC-8004", outwardIssue: <downstream-task-key>, type: "Depend")
   ```

3. Link downstream task as blocked by upstream task:
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

4. Transition TC-8004 to In Progress

5. Assign TC-8004 to current user

## Why No 2.2.x Remediation

No remediation tasks are created for the 2.2.x stream because all 2.2.x versions (2.2.0 through 2.2.4) already ship h2 >= 0.4.8, which is at or above the fixed version. The vulnerability does not affect the 2.2.x stream.

## Why No Cross-Stream Impact Notice

A cross-stream impact notice (Case B) is NOT generated because the issue is **unscoped** -- it has no stream suffix and already covers all streams. Cross-stream notices are only relevant for stream-scoped issues where the analysis reveals impact outside the issue's declared scope. Since TC-8004 is unscoped, there is no "outside scope" to report on.

## Post-Triage Summary

After engineer confirmation and execution of the above mutations:

1. Add the `ai-cve-triaged` label to TC-8004
2. Post a summary comment to TC-8004 documenting:
   - The version impact table (2.1.x affected, 2.2.x not affected)
   - The Affects Versions correction (removed RHTPA 2.2.0, added RHTPA 2.1.1)
   - Remediation outcome: two tasks created for 2.1.x stream (upstream backport + downstream propagation)
   - Links to both remediation tasks

All of the above are **proposals** requiring engineer confirmation before execution.
