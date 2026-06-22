# Remediation — TC-8004

## Step 7: Triage Outcome

### Case Determination

- **2.1.x stream**: AFFECTED -- both versions (2.1.0, 2.1.1) ship h2 0.4.5 (vulnerable)
- **2.2.x stream**: NOT AFFECTED -- all versions ship h2 >= 0.4.8 (fixed)

This is **Case A** (affected -- create remediation tasks) for the **2.1.x stream only**.

No cross-stream impact notice (Case B) is needed because the 2.2.x stream is not affected -- there is nothing to alert other streams about.

### Remediation Tasks (2.1.x Stream Only)

Since h2 is a **Cargo** ecosystem (source dependency), two tasks are required for the affected 2.1.x stream:

---

#### Task 1: Upstream Backport

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Task Description**:

```markdown
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 versions before 0.4.8) must be updated
to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (build v0.3.8), RHTPA 2.1.1 (build v0.3.12)
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
- The fix adds a configurable maximum header list size defaulting to 16 KiB

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

#### Task 2: Downstream Propagation

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Task Description**:

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

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

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

---

### Jira Linkage

After creating both tasks:

1. Link upstream task to TC-8004:
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: "<upstream-task-key>",
     type: "Depend"
   )
   ```

2. Link downstream task to TC-8004:
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: "<downstream-task-key>",
     type: "Depend"
   )
   ```

3. Link downstream task as blocked by upstream task:
   ```
   jira.create_link(
     inwardIssue: "<upstream-task-key>",
     outwardIssue: "<downstream-task-key>",
     type: "Blocks"
   )
   ```

4. Transition TC-8004 to In Progress.
5. Assign TC-8004 to the current user.

### No Remediation Needed for 2.2.x Stream

The 2.2.x stream is **not affected** -- all versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8, which is at or above the fixed version. No remediation tasks are created for this stream.

### Post-Triage Summary

Add `ai-cve-triaged` label to TC-8004 and post summary comment:

```
## CVE-2026-33501 Triage Summary

### Version Impact

| Version | h2 Version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.1.0 | 0.4.5 | YES | |
| 2.1.1 | 0.4.5 | YES | |
| 2.2.0 | 0.4.8 | NO | fixed version |
| 2.2.1 | 0.4.8 | NO | fixed version |
| 2.2.2 | -- | NO | retag of 2.2.1 |
| 2.2.3 | 0.4.9 | NO | fixed version |
| 2.2.4 | 0.4.9 | NO | fixed version |

### Affects Versions Correction

[RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]
- Added RHTPA 2.1.1 (h2 0.4.5, affected)
- Removed RHTPA 2.2.0 (h2 0.4.8, not affected)

### Triage Outcome

Only the 2.1.x stream is affected. The 2.2.x stream ships h2 >= 0.4.8 (fixed) and is not affected.

Remediation tasks created for 2.1.x stream:
- <upstream-task-key>: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x) -- upstream backport on release/0.3.z
- <downstream-task-key>: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x) -- downstream propagation (blocked by <upstream-task-key>)

---
_Comment generated by `/sdlc-workflow:triage-security` skill_
```
