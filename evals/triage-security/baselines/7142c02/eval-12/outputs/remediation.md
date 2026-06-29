# Step 7 -- Remediation: CVE-2026-48901 (h2)

## Triage Outcome

**Case A + Case B**: The scoped 2.2.x stream has one affected version (2.2.0), and the cross-stream 2.1.x stream is fully affected.

### Scoped stream (2.2.x)

Only version 2.2.0 is affected. Versions 2.2.1+ already ship h2 >= 0.4.8. Since the fix is already present in later 2.2.x releases, the remediation path for this stream depends on whether 2.2.0 is still deployed. If 2.2.0 is superseded by 2.2.1+, the scoped stream may not need active remediation. However, Affects Versions should be corrected.

### Cross-stream (2.1.x)

All 2.1.x versions ship h2 0.4.5 (below the 0.4.8 fix threshold). Since no stream-specific CVE Jira exists for 2.1.x, preemptive remediation tasks should be created.

---

## Remediation Task Descriptions

### Task 1: Upstream Backport (2.1.x stream -- preemptive)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

**Link type**: Related (to TC-8030, since this is a preemptive task for a different stream)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

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

- Depends on: TC-8030 (parent tracking issue)

---

### Task 2: Downstream Propagation (2.1.x stream -- preemptive)

**Summary**: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

**Link type**: Related (to TC-8030); Blocks (blocked by upstream task 1)

#### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-48901
fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next build
ships the fix.

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
- Depends on: TC-8030 (parent tracking issue)

---

### Task 3: Upstream Backport (2.2.x stream -- standard remediation)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-48901

**Link type**: Depend (to TC-8030)

**Note**: In the 2.2.x stream, the fix for h2 was already picked up starting with version 2.2.1 (build v0.4.8, h2 = 0.4.8). Only version 2.2.0 shipped the vulnerable h2 0.4.5. Since subsequent releases already include the fix, this task may be resolved as already fixed if 2.2.0 is no longer actively deployed.

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.2.0 (v0.4.5)
Source commit(s): v0.4.5

Note: The fix is already present in 2.2.1+ (h2 0.4.8 at tag v0.4.8). The upstream
branch release/0.4.z already includes h2 >= 0.4.8.

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- h2 is already >= 0.4.8 on the release/0.4.z branch (fixed from v0.4.8 onward)
- Verify that no backport to a 2.2.0 maintenance branch is needed
- If 2.2.0 is superseded, this task can be closed as already fixed

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (parent tracking issue)

---

## Post-Triage Actions

1. **Affects Versions Correction**: Correct the Affects Versions on TC-8030. Currently set to "RHTPA 2.2.0" -- only 2.2.0 is affected in the scoped stream, so this is correct. No change needed.

2. **Cross-stream impact comment**: Post to TC-8030:
   > Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file analysis.
   > All 2.1.x versions (2.1.0, 2.1.1) ship h2 0.4.5.
   > The 2.1.x stream does not have a dedicated CVE Jira -- preemptive remediation tasks have been created.

3. **Preemptive remediation comment**: Post to TC-8030:
   > Preemptive remediation tasks created for streams without CVE Jiras:
   > - 2.1.x: [upstream-task-key] (security-preemptive), [downstream-task-key] (security-preemptive)
   >
   > These tasks use the "Related" link type and carry the security-preemptive
   > label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
   > reconciliation will link them and remove the label.

4. **Label**: Add `ai-cve-triaged` label to TC-8030.

5. **Post-triage summary comment**: Document the version impact table, Affects Versions status, triage outcome, and links to all remediation tasks created. Include @mention of the reporter.
