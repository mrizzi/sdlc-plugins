# Step 8 -- Remediation: CVE-2026-99001 (criterion)

## Triage Outcome

- **Case A**: Affected -- all 2.2.x versions ship criterion 0.5.1 (below fix threshold 0.5.2)
- **Case B**: Cross-stream impact -- 2.1.x stream is also affected
- Ecosystem: **Cargo** (source dependency) -- requires **two tasks** per stream (upstream backport + downstream propagation)
- **Dev-dependency override**: criterion is dev-only; all tasks carry `dev-dependency` label and Normal priority

---

## Case A: Remediation Tasks for 2.2.x Stream (in scope)

### Task 1: Upstream Backport (2.2.x)

**Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal (dev-dependency override -- CVE severity Medium/5.3 does not apply)

#### Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: path traversal in benchmark output in the criterion crate.
The vulnerable dependency (criterion < 0.5.2) must be updated to the fixed version (0.5.2+).

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

Affected versions: 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12

Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct dev-dependency
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) -- NOT shipped in production builds. Used for benchmarks only.

### Remediation approach (direct dependency)

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml `[dev-dependencies]`
- Run `cargo update -p criterion` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)

---

### Task 2: Downstream Propagation (2.2.x)

**Summary**: Propagate CVE-2026-99001 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal (dev-dependency override)

#### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99001 fix from the upstream backport task.

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

The upstream backport bumps criterion to 0.5.2 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
- **Dependency type**: direct dev-dependency -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)

---

## Case B: Cross-Stream Preemptive Tasks for 2.1.x Stream

The 2.1.x stream is also affected (criterion 0.5.1 in all versions) but has no stream-specific CVE Jira. Preemptive remediation tasks are created with the `security-preemptive` label and linked to TC-8050 via "Related" (not "Depend").

### Task 3: Upstream Backport -- Preemptive (2.1.x)

**Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`, `security-preemptive`

**Priority**: Normal (dev-dependency override)

**Link type**: Related (to TC-8050, preemptive -- not Depend)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8050 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-99001: path traversal in benchmark output in the criterion crate.
The vulnerable dependency (criterion < 0.5.2) must be updated to the fixed version (0.5.2+).

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

Affected versions: 2.1.0, 2.1.1
Source commit(s): v0.3.8, v0.3.12

Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct dev-dependency
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) -- NOT shipped in production builds. Used for benchmarks only.

### Remediation approach (direct dependency)

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml `[dev-dependencies]`
- Run `cargo update -p criterion` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8050 (originating CVE, stream 2.2.x -- preemptive cross-stream task)

---

### Task 4: Downstream Propagation -- Preemptive (2.1.x)

**Summary**: Propagate CVE-2026-99001 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`, `security-preemptive`

**Priority**: Normal (dev-dependency override)

**Link type**: Related (to TC-8050, preemptive)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8050 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-99001 fix from the upstream backport task.

This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only).

The upstream backport bumps criterion to 0.5.2 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag)
- **Dependency type**: direct dev-dependency -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: preemptive upstream backport task (2.1.x) (upstream backport must merge first)
- Related to: TC-8050 (originating CVE, stream 2.2.x -- preemptive cross-stream task)

---

## Jira Linkage Summary

| Task | Type | Stream | Link to TC-8050 | Blocked By |
|------|------|--------|-----------------|------------|
| Upstream backport (2.2.x) | Standard | 2.2.x | Depend | -- |
| Downstream propagation (2.2.x) | Standard | 2.2.x | Depend | Upstream backport (2.2.x) |
| Upstream backport (2.1.x) | Preemptive | 2.1.x | Related | -- |
| Downstream propagation (2.1.x) | Preemptive | 2.1.x | Related | Upstream backport (2.1.x) |

## Dev-Dependency Override Summary

All four remediation tasks carry the following modifications per the dependency scope decision tree:

- **Label**: `dev-dependency` added to all tasks
- **Priority**: Normal (overrides CVE severity Medium/CVSS 5.3)
- **Rationale**: criterion is declared in `[dev-dependencies]` in backend/Cargo.toml and is NOT present in production builds. It is used for benchmarks only. The vulnerability (path traversal in benchmark output) represents a supply chain risk but does not affect shipped product artifacts.

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8050
2. Post summary comment to TC-8050 with version impact table, remediation task links, and @mention of the issue reporter
3. Post cross-stream impact comment noting 2.1.x is also affected
4. Post description digest comments on each created task
