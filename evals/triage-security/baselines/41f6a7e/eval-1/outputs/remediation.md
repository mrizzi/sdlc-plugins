# Step 7 -- Remediation

## Triage Outcome: Case A -- Affected (create remediation tasks)

The issue is scoped to stream 2.2.x. Versions 2.2.0, 2.2.1, and 2.2.2 are affected.
Versions 2.2.3 and 2.2.4 already ship the fixed quinn-proto 0.11.14.

Since quinn-proto is a **source dependency** (Cargo ecosystem), two tasks are created:
an upstream backport task and a downstream propagation subtask.

### Cross-Stream Impact Notice (Case B)

Stream 2.1.x is also affected (all versions ship quinn-proto 0.11.9). A cross-stream
impact comment would be posted to TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
(versions 2.1.0, 2.1.1) based on lock file analysis.
This stream is tracked by a companion issue (see Related links) or may
require separate PSIRT triage.
```

---

## Task 1: Upstream Backport Task

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

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (v0.4.9, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

Note: The upstream branch release/0.4.z already has quinn-proto 0.11.14 at its latest tag (v0.4.11+). This task may already be resolved -- verify that the fix is present on the branch tip before creating a new PR.

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)
- The upstream fix PR is https://github.com/quinn-rs/quinn/pull/2048

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Task 2: Downstream Propagation Subtask

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

Affected product versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

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

## Jira Operations (would execute after confirmation)

### Create upstream task
```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <upstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Create downstream subtask
```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <downstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Link tasks
```
# Link upstream task to Vulnerability issue
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")

# Link downstream task to Vulnerability issue
jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")

# Link downstream blocked by upstream
jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
```

### Post-triage actions
```
# Add ai-cve-triaged label
jira.edit_issue("TC-8001", fields={"labels": ["CVE-2026-31812", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]})

# Transition to In Progress
jira.transition_issue("TC-8001", transition: "In Progress")
```
