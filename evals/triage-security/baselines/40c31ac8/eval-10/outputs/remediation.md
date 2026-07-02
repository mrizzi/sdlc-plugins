# Step 8 -- Remediation for TC-8020 (CVE-2026-55123)

## Triage Outcome

The version impact analysis shows affected versions in both the issue's scoped stream (rhtpa-2.2) and another stream (rhtpa-2.1). This triggers:

- **Case A**: Create remediation tasks for the current stream (rhtpa-2.2)
- **Case B**: Create preemptive remediation tasks for stream rhtpa-2.1 (no CVE Jira exists for that stream)

## Case A: Remediation Tasks for Stream rhtpa-2.2 (Current Issue Scope)

Since tokio is a Cargo (source dependency) ecosystem, two tasks are created:

### Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`

**Description**:

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-55123: tokio use-after-free in task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1), RHTPA 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Update tokio dependency to >= 1.42.0 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (parent tracking issue)
```

**Post-creation actions**:
1. Post description digest comment per `shared/description-digest-protocol.md`
2. Link to TC-8020 with link type "Depend"

### Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`

**Description**:

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-55123 fix from the upstream backport task.

The upstream backport task bumps tokio to 1.42.0
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue)
```

**Post-creation actions**:
1. Post description digest comment per `shared/description-digest-protocol.md`
2. Link to TC-8020 with link type "Depend"
3. Link downstream subtask as blocked by upstream task with link type "Blocks"

---

## Case B: Preemptive Remediation Tasks for Stream rhtpa-2.1

A JQL search for sibling CVE Jiras with label `CVE-2026-55123` returned no results for stream rhtpa-2.1. No CVE Jira exists for that stream. Per Step 8 Case B, preemptive remediation tasks are created.

Since tokio is a Cargo (source dependency) ecosystem, two preemptive tasks are created:

### Preemptive Task 1: Upstream Backport Task (rhtpa-2.1)

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

**Description**:

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-55123: tokio use-after-free in task abort.
The vulnerable dependency (tokio < 1.42.0) must be updated
to the fixed version (1.42.0+).

Affected versions: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp

## Implementation Notes

- Update tokio dependency to >= 1.42.0 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] tokio dependency is >= 1.42.0
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8020 (parent tracking issue, cross-stream)
```

**Post-creation actions**:
1. Post description digest comment per `shared/description-digest-protocol.md`
2. Link to TC-8020 with link type "Related" (not "Depend", because this is a preemptive task for a different stream)

### Preemptive Task 2: Downstream Propagation Subtask (rhtpa-2.1)

**Summary**: Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

**Description**:

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-55123 fix from the upstream backport task.

The upstream backport task bumps tokio to 1.42.0
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream preemptive backport task (upstream backport must merge first)
- Depends on: TC-8020 (parent tracking issue, cross-stream)
```

**Post-creation actions**:
1. Post description digest comment per `shared/description-digest-protocol.md`
2. Link to TC-8020 with link type "Related" (not "Depend", because this is a preemptive task for a different stream)
3. Link downstream preemptive subtask as blocked by upstream preemptive task with link type "Blocks"

---

## Post-Triage Summary

### 1. Add `ai-cve-triaged` label to TC-8020

### 2. Post summary comment to TC-8020

The summary comment would include:

1. Version impact table (from Step 2.4)
2. Affects Versions correction (scoped to stream rhtpa-2.2: RHTPA 2.2.0, RHTPA 2.2.1)
3. Triage outcome: Case A remediation + Case B preemptive remediation
4. Links to all remediation tasks created:
   - Stream rhtpa-2.2 (Case A): upstream backport task + downstream propagation subtask
   - Stream rhtpa-2.1 (Case B, preemptive): upstream backport task + downstream propagation subtask
5. @mention of the vulnerability issue's reporter

The comment MUST include the Comment Footnote:

```
---
This comment was AI-generated by sdlc-workflow/triage-security v0.11.1.
```

(In ADF format with the rule node and link to https://github.com/mrizzi/sdlc-plugins)
