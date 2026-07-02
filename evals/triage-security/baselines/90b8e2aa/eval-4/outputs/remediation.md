# Step 8 -- Remediation

## Triage Outcome: Case A (Affected) -- 2.1.x stream only

The version impact analysis shows that only the **2.1.x stream** is affected. The 2.2.x stream ships h2 >= 0.4.8 (the fixed version) across all its releases and requires no remediation.

No sibling issues exist (JQL returned empty). No preemptive tasks found.

## Remediation Tasks (2.1.x stream only)

Since h2 is a **Cargo** (source dependency) ecosystem package, two tasks are required for the affected 2.1.x stream: an upstream backport task and a downstream propagation subtask.

No tasks are created for the 2.2.x stream because it is not affected.

---

### Task 1: Upstream Backport (source repo fix)

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

#### Description

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

- Update h2 dependency to >= 0.4.8 in Cargo.lock (and Cargo.toml if directly specified)
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)

---

### Task 2: Downstream Propagation (Konflux release repo update)

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

#### Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8+
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
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

## Jira Linkage Plan

1. Link upstream backport task to TC-8004 with link type "Depend"
2. Link downstream propagation task to TC-8004 with link type "Depend"
3. Link downstream propagation task as blocked by upstream backport task with link type "Blocks"
4. Add `ai-cve-triaged` label to TC-8004

## Post-Triage Summary Comment

To be posted on TC-8004:

> **Triage Summary for CVE-2026-33501 (h2 < 0.4.8)**
>
> **Version Impact:**
>
> | Version | h2 version | Affected? |
> |---------|------------|-----------|
> | 2.1.0 | 0.4.5 | YES |
> | 2.1.1 | 0.4.5 | YES |
> | 2.2.0 | 0.4.8 | NO |
> | 2.2.1 | 0.4.8 | NO |
> | 2.2.2 | _(retag)_ | NO |
> | 2.2.3 | 0.4.9 | NO |
> | 2.2.4 | 0.4.9 | NO |
>
> **Affects Versions corrected**: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]
>
> **Outcome**: Remediation tasks created for 2.1.x stream (the only affected stream).
> 2.2.x stream ships h2 >= 0.4.8 -- not affected, no remediation needed.
>
> **Remediation tasks**:
> - Upstream backport task (bump h2 to 0.4.8 on release/0.3.z)
> - Downstream propagation task (update backend ref in rhtpa-release.0.3.z, blocked by upstream task)
