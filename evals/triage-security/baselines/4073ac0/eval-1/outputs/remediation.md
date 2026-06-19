# Step 7 -- Remediation

## Triage Outcome: Case A -- Affected, create remediation tasks

The 2.2.x stream has affected versions (2.2.0, 2.2.1, 2.2.2). Since quinn-proto is a **Cargo** (source dependency) ecosystem, two remediation tasks are required: an upstream backport task and a downstream propagation task with a Blocks dependency.

Additionally, **Case B** applies: the 2.1.x stream is also affected (outside this issue's scope). A cross-stream impact comment should be posted.

---

## PROPOSED Cross-Stream Impact Comment (Case B)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on
lock file analysis. Versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9.
This stream is tracked by a companion issue (see Related links) or may require
separate PSIRT triage.
```

---

## PROPOSED Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-31812

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (tag v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (tag v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (retag of 2.2.1, quinn-proto 0.11.12)
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
- Note: versions 2.2.3+ already ship quinn-proto 0.11.14 on this branch,
  so the fix may already be present at branch HEAD

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## PROPOSED Task 2: Downstream Propagation Task

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

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
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

## PROPOSED Jira Linkage

### Task creation calls:

```
# 1. Upstream backport task
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <upstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)

# 2. Downstream propagation task
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <downstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Link creation calls:

```
# Link upstream task to Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <upstream_task.key>,
  type: "Depend"
)

# Link downstream task to Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8001",
  outwardIssue: <downstream_task.key>,
  type: "Depend"
)

# Downstream task is Blocked by upstream task
jira.create_link(
  inwardIssue: <upstream_task.key>,
  outwardIssue: <downstream_task.key>,
  type: "Blocks"
)
```

### Post-creation actions:

```
# Transition Vulnerability to In Progress
jira.transition_issue("TC-8001", status: "In Progress")

# Assign Vulnerability to current user
jira.edit_issue("TC-8001", fields={"assignee": {"accountId": "<current-user>"}})

# Add ai-cve-triaged label
jira.edit_issue("TC-8001", fields={"labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]})
```

---

## Post-Triage Summary (PROPOSED comment on TC-8001)

```
Triage complete for CVE-2026-31812 (quinn-proto < 0.11.14).

Version Impact:
| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0   | 0.11.9      | YES       | stream 2.1.x (out of scope) |
| 2.1.1   | 0.11.9      | YES       | stream 2.1.x (out of scope) |
| 2.2.0   | 0.11.9      | YES       |       |
| 2.2.1   | 0.11.12     | YES       |       |
| 2.2.2   | 0.11.12     | YES       | retag of 2.2.1 |
| 2.2.3   | 0.11.14     | NO        | ships fixed version |
| 2.2.4   | 0.11.14     | NO        | ships fixed version |

Affects Versions correction: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

Remediation tasks created:
- <upstream_task.key> (upstream backport: bump quinn-proto to 0.11.14 on release/0.4.z)
- <downstream_task.key> (downstream propagation: update backend ref in rhtpa-release.0.4.z, blocked by <upstream_task.key>)

Cross-stream impact: 2.1.x stream also affected (2.1.0, 2.1.1 ship quinn-proto 0.11.9).
```
