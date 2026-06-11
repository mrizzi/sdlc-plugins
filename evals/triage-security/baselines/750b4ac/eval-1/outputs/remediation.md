# Step 7 -- Remediation Task Descriptions

## Triage Outcome: Case A -- Affected (create remediation tasks)

The 2.2.x stream has affected versions (2.2.0, 2.2.1, 2.2.2). Since quinn-proto is a **Cargo** ecosystem (source dependency), two tasks are required:

1. **Upstream backport task** -- fix the dependency in the source repository
2. **Downstream propagation subtask** -- update the source reference in the Konflux release repo

The downstream subtask is **Blocks**-linked to the upstream task (downstream is blocked by upstream).

### Cross-Stream Impact Notice

The 2.1.x stream (versions 2.1.0, 2.1.1) also ships vulnerable quinn-proto (0.11.9), but this is outside the scope of TC-8001 (scoped to 2.2.x). A cross-stream impact comment would be posted to TC-8001 noting this observation for PSIRT awareness.

---

## PROPOSAL: Task 1 -- Upstream Backport Task

**Proposed Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Proposed Labels**: ai-generated-jira, Security, CVE-2026-31812

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto before version 0.11.14 allows a remote attacker to cause a panic by sending a QUIC transport frame that creates an excessive number of streams (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (tag v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (tag v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock (and Cargo.toml if directly specified)
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)
- Note: versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 on this branch, confirming the fix is available upstream

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent Vulnerability tracking issue)

---

## PROPOSAL: Task 2 -- Downstream Propagation Subtask

**Proposed Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

**Proposed Labels**: ai-generated-jira, Security, CVE-2026-31812

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.4.12`)
- Update the rhtpa-backend reference to the merged commit or new release tag that includes quinn-proto >= 0.11.14
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent Vulnerability tracking issue)

---

## Proposed Jira Operations

All operations below are **proposals** requiring engineer confirmation before execution.

### Task Creation

```
PROPOSAL: upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <upstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)

PROPOSAL: downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <downstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Linkage

```
PROPOSAL: jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream_task.key>,
  type: "Depend"
)

PROPOSAL: jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream_task.key>,
  type: "Depend"
)

PROPOSAL: jira.create_link(
  inwardIssue: <upstream_task.key>,
  outwardIssue: <downstream_task.key>,
  type: "Blocks"
)
```

The **Blocks** link between upstream and downstream ensures the downstream propagation task cannot proceed until the upstream backport merges. This reflects the actual dependency: the Konflux release repo cannot reference a fix that does not yet exist in the source repository.
