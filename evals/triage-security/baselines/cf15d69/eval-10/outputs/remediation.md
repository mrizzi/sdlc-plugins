# Step 7 -- Remediation: TC-8020

## Triage Outcome

CVE-2026-55123 affects supported versions in both streams rhtpa-2.2 (issue scope) and rhtpa-2.1 (cross-stream). This triggers both Case A (standard remediation for the scoped stream) and Case B (preemptive remediation for the other stream).

---

## Case A: Standard Remediation (stream rhtpa-2.2)

The issue is scoped to stream rhtpa-2.2. Both RHTPA 2.2.0 and RHTPA 2.2.1 ship tokio 1.41.1 which is below the fix threshold of 1.42.0. Ecosystem is Cargo (source dependency), so two tasks are created.

### Task 1: Upstream Backport Task (rhtpa-2.2)

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`

**Description**:

> ## Repository
>
> backend
>
> ## Target Branch
>
> release/0.4.z
>
> ## Description
>
> Remediate CVE-2026-55123: Use-after-free in task abort in tokio.
> The vulnerable dependency (tokio < 1.42.0) must be updated
> to the fixed version (1.42.0+).
>
> Affected versions: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1)
> Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1)
>
> Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
> Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp
>
> ## Implementation Notes
>
> - Update tokio dependency to >= 1.42.0 in Cargo.lock
> - Target branch: release/0.4.z
> - Check for pinned versions or transitive dependency constraints
>   that might prevent the bump
> - If a direct bump introduces breaking changes, assess whether a
>   code-level workaround is viable (see upstream changelog)
>
> ## Acceptance Criteria
>
> - [ ] tokio dependency is >= 1.42.0
> - [ ] No other dependency conflicts introduced
> - [ ] Existing tests pass
>
> ## Test Requirements
>
> - [ ] Existing test suite passes with the updated dependency
>
> ## Dependencies
>
> - Depends on: TC-8020 (parent tracking issue)

**Jira API call**:
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Link**: `jira.create_link(inwardIssue: "TC-8020", outwardIssue: <upstream-task-key>, type: "Depend")`

### Task 2: Downstream Propagation Subtask (rhtpa-2.2)

**Summary**: Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`

**Description**:

> ## Repository
>
> rhtpa-release.0.4.z
>
> ## Target Branch
>
> main
>
> ## Description
>
> Update backend reference in rhtpa-release.0.4.z to pick up the
> CVE-2026-55123 fix from <upstream-task-key>.
>
> The upstream backport (<upstream-task-key>) bumps tokio to 1.42.0
> on release/0.4.z. Once that PR merges, update the source pinning in this
> Konflux release repo so the next build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: artifacts.lock.yaml (download URL contains tag)
> - Update the backend reference to the merged commit or new release tag
> - Verify the Konflux build pipeline triggers successfully
>
> ## Acceptance Criteria
>
> - [ ] backend reference updated to include the fix
> - [ ] Konflux rebuild triggers new container image
>
> ## Test Requirements
>
> - [ ] Container image builds successfully with the updated reference
>
> ## Dependencies
>
> - Depends on: <upstream-task-key> (upstream backport must merge first)
> - Depends on: TC-8020 (parent tracking issue)

**Jira API call**:
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Links**:
- `jira.create_link(inwardIssue: "TC-8020", outwardIssue: <downstream-task-key>, type: "Depend")`
- `jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")`

---

## Case B: Preemptive Remediation (stream rhtpa-2.1)

Cross-stream impact analysis shows stream rhtpa-2.1 is also affected (tokio 1.40.0 < 1.42.0). A JQL search for sibling CVE Jiras with label CVE-2026-55123 returns no results for stream rhtpa-2.1 -- no CVE Jira exists for that stream. Per Step 7 Case B, preemptive remediation tasks are created.

### Task 3: Preemptive Upstream Backport Task (rhtpa-2.1)

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.
>
> ## Repository
>
> backend
>
> ## Target Branch
>
> release/0.3.z
>
> ## Description
>
> Remediate CVE-2026-55123: Use-after-free in task abort in tokio.
> The vulnerable dependency (tokio < 1.42.0) must be updated
> to the fixed version (1.42.0+).
>
> Affected versions: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)
> Source commit(s): v0.3.8 (2.1.0), v0.3.12 (2.1.1)
>
> Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
> Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp
>
> ## Implementation Notes
>
> - Update tokio dependency to >= 1.42.0 in Cargo.lock
> - Target branch: release/0.3.z
> - Check for pinned versions or transitive dependency constraints
>   that might prevent the bump
> - If a direct bump introduces breaking changes, assess whether a
>   code-level workaround is viable (see upstream changelog)
>
> ## Acceptance Criteria
>
> - [ ] tokio dependency is >= 1.42.0
> - [ ] No other dependency conflicts introduced
> - [ ] Existing tests pass
>
> ## Test Requirements
>
> - [ ] Existing test suite passes with the updated dependency
>
> ## Dependencies
>
> - Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)

**Jira API call**:
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)",
  description: <upstream-task-description-with-preemptive-prefix>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Link**: `jira.create_link(inwardIssue: "TC-8020", outwardIssue: <preemptive-upstream-task-key>, type: "Related")`

### Task 4: Preemptive Downstream Propagation Subtask (rhtpa-2.1)

**Summary**: Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.
>
> ## Repository
>
> rhtpa-release.0.3.z
>
> ## Target Branch
>
> main
>
> ## Description
>
> Update backend reference in rhtpa-release.0.3.z to pick up the
> CVE-2026-55123 fix from <preemptive-upstream-task-key>.
>
> The upstream backport (<preemptive-upstream-task-key>) bumps tokio to 1.42.0
> on release/0.3.z. Once that PR merges, update the source pinning in this
> Konflux release repo so the next build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: artifacts.lock.yaml (download URL contains tag)
> - Update the backend reference to the merged commit or new release tag
> - Verify the Konflux build pipeline triggers successfully
>
> ## Acceptance Criteria
>
> - [ ] backend reference updated to include the fix
> - [ ] Konflux rebuild triggers new container image
>
> ## Test Requirements
>
> - [ ] Container image builds successfully with the updated reference
>
> ## Dependencies
>
> - Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
> - Related to: TC-8020 (originating CVE Jira, stream rhtpa-2.2)

**Jira API call**:
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <downstream-task-description-with-preemptive-prefix>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Links**:
- `jira.create_link(inwardIssue: "TC-8020", outwardIssue: <preemptive-downstream-task-key>, type: "Related")`
- `jira.create_link(inwardIssue: <preemptive-upstream-task-key>, outwardIssue: <preemptive-downstream-task-key>, type: "Blocks")`

---

## Post-Triage Actions

1. **Add `ai-cve-triaged` label** to TC-8020
2. **Transition** TC-8020 to In Progress
3. **Assign** TC-8020 to the current user
4. **Post summary comment** to TC-8020 documenting all created tasks and the version impact table (with Comment Footnote)

---

_This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/mrizzi/sdlc-plugins) v0.11.0._
