# Step 7 -- Remediation

## Triage Outcome: Case A -- Affected (2.1.x stream only)

The version impact analysis shows MIXED results. Only the 2.1.x stream is affected (RHTPA 2.1.0 and RHTPA 2.1.1 ship h2 0.4.5, which is within the vulnerable range < 0.4.8). The 2.2.x stream already ships h2 >= 0.4.8 and requires no remediation.

Since this issue is UNSCOPED (no stream suffix), it covers all streams by definition. No cross-stream impact notice (Case B) is needed -- Case B applies only to scoped issues where other streams outside the issue's scope are also affected.

## Ecosystem

**Cargo** (source dependency) -- requires two tasks: an upstream backport task and a downstream propagation subtask.

---

## Proposed Remediation Tasks

### Task 1: Upstream Backport -- bump h2 to >= 0.4.8 on release/0.3.z

**Proposed Jira issue creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Proposed task description:**

#### Repository

backend (rhtpa-backend)

#### Target Branch

release/0.3.z

#### Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (v0.3.8, h2 0.4.5), RHTPA 2.1.1 (v0.3.12, h2 0.4.5)
Source commits: v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

#### Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock (and Cargo.toml if directly specified)
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

#### Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

#### Test Requirements

- [ ] Existing test suite passes with the updated dependency

#### Dependencies

- Depends on: TC-8004 (parent Vulnerability tracking issue)

---

### Task 2: Downstream Propagation -- update backend ref in rhtpa-release.0.3.z

**Proposed Jira issue creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-33501"]
)
```

**Proposed task description:**

#### Repository

rhtpa-release.0.3.z

#### Target Branch

main

#### Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-33501 fix from the upstream backport task.

The upstream backport task bumps h2 to >= 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

#### Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

#### Acceptance Criteria

- [ ] backend reference updated to include the h2 >= 0.4.8 fix
- [ ] Konflux rebuild triggers new container image

#### Test Requirements

- [ ] Container image builds successfully with the updated reference

#### Dependencies

- Blocked by: upstream backport task (upstream backport must merge first)
- Depends on: TC-8004 (parent Vulnerability tracking issue)

---

## Proposed Jira Linkage

1. Link upstream backport task to TC-8004 (Vulnerability) with "Depend" link type
2. Link downstream propagation task to TC-8004 (Vulnerability) with "Depend" link type
3. Link downstream propagation task as blocked by upstream backport task with "Blocks" link type
4. Transition TC-8004 to In Progress
5. Assign TC-8004 to current user
6. Add `ai-cve-triaged` label to TC-8004

## Streams NOT requiring remediation

- **2.2.x**: All versions (RHTPA 2.2.0 through RHTPA 2.2.4) ship h2 >= 0.4.8. No tasks created for this stream.
