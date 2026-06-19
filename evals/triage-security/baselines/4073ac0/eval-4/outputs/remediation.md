# Step 7 -- Remediation

## Triage Outcome

**Case A: Affected -- create remediation tasks**

The version impact analysis shows that **2.1.x stream versions are affected**
(h2 0.4.5, within the vulnerable range < 0.4.8). The 2.2.x stream is **not
affected** (all versions ship h2 >= 0.4.8).

Since the issue is **unscoped**, remediation tasks are created only for streams
with actually affected versions. The 2.2.x stream requires no remediation.

**No cross-stream impact notice is needed.** The issue is unscoped (covers all
streams), so there is no "other stream outside this issue's scope" to notify
about. Cross-stream impact notices (Case B) only apply to stream-scoped issues
where impact is discovered outside the issue's scope.

## Ecosystem

The vulnerable library (h2) is a **Cargo** (Rust) dependency -- a source
dependency ecosystem. Per the remediation templates, this requires **two tasks**:

1. **Upstream backport task** -- bump h2 in the source repository (backend)
2. **Downstream propagation subtask** -- update the backend reference in the
   Konflux release repo (rhtpa-release.0.3.z)

Tasks are created only for the **2.1.x stream** (the only affected stream).

---

## Proposed Task 1: Upstream Backport (2.1.x)

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

### Task Description

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed
version (0.4.8+).

Affected versions: RHTPA 2.1.0 (tag v0.3.8), RHTPA 2.1.1 (tag v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- h2 is a transitive dependency via hyper -- may need to bump hyper
  or adjust version constraints in Cargo.toml
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

## Proposed Task 2: Downstream Propagation (2.1.x)

**Proposed Jira creation:**

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

The upstream backport bumps h2 to >= 0.4.8 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

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

---

## Proposed Jira Linkage

After task creation, the following links would be established:

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

5. Assign TC-8004 to the current user.

## Proposed Labels

Add `ai-cve-triaged` label to TC-8004:
```
jira.edit_issue("TC-8004", fields={
  "labels": ["CVE-2026-33501", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

## Proposed Post-Triage Summary Comment

The following comment would be posted to TC-8004:

```
## Triage Summary -- CVE-2026-33501 (h2 < 0.4.8)

### Version Impact

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | YES | < 0.4.8 |
| 2.1.1 | 2.1.x | 0.4.5 | YES | < 0.4.8 |
| 2.2.0 | 2.2.x | 0.4.8 | NO | >= 0.4.8 (fixed version) |
| 2.2.1 | 2.2.x | 0.4.8 | NO | >= 0.4.8 (fixed version) |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.9 | NO | >= 0.4.8 |
| 2.2.4 | 2.2.x | 0.4.9 | NO | >= 0.4.8 |

### Affects Versions Correction

Corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]
- Removed RHTPA 2.2.0 (ships h2 0.4.8, not affected)
- Added RHTPA 2.1.1 (ships h2 0.4.5, affected)

### Triage Outcome

Remediation tasks created for 2.1.x stream (the only affected stream):
- <upstream-task-key>: Upstream backport -- bump h2 to >= 0.4.8 on release/0.3.z
- <downstream-task-key>: Downstream propagation -- update backend ref in
  rhtpa-release.0.3.z (blocked by upstream task)

2.2.x stream requires no remediation (all versions ship h2 >= 0.4.8).

---
_This triage was performed by the triage-security skill._
```

## Summary of Proposed Actions

| # | Action | Status |
|---|--------|--------|
| 1 | Correct Affects Versions to [RHTPA 2.1.0, RHTPA 2.1.1] | Proposed |
| 2 | Create upstream backport task for 2.1.x stream | Proposed |
| 3 | Create downstream propagation task for 2.1.x stream | Proposed |
| 4 | Link tasks to TC-8004 | Proposed |
| 5 | Link downstream task as blocked by upstream task | Proposed |
| 6 | Add ai-cve-triaged label | Proposed |
| 7 | Post triage summary comment | Proposed |
| 8 | Transition TC-8004 to In Progress | Proposed |
| 9 | Assign TC-8004 to current user | Proposed |

No actions are proposed for the 2.2.x stream -- it is not affected.
