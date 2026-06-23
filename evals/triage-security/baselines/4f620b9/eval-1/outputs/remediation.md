# Step 7 -- Remediation

## Triage Outcome

This issue is scoped to the **2.2.x** stream. Within the 2.2.x stream, versions 2.2.0, 2.2.1, and 2.2.2 are affected. This is **Case A** (affected -- create remediation tasks).

Additionally, the **2.1.x** stream is also affected (all versions). This triggers **Case B** (cross-stream impact notice).

## Ecosystem and Task Count

- **Ecosystem**: Cargo (source dependency)
- **Task structure**: Two tasks per affected stream -- upstream backport + downstream propagation with Blocks dependency

Since the issue is scoped to 2.2.x, remediation tasks are created only for the 2.2.x stream. Cross-stream impact on 2.1.x is reported via comment only.

---

## Task 1: Upstream Backport (2.2.x stream)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

Note: Versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already ship quinn-proto 0.11.14 and are not affected. The fix is already present on the release/0.4.z branch for builds >= 0.4.11.

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)
- Note: quinn-proto 0.11.14 is already present in later builds (v0.4.11+),
  confirming compatibility with the codebase

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Task 2: Downstream Propagation (2.2.x stream)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
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

## Jira Linkage (proposed)

1. Link upstream backport task to TC-8001:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

2. Link downstream propagation task to TC-8001:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

3. Link downstream task as blocked by upstream task (Blocks dependency):
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

4. Transition TC-8001 to In Progress.

5. Assign TC-8001 to current user.

---

## Cross-Stream Impact Notice (Case B)

The following comment would be posted to TC-8001 to inform about cross-stream impact:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis.

2.1.x version details:
- RHTPA 2.1.0 (v0.3.8): quinn-proto 0.11.9 -- AFFECTED
- RHTPA 2.1.1 (v0.3.12): quinn-proto 0.11.9 -- AFFECTED

This stream is tracked by a companion issue (see Related links)
or may require separate PSIRT triage.
```

---

## Post-Triage Summary

The following actions would be performed after engineer confirmation:

1. **Add label** `ai-cve-triaged` to TC-8001
2. **Post summary comment** to TC-8001 documenting:
   - Version impact table (all 7 versions across both streams)
   - Affects Versions correction: removed RHTPA 2.0.0, added RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
   - Triage outcome: Case A (remediation tasks created for 2.2.x) + Case B (cross-stream notice for 2.1.x)
   - Links to remediation tasks: upstream backport task and downstream propagation task (blocked by upstream)
