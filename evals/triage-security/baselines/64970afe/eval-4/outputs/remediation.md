# Step 8 -- Remediation: TC-8004 (CVE-2026-33501)

## Triage Outcome

**Case A: Affected -- create remediation tasks** for the 2.1.x stream only.

The 2.2.x stream is NOT affected (all versions ship h2 >= 0.4.8), so no remediation tasks are created for that stream.

Since this is an unscoped issue and Case B (cross-stream impact) applies only to scoped issues, Case B is skipped entirely. The 2.2.x stream's non-affected status means there is nothing to remediate there regardless.

## Ecosystem and Task Structure

- Ecosystem: **Cargo** (source dependency)
- Task structure: **two tasks** per affected stream -- upstream backport + downstream propagation
- Affected stream(s): **2.1.x only**

## Task 1: Upstream Backport (2.1.x stream)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <see description below>,
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

Affected versions: RHTPA 2.1.0 (tag v0.3.8, h2 0.4.5), RHTPA 2.1.1 (tag v0.3.12, h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct or transitive -- verify by inspecting Cargo.toml at the pinned tag
- Update h2 dependency to >= 0.4.8 in Cargo.lock (and Cargo.toml if direct dependency)
- The fix adds a configurable maximum header list size defaulting to 16 KiB
- If h2 is a transitive dependency, identify the direct dependency that pulls it in and bump that first; fall back to pinning h2 directly via `cargo add h2@0.4.8` if needed

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

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
  description: <see description below>,
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

The upstream backport bumps h2 to >= 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: carried forward from upstream task
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

## Jira Linkage

After creating both tasks:

1. Link upstream backport task to TC-8004:
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

2. Link downstream propagation task to TC-8004:
   ```
   jira.create_link(
     inwardIssue: "TC-8004",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

3. Link downstream task as blocked by upstream task:
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

4. Transition TC-8004 to In Progress.

5. Add `ai-cve-triaged` label to TC-8004.

## Streams NOT Requiring Remediation

| Stream | Reason |
|--------|--------|
| 2.2.x | All versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8 (the fixed version). No remediation needed. |

## Post-Triage Summary Comment

The following summary comment would be posted to TC-8004:

---

**CVE-2026-33501 Triage Summary -- h2 memory exhaustion via CONTINUATION frames**

**Version Impact:**

| Version | Stream | h2 version | Affected? |
|---------|--------|------------|-----------|
| 2.1.0 | 2.1.x | 0.4.5 | YES |
| 2.1.1 | 2.1.x | 0.4.5 | YES |
| 2.2.0 | 2.2.x | 0.4.8 | NO |
| 2.2.1 | 2.2.x | 0.4.8 | NO |
| 2.2.2 | 2.2.x | -- | NO (retag of 2.2.1) |
| 2.2.3 | 2.2.x | 0.4.9 | NO |
| 2.2.4 | 2.2.x | 0.4.9 | NO |

**Affects Versions Correction:** Removed RHTPA 2.2.0 (not affected -- ships h2 0.4.8). Added RHTPA 2.1.1 (affected -- ships h2 0.4.5). Final: RHTPA 2.1.0, RHTPA 2.1.1.

**Triage Outcome:** Remediation tasks created for the 2.1.x stream. The 2.2.x stream is not affected.

**Remediation Tasks:**
- Upstream backport task: bump h2 to >= 0.4.8 on release/0.3.z (blocked by upstream fix PR hyperium/h2#812)
- Downstream propagation task: update backend ref in rhtpa-release.0.3.z (blocked by upstream backport)

**Sibling Issues:** JQL search returned empty -- no sibling Vulnerability issues found for CVE-2026-33501.
