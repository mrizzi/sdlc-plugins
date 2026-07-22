# Step 8 -- Remediation: TC-8004 (CVE-2026-33501)

## Triage Outcome

**Case A: Affected -- create remediation tasks** for the 2.1.x stream only.

The issue is unscoped and covers all streams. The version impact analysis shows:
- **2.1.x stream**: AFFECTED (h2 0.4.5, below fix threshold 0.4.8)
- **2.2.x stream**: NOT affected (h2 >= 0.4.8, at or above fix threshold)

Case B (cross-stream impact) does not apply to unscoped issues -- they cover all streams by definition.

Since the ecosystem is **Cargo** (source dependency), two remediation tasks are created for the affected 2.1.x stream: an upstream backport task and a downstream propagation subtask.

No remediation tasks are created for the 2.2.x stream because it already ships the fixed version.

---

## Task 1: Upstream Backport (2.1.x stream)

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

### Task Description

## Repository

rhtpa-backend

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

- Target branch: release/0.3.z
- **Dependency type**: direct (h2 is a direct Cargo dependency)
- The fix adds a configurable maximum header list size defaulting to 16 KiB

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.toml
- Run `cargo update -p h2` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog for h2 0.4.8)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)

---

### Jira Creation

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <upstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

---

## Task 2: Downstream Propagation (2.1.x stream)

**Summary**: Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

### Task Description

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

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)

---

### Jira Creation

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <downstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

## Jira Linkage

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

# Link downstream as blocked by upstream
jira.create_link(
  inwardIssue: <upstream-task-key>,
  outwardIssue: <downstream-task-key>,
  type: "Blocks"
)
```

## Post-Triage Summary

Add the `ai-cve-triaged` label to TC-8004 and post summary comment:

```
CVE-2026-33501 triage complete for h2 (memory exhaustion via CONTINUATION frames).

Version Impact:
| Version | h2 version | Affected? |
|---------|------------|-----------|
| 2.1.0   | 0.4.5      | YES       |
| 2.1.1   | 0.4.5      | YES       |
| 2.2.0   | 0.4.8      | NO        |
| 2.2.1   | 0.4.8      | NO        |
| 2.2.2   | --         | NO (retag of 2.2.1) |
| 2.2.3   | 0.4.9      | NO        |
| 2.2.4   | 0.4.9      | NO        |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]
RHTPA 2.2.0 removed (ships h2 0.4.8, fixed version). RHTPA 2.1.1 added (ships h2 0.4.5, vulnerable).

Outcome: Remediation tasks created for 2.1.x stream only.
- <upstream-task-key>: Upstream backport -- bump h2 to >= 0.4.8 on release/0.3.z
- <downstream-task-key>: Downstream propagation -- update rhtpa-backend ref in rhtpa-release.0.3.z (blocked by upstream task)

2.2.x stream requires no action -- all versions ship h2 >= 0.4.8.

No sibling issues found (JQL returned empty).
```

## Tasks NOT Created (2.2.x stream)

No remediation tasks are created for the 2.2.x stream because:
- All 2.2.x versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8
- h2 0.4.8 is the fixed version for CVE-2026-33501
- The stream is not affected by this vulnerability
