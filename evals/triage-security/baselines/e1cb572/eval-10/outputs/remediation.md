# Step 7 -- Remediation

## Triage Outcome

- **Case A**: Stream rhtpa-2.2 is affected -- create standard remediation tasks
- **Case B**: Stream rhtpa-2.1 is also affected with no CVE Jira -- create preemptive remediation tasks

Ecosystem: **Cargo** (source dependency) -- two tasks per stream (upstream backport + downstream propagation).

---

## Case A: Remediation Tasks for rhtpa-2.2 (Current Stream)

### Task 1: Upstream Backport (rhtpa-2.2)

**Proposed Jira creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Task description:**

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: Use-after-free in task abort in the tokio crate.
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Update tokio dependency to >= 1.42.0 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (parent tracking issue)

---

### Task 2: Downstream Propagation (rhtpa-2.2)

**Proposed Jira creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Task description:**

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from the upstream backport task.

The upstream backport bumps tokio to 1.42.0 on release/0.4.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

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
- Depends on: TC-8020 (parent tracking issue)

---

### Linkage for Case A tasks

**Proposed Jira link operations:**

1. Link upstream task to TC-8020:
   ```
   jira.create_link(inwardIssue: "TC-8020", outwardIssue: <upstream-task-key>, type: "Depend")
   ```

2. Link downstream task as blocked by upstream:
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

3. Link downstream task to TC-8020:
   ```
   jira.create_link(inwardIssue: "TC-8020", outwardIssue: <downstream-task-key>, type: "Depend")
   ```

---

## Case B: Preemptive Remediation Tasks for rhtpa-2.1

Stream rhtpa-2.1 is affected (tokio 1.40.0 < 1.42.0) but has no CVE Jira.
Creating preemptive remediation tasks with `security-preemptive` label and "Related" link type.

### Preemptive Task 1: Upstream Backport (rhtpa-2.1)

**Proposed Jira creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Task description:**

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-55123: Use-after-free in task abort in the tokio crate.
The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Update tokio dependency to >= 1.42.0 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (related -- originating CVE Jira, different stream)

---

### Preemptive Task 2: Downstream Propagation (rhtpa-2.1)

**Proposed Jira creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Task description:**

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from the preemptive upstream backport task.

The upstream backport bumps tokio to 1.42.0 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

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

- Depends on: preemptive upstream backport task (upstream backport must merge first)
- Depends on: TC-8020 (related -- originating CVE Jira, different stream)

---

### Linkage for Case B preemptive tasks

**Proposed Jira link operations:**

1. Link preemptive upstream task to TC-8020 with "Related" (not "Depend"):
   ```
   jira.create_link(inwardIssue: "TC-8020", outwardIssue: <preemptive-upstream-task-key>, type: "Related")
   ```

2. Link preemptive downstream task as blocked by preemptive upstream:
   ```
   jira.create_link(inwardIssue: <preemptive-upstream-task-key>, outwardIssue: <preemptive-downstream-task-key>, type: "Blocks")
   ```

3. Link preemptive downstream task to TC-8020 with "Related":
   ```
   jira.create_link(inwardIssue: "TC-8020", outwardIssue: <preemptive-downstream-task-key>, type: "Related")
   ```

---

## Post-Triage Actions

### 1. Add `ai-cve-triaged` label to TC-8020

**Proposed:**
```
jira.edit_issue("TC-8020", fields={
  "labels": ["CVE-2026-55123", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 2. Transition TC-8020 to In Progress

**Proposed:**
```
jira.transition_issue("TC-8020", transition: "In Progress")
```

### 3. Post summary comment to TC-8020

**Proposed comment:**

---

**Triage Summary for CVE-2026-55123 (tokio < 1.42.0)**

**Version Impact:**

| Version | Stream | tokio | Affected? |
|---------|--------|-------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES |

**Affects Versions:** No correction needed -- PSIRT assignment is correct (RHTPA 2.2.0, RHTPA 2.2.1).

**Triage Outcome:**
- Case A (rhtpa-2.2): Remediation tasks created -- upstream backport task and downstream propagation task
- Case B (rhtpa-2.1): Preemptive remediation tasks created -- no CVE Jira exists for this stream

**Remediation Tasks (rhtpa-2.2):**
- [upstream-task-key]: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)
- [downstream-task-key]: Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Preemptive Tasks (rhtpa-2.1):**
- [preemptive-upstream-task-key]: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) (security-preemptive)
- [preemptive-downstream-task-key]: Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1) (security-preemptive)

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/mrizzi/sdlc-plugins) v0.11.0.
