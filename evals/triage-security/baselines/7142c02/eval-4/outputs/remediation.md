# Step 7 -- Remediation: TC-8004

## Triage Outcome

**Case A: Affected -- create remediation tasks for 2.1.x stream only.**

The version impact analysis shows:
- **2.1.x stream**: AFFECTED (h2 0.4.5, below fix threshold 0.4.8)
- **2.2.x stream**: NOT affected (h2 0.4.8+, at or above fix threshold)

Since this is an **unscoped** issue (no stream suffix), all streams were analyzed. Only the 2.1.x stream requires remediation. No cross-stream impact notice is generated because the issue is unscoped -- it already covers all streams by definition.

The ecosystem is **Cargo** (source dependency), so two tasks are required for the affected 2.1.x stream:
1. Upstream backport task (fix h2 in the source repo)
2. Downstream propagation subtask (update the reference in the Konflux release repo)

---

## Task 1: Upstream Backport (2.1.x)

### Jira Creation

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

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- h2 is a transitive dependency via hyper -- may need to bump hyper
  or adjust dependency resolution to pull in h2 >= 0.4.8
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

## Task 2: Downstream Propagation (2.1.x)

### Jira Creation

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

The upstream backport bumps h2 to 0.4.8+ on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next
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

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)

---

## Jira Linkage

After task creation, the following links would be established:

1. **Upstream task -> TC-8004**: Link type "Depend"
   ```
   jira.create_link(inwardIssue: "TC-8004", outwardIssue: <upstream-task-key>, type: "Depend")
   ```

2. **Downstream task -> TC-8004**: Link type "Depend"
   ```
   jira.create_link(inwardIssue: "TC-8004", outwardIssue: <downstream-task-key>, type: "Depend")
   ```

3. **Downstream task blocked by upstream task**: Link type "Blocks"
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```

4. **Transition** TC-8004 to In Progress.

5. **Assign** TC-8004 to current user.

6. **Add label** `ai-cve-triaged` to TC-8004.

## Why No Cross-Stream Impact Notice

This issue is **unscoped** (no stream suffix in the summary). An unscoped issue already covers all streams by definition. Cross-stream impact notices (Case B) are only generated for **stream-scoped** issues where the analysis reveals impact in streams outside the issue's scope. Since this issue has no scope restriction, there are no "other streams outside scope" to notify about.

## Why No Remediation for 2.2.x

The 2.2.x stream ships h2 0.4.8 or later in all versions:
- 2.2.0: h2 0.4.8 (fix threshold)
- 2.2.1: h2 0.4.8 (fix threshold)
- 2.2.2: retag of 2.2.1
- 2.2.3: h2 0.4.9 (above fix threshold)
- 2.2.4: h2 0.4.9 (above fix threshold)

No version in the 2.2.x stream ships a vulnerable h2 version, so no remediation task is needed for this stream.

## Post-Triage Summary Comment

The following summary comment would be posted to TC-8004:

```
Triage complete for CVE-2026-33501 (h2 memory exhaustion via CONTINUATION frames).

Version Impact:

| Version | Stream | h2 version | Affected? |
|---------|--------|------------|-----------|
| 2.1.0   | 2.1.x  | 0.4.5      | YES       |
| 2.1.1   | 2.1.x  | 0.4.5      | YES       |
| 2.2.0   | 2.2.x  | 0.4.8      | NO        |
| 2.2.1   | 2.2.x  | 0.4.8      | NO        |
| 2.2.2   | 2.2.x  | --         | NO (retag of 2.2.1) |
| 2.2.3   | 2.2.x  | 0.4.9      | NO        |
| 2.2.4   | 2.2.x  | 0.4.9      | NO        |

Affects Versions corrected: removed RHTPA 2.2.0 (not affected), added RHTPA 2.1.1 (affected).

Remediation tasks created for 2.1.x stream:
- <upstream-task-key>: Upstream backport -- bump h2 to 0.4.8 on release/0.3.z
- <downstream-task-key>: Downstream propagation -- update backend ref in rhtpa-release.0.3.z (blocked by <upstream-task-key>)

No remediation needed for 2.2.x stream (ships h2 0.4.8+).
```
