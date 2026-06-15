# Step 7 -- Remediation: TC-8004

## Triage Outcome: Case A -- Affected (2.1.x stream only)

The version impact analysis shows that only the **2.1.x stream** is affected. The 2.2.x stream ships h2 >= 0.4.8 (the fixed version) in all releases and requires no remediation.

Since h2 is a **Cargo** (source dependency) ecosystem package, two remediation tasks are required for the affected 2.1.x stream:

1. **Upstream backport task** -- bump h2 in the backend source repo on the release/0.3.z branch
2. **Downstream propagation subtask** -- update the backend source reference in the Konflux release repo rhtpa-release.0.3.z

No cross-stream impact notice is generated because the issue is **unscoped** (it covers all streams by definition, so there is no "other stream outside this issue's scope").

---

## Task 1: Upstream Backport (2.1.x stream)

### Jira Issue Creation (proposed)

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

Affected versions: RHTPA 2.1.0 (build v0.3.8, h2 0.4.5), RHTPA 2.1.1 (build v0.3.12, h2 0.4.5)
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

## Task 2: Downstream Propagation (2.1.x stream)

### Jira Issue Creation (proposed)

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

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport task bumps h2 to >= 0.4.8 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
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

1. Link upstream task to TC-8004:
   ```
   jira.create_link(inwardIssue: "TC-8004", outwardIssue: <upstream-task-key>, type: "Depend")
   ```

2. Link downstream task to TC-8004:
   ```
   jira.create_link(inwardIssue: "TC-8004", outwardIssue: <downstream-task-key>, type: "Depend")
   ```

3. Link downstream task as blocked by upstream task:
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

4. Transition TC-8004 to In Progress.

5. Assign TC-8004 to current user.

6. Add `ai-cve-triaged` label to TC-8004.

## Post-Triage Summary Comment (proposed)

```
## CVE-2026-33501 Triage Summary

### Version Impact

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | YES | < 0.4.8 |
| 2.1.1 | 2.1.x | 0.4.5 | YES | < 0.4.8 |
| 2.2.0 | 2.2.x | 0.4.8 | NO | >= 0.4.8 (fixed version) |
| 2.2.1 | 2.2.x | 0.4.8 | NO | >= 0.4.8 |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.9 | NO | >= 0.4.8 |
| 2.2.4 | 2.2.x | 0.4.9 | NO | >= 0.4.8 |

### Affects Versions Correction

[RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]

### Triage Outcome

Remediation required for 2.1.x stream only. 2.2.x stream ships h2 >= 0.4.8 and is not affected.

### Remediation Tasks

- <upstream-task-key>: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x) -- upstream backport on release/0.3.z
- <downstream-task-key>: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x) -- downstream propagation, blocked by <upstream-task-key>

---
_This triage was performed by the triage-security skill._
```
