# Step 8 -- Remediation

## Triage Outcome: Case A -- Affected (create remediation tasks)

The version impact analysis shows that **only the 2.1.x stream** is affected. All 2.2.x versions ship h2 >= 0.4.8 and are not vulnerable.

Since the issue is **unscoped**, Case B (cross-stream impact) does not apply -- unscoped issues cover all streams by definition, so there are no "other streams outside scope" to flag. Remediation tasks are created only for the actually affected stream (2.1.x).

## Affected Stream

| Stream | Versions Affected | h2 Version Shipped | Fix Required |
|--------|-------------------|--------------------|--------------|
| 2.1.x | 2.1.0, 2.1.1 | 0.4.5 | Bump to >= 0.4.8 |
| 2.2.x | _(none)_ | 0.4.8+ | _(already fixed)_ |

## Remediation Tasks (2.1.x stream only)

Since h2 is a **Cargo** (source dependency) ecosystem package, two tasks are created: an upstream backport task and a downstream propagation subtask.

### Task 1: Upstream Backport

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

```markdown
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

- Target branch: release/0.3.z
- **Dependency type**: determined by lock file analysis (direct or transitive)
- The fix adds a configurable maximum header list size defaulting to 16 KiB
- h2 0.4.8 is already available upstream

### Remediation approach

- Update h2 dependency to >= 0.4.8 in Cargo.toml / Cargo.lock
- If h2 is a transitive dependency, identify the direct dependency that pulls it in and bump that first
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

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

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-33501

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-33501 fix from the upstream backport task.

The upstream backport bumps h2 to >= 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

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

1. Link upstream backport task to TC-8004 with type "Depend"
2. Link downstream propagation task to TC-8004 with type "Depend"
3. Link downstream propagation task as blocked by upstream backport task with type "Blocks"
4. Transition TC-8004 to In Progress
5. Add `ai-cve-triaged` label to TC-8004

## No Remediation for 2.2.x

The 2.2.x stream requires no remediation tasks. All versions in this stream ship h2 >= 0.4.8:

| Version | h2 Version | Status |
|---------|------------|--------|
| 2.2.0 | 0.4.8 | Already at fix threshold |
| 2.2.1 | 0.4.8 | Already at fix threshold |
| 2.2.2 | _(retag of 2.2.1)_ | Already at fix threshold |
| 2.2.3 | 0.4.9 | Above fix threshold |
| 2.2.4 | 0.4.9 | Above fix threshold |

## Post-Triage Summary Comment

```
CVE-2026-33501 triage complete for TC-8004.

Version impact (h2 < 0.4.8):

| Version | h2 | Affected? |
|---------|----|-----------|
| 2.1.0 | 0.4.5 | YES |
| 2.1.1 | 0.4.5 | YES |
| 2.2.0 | 0.4.8 | NO |
| 2.2.1 | 0.4.8 | NO |
| 2.2.2 | -- | NO (retag of 2.2.1) |
| 2.2.3 | 0.4.9 | NO |
| 2.2.4 | 0.4.9 | NO |

Affects Versions corrected: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1]

Outcome: Remediation required for 2.1.x stream only.
- Upstream backport task: bump h2 to >= 0.4.8 on release/0.3.z
- Downstream propagation task: update backend ref in rhtpa-release.0.3.z

2.2.x stream already ships patched h2 -- no action needed.
```
