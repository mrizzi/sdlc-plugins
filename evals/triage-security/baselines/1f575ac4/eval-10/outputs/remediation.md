# Step 7 -- Remediation

## Case A: Standard Remediation for Current Stream (rhtpa-2.2)

The issue TC-8020 is scoped to stream rhtpa-2.2. All versions in this stream (RHTPA 2.2.0, RHTPA 2.2.1) are affected. Standard remediation tasks are created.

### Task 1: Upstream Backport Task (rhtpa-2.2)

**Jira Creation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123"]`

**Description:**

> ## Repository
>
> rhtpa-backend
>
> ## Target Branch
>
> release/0.4.z
>
> ## Description
>
> Remediate CVE-2026-55123: tokio use-after-free in task abort.
> The vulnerable dependency (tokio < 1.42.0) must be updated
> to the fixed version (1.42.0+).
>
> Affected versions: RHTPA 2.2.0, RHTPA 2.2.1
> Source commit(s): v0.4.5, v0.4.8
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

**Post-creation actions:**
1. Post description digest comment on the upstream task
2. Link to TC-8020 with "Depend" link type:
   ```
   jira.create_link(
     inwardIssue: "TC-8020",
     outwardIssue: "<upstream-task-key>",
     type: "Depend"
   )
   ```

### Task 2: Downstream Propagation Subtask (rhtpa-2.2)

**Jira Creation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]
)
```

**Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123"]`

**Description:**

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
> Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
> CVE-2026-55123 fix from <upstream-task-key>.
>
> The upstream backport (<upstream-task-key>) bumps tokio to 1.42.0
> on release/0.4.z. Once that PR merges, update the source pinning in this
> Konflux release repo so the next build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: artifacts.lock.yaml (download URL contains tag)
> - Update the rhtpa-backend reference to the merged commit or new release tag
> - Verify the Konflux build pipeline triggers successfully
>
> ## Acceptance Criteria
>
> - [ ] rhtpa-backend reference updated to include the fix
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

**Post-creation actions:**
1. Post description digest comment on the downstream task
2. Link to TC-8020 with "Depend" link type:
   ```
   jira.create_link(
     inwardIssue: "TC-8020",
     outwardIssue: "<downstream-task-key>",
     type: "Depend"
   )
   ```
3. Link downstream as blocked by upstream:
   ```
   jira.create_link(
     inwardIssue: "<upstream-task-key>",
     outwardIssue: "<downstream-task-key>",
     type: "Blocks"
   )
   ```

---

## Case B: Preemptive Remediation for Cross-Stream (rhtpa-2.1)

Stream rhtpa-2.1 is also affected (tokio 1.40.0 < 1.42.0) but has **no CVE Jira** for this vulnerability. A JQL search for sibling Vulnerability issues with label CVE-2026-55123 returns no results for stream rhtpa-2.1. Per Step 7 Case B, proactive preemptive remediation tasks are created.

### Preemptive Task 1: Upstream Backport Task (rhtpa-2.1)

**Jira Creation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`

**Description:**

> ## Repository
>
> rhtpa-backend
>
> ## Target Branch
>
> release/0.3.z
>
> ## Description
>
> > **Preemptive remediation**: This task was created proactively from cross-stream
> > impact analysis of TC-8020 (stream rhtpa-2.2).
> > No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> > this task will be linked and the `security-preemptive` label removed.
>
> Remediate CVE-2026-55123: tokio use-after-free in task abort.
> The vulnerable dependency (tokio < 1.42.0) must be updated
> to the fixed version (1.42.0+).
>
> Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
> Source commit(s): v0.3.8, v0.3.12
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

**Post-creation actions:**
1. Post description digest comment on the preemptive upstream task
2. Link to TC-8020 with "Related" link type (NOT "Depend", because the originating CVE belongs to a different stream):
   ```
   jira.create_link(
     inwardIssue: "TC-8020",
     outwardIssue: "<preemptive-upstream-task-key>",
     type: "Related"
   )
   ```

### Preemptive Task 2: Downstream Propagation Subtask (rhtpa-2.1)

**Jira Creation:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
)
```

**Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`

**Description:**

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
> > **Preemptive remediation**: This task was created proactively from cross-stream
> > impact analysis of TC-8020 (stream rhtpa-2.2).
> > No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> > this task will be linked and the `security-preemptive` label removed.
>
> Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
> CVE-2026-55123 fix from <preemptive-upstream-task-key>.
>
> The upstream backport (<preemptive-upstream-task-key>) bumps tokio to 1.42.0
> on release/0.3.z. Once that PR merges, update the source pinning in this
> Konflux release repo so the next build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: artifacts.lock.yaml (download URL contains tag)
> - Update the rhtpa-backend reference to the merged commit or new release tag
> - Verify the Konflux build pipeline triggers successfully
>
> ## Acceptance Criteria
>
> - [ ] rhtpa-backend reference updated to include the fix
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

**Post-creation actions:**
1. Post description digest comment on the preemptive downstream task
2. Link to TC-8020 with "Related" link type:
   ```
   jira.create_link(
     inwardIssue: "TC-8020",
     outwardIssue: "<preemptive-downstream-task-key>",
     type: "Related"
   )
   ```
3. Link downstream as blocked by upstream:
   ```
   jira.create_link(
     inwardIssue: "<preemptive-upstream-task-key>",
     outwardIssue: "<preemptive-downstream-task-key>",
     type: "Blocks"
   )
   ```

---

## Summary of All Remediation Tasks

| Task | Stream | Type | Labels | Link to TC-8020 |
|------|--------|------|--------|-----------------|
| Upstream backport (rhtpa-2.2) | rhtpa-2.2 | Standard (Case A) | ai-generated-jira, Security, CVE-2026-55123 | Depend |
| Downstream propagation (rhtpa-2.2) | rhtpa-2.2 | Standard (Case A) | ai-generated-jira, Security, CVE-2026-55123 | Depend |
| Upstream backport (rhtpa-2.1) | rhtpa-2.1 | Preemptive (Case B) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |
| Downstream propagation (rhtpa-2.1) | rhtpa-2.1 | Preemptive (Case B) | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related |
