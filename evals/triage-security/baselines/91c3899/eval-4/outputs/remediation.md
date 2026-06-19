# Step 7 -- Remediation: TC-8004

## Triage Decision

**Case A: Affected -- create remediation tasks**

The version impact analysis shows that 2.1.x stream versions are affected (h2 0.4.5 < 0.4.8). The 2.2.x stream is NOT affected (ships h2 >= 0.4.8). Remediation tasks are created **only for the affected 2.1.x stream**.

## Cross-Stream Impact Notice

A cross-stream impact notice is **NOT generated** for this issue. The issue is **unscoped** (no stream suffix in the summary), meaning it already covers all streams by definition. Cross-stream notices are only relevant for stream-scoped issues (those with a stream suffix like `[rhtpa-2.1]`) where the analysis discovers impact outside the issue's scope. Since this unscoped issue already encompasses both 2.1.x and 2.2.x streams, there are no "other streams outside scope" to report on.

## Duplicate/Sibling Check (Step 4)

JQL search for sibling Vulnerability issues with the same CVE:
```
project = TC AND issuetype = 10024 AND labels = CVE-2026-33501 AND key != TC-8004
```

**Result**: No sibling issues found. This is the only Vulnerability issue tracking CVE-2026-33501.

## Ecosystem and Task Structure

- **Ecosystem**: Cargo (source dependency)
- **Task structure**: Two tasks per affected stream -- upstream backport + downstream propagation
- **Affected streams**: 2.1.x only (2.2.x already ships patched h2)

Since only the 2.1.x stream is affected, exactly **two remediation tasks** are created.

## Remediation Task 1: Upstream Backport (2.1.x)

### Jira Issue Creation

```
upstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Task Description

```markdown
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: Memory exhaustion via CONTINUATION frames in h2.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (v0.3.8, h2 0.4.5), RHTPA 2.1.1 (v0.3.12, h2 0.4.5)
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
- The fix adds a configurable maximum header list size (16 KiB default)
  to prevent unbounded memory allocation from CONTINUATION frames

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

## Remediation Task 2: Downstream Propagation (2.1.x)

### Jira Issue Creation

```
downstream_task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

### Task Description

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.8 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

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

## Jira Linkage

After task creation:

1. Link upstream task to TC-8004:
   ```
   jira.create_link(inwardIssue: "TC-8004", outwardIssue: <upstream-task-key>, type: "Depend")
   ```

2. Link downstream task to TC-8004:
   ```
   jira.create_link(inwardIssue: "TC-8004", outwardIssue: <downstream-task-key>, type: "Depend")
   ```

3. Link downstream as blocked by upstream:
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

4. Transition TC-8004 to In Progress.

5. Assign TC-8004 to current user.

6. Add comment to TC-8004:
   > Remediation tasks created: <upstream-task-key> (upstream backport: bump h2 to 0.4.8 on release/0.3.z), <downstream-task-key> (downstream propagation: update rhtpa-backend ref in rhtpa-release.0.3.z, blocked by <upstream-task-key>).

## Why No 2.2.x Remediation

The 2.2.x stream does **not** require remediation tasks because all 2.2.x versions already ship h2 >= 0.4.8:

| Version | h2 Version | Status |
|---------|------------|--------|
| RHTPA 2.2.0 | 0.4.8 | Already patched |
| RHTPA 2.2.1 | 0.4.8 | Already patched |
| RHTPA 2.2.2 | (retag of 2.2.1) | Already patched |
| RHTPA 2.2.3 | 0.4.9 | Already patched |
| RHTPA 2.2.4 | 0.4.9 | Already patched |

No action is needed for the 2.2.x stream. The vulnerability was never present in any released 2.2.x version.

## Post-Triage Actions

1. **Add label**: `ai-cve-triaged` to TC-8004
2. **Post summary comment** to TC-8004 with:
   - Version impact table (mixed: 2.1.x affected, 2.2.x not affected)
   - Affects Versions correction (removed RHTPA 2.2.0, added RHTPA 2.1.1)
   - Remediation tasks created (upstream + downstream for 2.1.x only)
