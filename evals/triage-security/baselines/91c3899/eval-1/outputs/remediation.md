# Step 7 -- Remediation

## Triage Outcome: Case A -- Affected, Create Remediation Tasks

The 2.2.x stream has affected versions (2.2.0, 2.2.1, 2.2.2). Remediation tasks are needed.

Since quinn-proto is a **Cargo** (source dependency) ecosystem, two tasks are created:
1. **Upstream backport task** -- fix in the source repository (`backend`)
2. **Downstream propagation subtask** -- update the reference in the Konflux release repo (`rhtpa-release.0.4.z`), blocked by the upstream task

## Cross-Stream Impact Notice

The 2.1.x stream is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9), but is outside the scope of this issue (`[rhtpa-2.2]`). A comment would be posted to TC-8001 noting the cross-stream impact, per Case B:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by a companion issue (see Related links) or may require separate PSIRT triage.

---

## Proposed Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1, quinn-proto 0.11.12)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
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

---

## Proposed Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

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

## Proposed Jira Operations

All operations below are **proposed actions** pending engineer confirmation. No Jira mutations have been executed.

### 1. Create upstream backport task

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <upstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### 2. Create downstream propagation subtask

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <downstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### 3. Link tasks to Vulnerability issue

```
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream_task.key>,
  type: "Depend"
)

jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream_task.key>,
  type: "Depend"
)
```

### 4. Link downstream as blocked by upstream (Blocks dependency)

```
jira.create_link(
  inwardIssue: <upstream_task.key>,
  outwardIssue: <downstream_task.key>,
  type: "Blocks"
)
```

### 5. Transition and assign

```
jira.transition_issue("TC-8001", status: "In Progress")
jira.assign_issue("TC-8001", assignee: <current-user>)
```

### 6. Post comment to TC-8001

```
jira.add_comment("TC-8001", comment: "Remediation tasks created:
  <upstream_task.key> (upstream backport: bump quinn-proto to 0.11.14 on release/0.4.z),
  <downstream_task.key> (downstream propagation: update backend ref in rhtpa-release.0.4.z, blocked by <upstream_task.key>)")
```

### 7. Add triage label

```
jira.edit_issue("TC-8001", labels: [existing labels + "ai-cve-triaged"])
```
