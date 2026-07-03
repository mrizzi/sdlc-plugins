# Remediation — TC-8004

## Triage Outcome

**Case A: Affected** — the 2.1.x stream ships vulnerable h2 versions. Remediation tasks are required for stream 2.1.x only.

The 2.2.x stream is NOT affected (all versions ship h2 >= 0.4.8). No remediation tasks are created for stream 2.2.x. No Case B (cross-stream impact) applies because the other stream is not affected.

## Ecosystem

Cargo (source dependency) — two tasks required per affected stream:
1. Upstream backport task (fix in source repo rhtpa-backend)
2. Downstream propagation subtask (update reference in Konflux release repo rhtpa-release.0.3.z)

## Sibling / Duplicate Check (Step 4)

JQL search for sibling Vulnerability issues with label `CVE-2026-33501` returned **no results**. No duplicates or cross-stream companions exist.

## Task 1: Upstream Backport (stream 2.1.x)

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

### Task Description

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 - Memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 versions before 0.4.8) must be updated
to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (tag v0.3.8), RHTPA 2.1.1 (tag v0.3.12)
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
```

### Jira Creation

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <upstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

---

## Task 2: Downstream Propagation (stream 2.1.x)

**Summary**: Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

### Task Description

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

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

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

### Jira Creation

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <downstream-task-description>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

## Jira Linkage

After creating both tasks:

1. Link upstream task to Vulnerability issue:
   ```
   jira.create_link(inwardIssue: "TC-8004", outwardIssue: <upstream-task-key>, type: "Depend")
   ```

2. Link downstream subtask as blocked by upstream task:
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

3. Link downstream task to Vulnerability issue:
   ```
   jira.create_link(inwardIssue: "TC-8004", outwardIssue: <downstream-task-key>, type: "Depend")
   ```

## Post-Triage Summary

1. Add label `ai-cve-triaged` to TC-8004.

2. Post summary comment to TC-8004:

```
Triage complete for CVE-2026-33501 (h2 — Memory exhaustion via CONTINUATION frames).

Version Impact:

| Version | Stream | h2 Version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | YES | < 0.4.8 |
| 2.1.1 | 2.1.x | 0.4.5 | YES | < 0.4.8 |
| 2.2.0 | 2.2.x | 0.4.8 | NO | = 0.4.8 (fixed) |
| 2.2.1 | 2.2.x | 0.4.8 | NO | = 0.4.8 (fixed) |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.9 | NO | > 0.4.8 (fixed) |
| 2.2.4 | 2.2.x | 0.4.9 | NO | > 0.4.8 (fixed) |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].

Outcome: Remediation tasks created for stream 2.1.x (affected).
Stream 2.2.x is not affected — all versions ship h2 >= 0.4.8.

Remediation tasks:
- <upstream-task-key>: Upstream backport — bump h2 to 0.4.8 on release/0.3.z
- <downstream-task-key>: Downstream propagation — update rhtpa-backend ref in rhtpa-release.0.3.z (blocked by <upstream-task-key>)
```
