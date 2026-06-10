# Step 7 -- Remediation

## Triage Outcome

This is **Case A + Case B**: The 2.2.x stream (in scope) has affected versions requiring remediation, and the 2.1.x stream (out of scope) is also affected, requiring a cross-stream impact notice.

### Affected versions within scope (2.2.x stream)

- RHTPA 2.2.0 (quinn-proto 0.11.9)
- RHTPA 2.2.1 (quinn-proto 0.11.12)
- RHTPA 2.2.2 (retag of 2.2.1)

Note: RHTPA 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (the fixed version). The fix already exists on the upstream branch release/0.4.z, so the upstream backport task for the 2.2.x stream covers ensuring the fix is properly incorporated into a release that covers the affected versions.

### Ecosystem

Cargo (source dependency) -- requires **two tasks**: upstream backport + downstream propagation subtask with Blocks dependency.

---

## PROPOSAL: Task 1 -- Upstream Backport (2.2.x stream)

### Jira Issue Creation

```
PROPOSAL: Create upstream backport task
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

```
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

Upstream fix: quinn-rs/quinn#2048
Advisory: GHSA-2026-qp73-x4mq

Note: The fix has already landed on release/0.4.z as of v0.4.11 (quinn-proto 0.11.14).
If the branch HEAD already contains the fix, this task may be resolved by confirming
the fix is present and ensuring it will be included in the next release covering
the affected versions.

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
```

---

## PROPOSAL: Task 2 -- Downstream Propagation Subtask (2.2.x stream)

### Jira Issue Creation

```
PROPOSAL: Create downstream propagation subtask
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

```
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

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

## Implementation Notes

- Update the backend reference to the merged commit or new release tag
  that includes quinn-proto >= 0.11.14
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

---

## PROPOSAL: Jira Linkage

After creating both tasks:

1. **Link upstream task to Vulnerability issue**:
   ```
   PROPOSAL: jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

2. **Link downstream subtask as blocked by upstream task**:
   ```
   PROPOSAL: jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

3. **Link downstream subtask to Vulnerability issue**:
   ```
   PROPOSAL: jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

4. **Transition TC-8001 to In Progress**.

5. **Add ai-cve-triaged label** to TC-8001.

---

## PROPOSAL: Cross-Stream Impact Notice (Case B)

The version impact analysis reveals that the **2.1.x stream** (outside this issue's scope) is also affected:

- RHTPA 2.1.0 (v0.3.8): quinn-proto 0.11.9 -- AFFECTED
- RHTPA 2.1.1 (v0.3.12): quinn-proto 0.11.9 -- AFFECTED

The upstream branch release/0.3.z does not appear to have the fix (latest tag v0.3.12 still shows 0.11.9).

```
PROPOSAL: Add comment to TC-8001

"Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis:
- RHTPA 2.1.0 (v0.3.8): quinn-proto 0.11.9
- RHTPA 2.1.1 (v0.3.12): quinn-proto 0.11.9

The 2.1.x stream is tracked separately -- this may require a companion
PSIRT issue or separate triage. The upstream branch release/0.3.z does
not yet include the fix."
```

No remediation tasks are created for the 2.1.x stream from this issue, as it is outside the issue's scope [rhtpa-2.2]. PSIRT manages per-stream Vulnerability tracking.
