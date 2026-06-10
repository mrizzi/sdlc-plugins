# Step 7 -- Remediation

## Triage Outcome: Case A -- Affected (2.1.x stream only)

The version impact analysis shows **mixed impact**:
- **2.1.x stream**: ALL versions affected (RHTPA 2.1.0, RHTPA 2.1.1) -- h2 0.4.5 < 0.4.8
- **2.2.x stream**: NO versions affected -- all ship h2 >= 0.4.8

Remediation tasks are proposed **only for the 2.1.x stream**. No tasks are needed for the 2.2.x stream since it already ships the fixed version.

### Cross-Stream Impact Notice

A cross-stream impact notice is **not needed** for this issue. TC-8004 is unscoped (no stream suffix), so it covers all streams by definition. There are no "other streams outside the issue's scope" to notify about.

## Proposed Remediation Tasks

Since h2 is a **Cargo** (source dependency) ecosystem package, two tasks are required per the remediation template: an upstream backport task and a downstream propagation subtask with a Blocks dependency.

---

### Task 1: Upstream Backport (2.1.x stream)

**Proposed Jira creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Proposed Task Description:**

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: Memory exhaustion via CONTINUATION frames in h2.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed
version (0.4.8+).

Affected versions: RHTPA 2.1.0 (v0.3.8, h2 0.4.5), RHTPA 2.1.1 (v0.3.12, h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: hyperium/h2#812
Advisory: GHSA-2026-kv8p-r3n7

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
```

---

### Task 2: Downstream Propagation (2.1.x stream)

**Proposed Jira creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Proposed Task Description:**

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps h2 to 0.4.8 on
release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

---

## Proposed Jira Linkage

After creating both tasks:

1. **Link** upstream task to TC-8004:
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

2. **Link** downstream task to TC-8004:
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

3. **Link** downstream task as blocked by upstream task:
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

4. **Transition** TC-8004 to In Progress.

5. **Assign** TC-8004 to the current user.

6. **Add label** `ai-cve-triaged` to TC-8004.

## Why No 2.2.x Remediation

The 2.2.x stream requires no remediation tasks because:
- RHTPA 2.2.0 (v0.4.5) ships h2 0.4.8 -- at the fixed version
- RHTPA 2.2.1 (v0.4.8) ships h2 0.4.8 -- at the fixed version
- RHTPA 2.2.2 (v0.4.9) is a retag of 2.2.1 -- same as 2.2.1
- RHTPA 2.2.3 (v0.4.11) ships h2 0.4.9 -- above the fixed version
- RHTPA 2.2.4 (v0.4.12) ships h2 0.4.9 -- above the fixed version

All 2.2.x versions ship h2 >= 0.4.8, which is outside the vulnerable range.

## Post-Triage Summary (proposed comment on TC-8004)

```
## CVE-2026-33501 Triage Summary

### Version Impact

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | YES | < 0.4.8 |
| 2.1.1 | 2.1.x | 0.4.5 | YES | < 0.4.8 |
| 2.2.0 | 2.2.x | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.1 | 2.2.x | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.9 | NO | >= 0.4.8 (fixed) |
| 2.2.4 | 2.2.x | 0.4.9 | NO | >= 0.4.8 (fixed) |

### Affects Versions Correction

[RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]

### Triage Outcome

Remediation required for 2.1.x stream only. 2.2.x stream already ships h2 >= 0.4.8.

### Remediation Tasks

- <upstream-task-key>: Upstream backport -- bump h2 to 0.4.8 on release/0.3.z (2.1.x)
- <downstream-task-key>: Downstream propagation -- update rhtpa-backend ref in rhtpa-release.0.3.z (blocked by <upstream-task-key>)
```

All actions above are **proposals** pending engineer confirmation before execution.
