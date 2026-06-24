# Step 7 -- Remediation: TC-8004

## Triage Outcome

**Case A: Affected -- create remediation tasks for the 2.1.x stream only.**

The version impact analysis shows:
- **2.1.x stream**: ALL versions affected (2.1.0 and 2.1.1 ship h2 0.4.5, below fix threshold 0.4.8)
- **2.2.x stream**: NO versions affected (all ship h2 >= 0.4.8)

Since this is a **source dependency ecosystem** (Cargo), two tasks are required for the affected 2.1.x stream: an upstream backport task and a downstream propagation subtask.

No remediation is needed for the 2.2.x stream as it already ships the fixed version.

---

## Task 1: Upstream Backport (2.1.x stream)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Task Description

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (build v0.3.8), RHTPA 2.1.1 (build v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock (and Cargo.toml if directly specified)
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)
- The fix adds a configurable maximum header list size that defaults to 16 KiB

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)

---

## Task 2: Downstream Propagation (2.1.x stream)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)

---

## Jira Linkage (proposed)

```
# Link upstream task to Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <upstream-task-key>,
  type: "Depend"
)

# Link downstream task to Vulnerability issue
jira.create_link(
  inwardIssue: "TC-8004",
  outwardIssue: <downstream-task-key>,
  type: "Depend"
)

# Link downstream task as blocked by upstream task
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

## Post-Triage Actions

1. **Add label** `ai-cve-triaged` to TC-8004
2. **Transition** TC-8004 to In Progress
3. **Assign** TC-8004 to current user

## Post-Triage Summary Comment (proposed for TC-8004)

```
Triage complete for CVE-2026-33501 (h2 < 0.4.8).

Version Impact:

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | YES | |
| 2.1.1 | 2.1.x | 0.4.5 | YES | |
| 2.2.0 | 2.2.x | 0.4.8 | NO | at fix threshold |
| 2.2.1 | 2.2.x | 0.4.8 | NO | |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.9 | NO | |
| 2.2.4 | 2.2.x | 0.4.9 | NO | |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
- Removed RHTPA 2.2.0 (2.2.x ships h2 >= 0.4.8, not affected)
- Added RHTPA 2.1.1 (ships h2 0.4.5, affected)

Remediation tasks created for 2.1.x stream:
- <upstream-task-key>: upstream backport -- bump h2 to >= 0.4.8 on release/0.3.z
- <downstream-task-key>: downstream propagation -- update backend ref in rhtpa-release.0.3.z (blocked by <upstream-task-key>)

No remediation needed for 2.2.x stream (all versions ship patched h2).
```

## Sibling/Duplicate Check (Step 4)

JQL search for sibling issues with label CVE-2026-33501 returned empty. No duplicates or companion issues exist. No preemptive tasks found. Proceeding with remediation for the affected 2.1.x stream only.
