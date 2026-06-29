# Step 7 -- Remediation

## Case A: Standard Remediation Tasks for rhtpa-2.2 (Issue Scope)

TC-8020 is scoped to stream rhtpa-2.2. Versions RHTPA 2.2.0 and RHTPA 2.2.1 are affected (tokio 1.41.1 < 1.42.0). Since tokio is a Cargo (source dependency) ecosystem, two tasks are created: an upstream backport task and a downstream propagation subtask.

### Task 1: Upstream Backport Task (rhtpa-2.2)

**Jira creation call:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Description:**

```markdown
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: Use-after-free in task abort in the tokio crate.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1
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
```

**Link:**

```
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)
```

**Labels:** `["ai-generated-jira", "Security", "CVE-2026-55123"]`

### Task 2: Downstream Propagation Subtask (rhtpa-2.2)

**Jira creation call:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Description:**

```markdown
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps tokio to 1.42.0
on release/0.4.z. Once that PR merges, update the source pinning in this
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

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

**Links:**

```
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

**Labels:** `["ai-generated-jira", "Security", "CVE-2026-55123"]`

---

## Case B: Preemptive Remediation Tasks for rhtpa-2.1 (Cross-Stream)

Stream rhtpa-2.1 is also affected (tokio 1.40.0 < 1.42.0) but has no CVE Jira for CVE-2026-55123. Preemptive remediation tasks are created with the `security-preemptive` label and "Related" link (not "Depend") to TC-8020.

### Task 3: Preemptive Upstream Backport Task (rhtpa-2.1)

**Jira creation call:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Description:**

```markdown
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-55123: Use-after-free in task abort in the tokio crate.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
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

- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)
```

**Link (Related, not Depend):**

```
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <preemptive-upstream-task-key>,
  type: "Related"
)
```

**Labels:** `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`

### Task 4: Preemptive Downstream Propagation Subtask (rhtpa-2.1)

**Jira creation call:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Description:**

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps tokio to 1.42.0
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

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)
```

**Links:**

```
jira.create_link(
  inwardIssue: "TC-8020",
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Related"
)

jira.create_link(
  inwardIssue: <preemptive-upstream-task-key>,
  outwardIssue: <preemptive-downstream-task-key>,
  type: "Blocks"
)
```

**Labels:** `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`

---

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8020.
2. Post summary comment to TC-8020 documenting the version impact table, Affects Versions confirmation, remediation tasks created (Case A for rhtpa-2.2, Case B preemptive for rhtpa-2.1), and cross-stream impact notice. Include @mention of the reporter.
3. Comment footnote: all Jira comments include the sdlc-workflow/triage-security v0.11.0 footnote.
