# Step 7 -- Remediation

## Triage Outcome

**Case A: Affected -- create remediation tasks for the 2.1.x stream only.**

The version impact analysis shows a **mixed impact across streams**:
- **2.1.x stream**: AFFECTED -- all versions (2.1.0, 2.1.1) ship h2 0.4.5, which is within the vulnerable range (< 0.4.8)
- **2.2.x stream**: NOT AFFECTED -- all versions ship h2 >= 0.4.8 (the fixed version)

Remediation tasks are created **only for the 2.1.x stream**. No tasks are needed for the 2.2.x stream since it already ships the patched dependency.

No cross-stream impact comment (Case B) is needed because the other stream (2.2.x) is not affected.

## Steps 4-6 Results

- **Step 4 (Duplicate/Sibling check)**: JQL search for sibling issues with label CVE-2026-33501 returned empty. No duplicates or companion issues exist.
- **Step 4.3 (Cross-CVE overlap)**: Skipped -- Upstream Affected Component, PS Component, and Stream custom fields are not configured in Security Configuration.
- **Step 4.4 (Preemptive task reconciliation)**: No preemptive tasks found for CVE-2026-33501.
- **Step 5 (Version Lifecycle check)**: Assumed both 2.1.x and 2.2.x are within support lifecycle (no external tool calls permitted in this eval).
- **Step 6 (Already Fixed check)**: No resolved sibling issues exist. Not already fixed.

## Remediation Tasks (2.1.x stream)

Since h2 is a **Cargo** (source dependency) ecosystem package, **two tasks** are required per the skill's remediation templates: one upstream backport task and one downstream propagation subtask.

### Task 1: Upstream Backport

```
Proposed action: Create Jira Task

jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Task Description:**

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 versions before 0.4.8) must be updated
to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)

---

### Task 2: Downstream Propagation

```
Proposed action: Create Jira Task

jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Task Description:**

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8
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

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)

---

## Proposed Jira Linkage

After task creation:

1. Link upstream backport task to TC-8004:
   ```
   jira.create_link(inwardIssue: "TC-8004", outwardIssue: <upstream-task-key>, type: "Depend")
   ```

2. Link downstream propagation subtask as blocked by upstream task:
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

3. Link downstream propagation subtask to TC-8004:
   ```
   jira.create_link(inwardIssue: "TC-8004", outwardIssue: <downstream-task-key>, type: "Depend")
   ```

4. Transition TC-8004 to In Progress.

5. Assign TC-8004 to current user.

## Post-Triage Summary

### Proposed: Add label `ai-cve-triaged` to TC-8004

### Proposed: Post summary comment to TC-8004

```
Triage summary for CVE-2026-33501 (h2 < 0.4.8):

Version Impact:

| Version | Stream | h2 version | Affected? |
|---------|--------|------------|-----------|
| 2.1.0 | 2.1.x | 0.4.5 | YES |
| 2.1.1 | 2.1.x | 0.4.5 | YES |
| 2.2.0 | 2.2.x | 0.4.8 | NO |
| 2.2.1 | 2.2.x | 0.4.8 | NO |
| 2.2.2 | 2.2.x | -- | NO (retag of 2.2.1) |
| 2.2.3 | 2.2.x | 0.4.9 | NO |
| 2.2.4 | 2.2.x | 0.4.9 | NO |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]

Outcome: Remediation tasks created for 2.1.x stream only.
- <upstream-task-key>: upstream backport (bump h2 to >= 0.4.8 on release/0.3.z)
- <downstream-task-key>: downstream propagation (update backend ref in rhtpa-release.0.3.z, blocked by upstream task)

2.2.x stream: NOT AFFECTED -- all versions ship h2 >= 0.4.8. No remediation needed.
```

_Awaiting engineer confirmation before executing any Jira mutations._
