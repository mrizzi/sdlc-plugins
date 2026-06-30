# Remediation — TC-8004

## Triage Outcome

**Case A: Affected — create remediation tasks** for the 2.1.x stream only.

The 2.2.x stream is NOT affected (all versions ship h2 >= 0.4.8), so no remediation tasks are created for that stream.

## Affected Stream

| Stream | Affected Versions | Ecosystem | Remediation Type |
|--------|-------------------|-----------|------------------|
| 2.1.x | 2.1.0, 2.1.1 | Cargo (source dependency) | 2 tasks: upstream backport + downstream propagation |

## Remediation Tasks

Since h2 is a Cargo (source dependency) ecosystem package, two tasks are required for the affected 2.1.x stream:

### Task 1: Upstream Backport (2.1.x stream)

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

**Description**:

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 - Memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

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
- h2 is a transitive dependency via hyper — may need to bump hyper
  or other intermediate crates to pull in h2 >= 0.4.8

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

### Task 2: Downstream Propagation (2.1.x stream)

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

**Description**:

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to >= 0.4.8 on release/0.3.z. Once that PR
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

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

## Jira Linkage

1. Link upstream task to TC-8004 with link type "Depend"
2. Link downstream task to TC-8004 with link type "Depend"
3. Link downstream task as blocked by upstream task with link type "Blocks"
4. Transition TC-8004 to In Progress
5. Assign TC-8004 to current user
6. Add `ai-cve-triaged` label to TC-8004

## Sibling / Duplicate Check

JQL search for sibling issues with label CVE-2026-33501 returned **no results**. No duplicates or companion issues exist.

## Cross-Stream Impact

Since TC-8004 is unscoped and the version impact analysis covers all streams:

- **2.1.x stream**: Affected — remediation tasks created above
- **2.2.x stream**: NOT affected — no remediation needed (ships h2 >= 0.4.8)

No cross-stream remediation comment is needed because the unaffected stream (2.2.x) does not require any action. There is no Case B scenario here — the 2.2.x stream already ships the patched version, so no preemptive tasks are required.

## Post-Triage Summary Comment

```
Triage complete for CVE-2026-33501 (h2 — memory exhaustion via CONTINUATION frames).

Version Impact:

| Version | Stream | h2 Version | Affected? |
|---------|--------|------------|-----------|
| 2.1.0   | 2.1.x  | 0.4.5      | YES       |
| 2.1.1   | 2.1.x  | 0.4.5      | YES       |
| 2.2.0   | 2.2.x  | 0.4.8      | NO        |
| 2.2.1   | 2.2.x  | 0.4.8      | NO        |
| 2.2.2   | 2.2.x  | —          | NO (retag of 2.2.1) |
| 2.2.3   | 2.2.x  | 0.4.9      | NO        |
| 2.2.4   | 2.2.x  | 0.4.9      | NO        |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]

Outcome: Remediation tasks created for 2.1.x stream only.
- Upstream backport task: bump h2 to >= 0.4.8 on release/0.3.z
- Downstream propagation task: update backend ref in rhtpa-release.0.3.z (blocked by upstream task)

2.2.x stream is not affected — all versions ship h2 >= 0.4.8 (at or above fix threshold).
No sibling or duplicate issues found.
```
