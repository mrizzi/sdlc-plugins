# Remediation — TC-8004

## Triage Outcome: Case A — Affected (2.1.x stream only)

The 2.1.x stream is affected. The 2.2.x stream is not affected (ships h2 >= 0.4.8). Since the issue is unscoped (covers all streams), no cross-stream impact notice is needed — the version impact analysis already covers all streams.

Remediation tasks are proposed only for the **2.1.x** stream. No remediation is needed for the 2.2.x stream.

The ecosystem is Cargo (source dependency), so two tasks are proposed: an upstream backport task and a downstream propagation subtask.

---

## PROPOSAL: Upstream Backport Task (2.1.x)

**Summary**: Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

### Task Description

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0, RHTPA 2.1.1
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)
- The fix adds a configurable maximum header list size that defaults to 16 KiB

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

## PROPOSAL: Downstream Propagation Task (2.1.x)

**Summary**: Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-33501`

### Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-33501 fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

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

---

## Jira Linkage (proposed)

After creation, the following links would be established:

1. Upstream backport task linked to TC-8004 with type "Depend"
2. Downstream propagation task linked to TC-8004 with type "Depend"
3. Downstream propagation task linked to upstream backport task with type "Blocks" (downstream blocked by upstream)

## Post-Triage Actions (proposed)

1. Add label `ai-cve-triaged` to TC-8004
2. Post description digest comment on each created task
3. Post summary comment on TC-8004 with:
   - Version impact table
   - Affects Versions correction (remove RHTPA 2.2.0, add RHTPA 2.1.1)
   - Remediation tasks created (upstream + downstream for 2.1.x)
   - @mention of the issue reporter

All proposed actions require engineer confirmation before execution.
