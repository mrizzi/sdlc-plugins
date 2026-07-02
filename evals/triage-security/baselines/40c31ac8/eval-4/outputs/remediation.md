# Remediation -- TC-8004

## Triage Outcome

**Case A: Affected** -- the 2.1.x stream has supported versions that ship the vulnerable dependency (h2 < 0.4.8). Remediation tasks are required for the 2.1.x stream only.

The 2.2.x stream is NOT affected (all versions ship h2 >= 0.4.8). No remediation tasks are created for 2.2.x.

No sibling issues exist (JQL returned empty). No duplicate or cross-stream companion issues found.

## Ecosystem: Cargo (Source Dependency)

Since h2 is a Cargo (Rust) dependency, two tasks are required per affected stream:
1. **Upstream backport task** -- bump h2 in the source repository (backend)
2. **Downstream propagation task** -- update the backend source reference in the Konflux release repo

## Remediation Tasks for Stream 2.1.x

### Task 1: Upstream Backport

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

```markdown
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed
version (0.4.8+).

Affected versions: RHTPA 2.1.0 (v0.3.8), RHTPA 2.1.1 (v0.3.12)
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

### Task 2: Downstream Propagation

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release
repo so the next build ships the fix.

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

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

## Jira Linkage Plan

1. Link upstream backport task to TC-8004 with link type "Depend"
2. Link downstream propagation task to TC-8004 with link type "Depend"
3. Link downstream propagation task as blocked by upstream backport task with link type "Blocks"
4. Transition TC-8004 to In Progress
5. Add `ai-cve-triaged` label to TC-8004

## Streams Not Requiring Remediation

| Stream | Reason |
|--------|--------|
| 2.2.x | All versions ship h2 >= 0.4.8 (fixed). No remediation needed. |

## Post-Triage Summary Comment

```
Triage complete for CVE-2026-33501 (h2 < 0.4.8).

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

Outcome: Remediation required for 2.1.x stream only.
Remediation tasks created:
- <upstream-task-key> (upstream backport: bump h2 to >= 0.4.8 on release/0.3.z)
- <downstream-task-key> (downstream propagation: update backend ref in rhtpa-release.0.3.z, blocked by <upstream-task-key>)

2.2.x stream: NOT affected -- all versions ship h2 >= 0.4.8.
```
