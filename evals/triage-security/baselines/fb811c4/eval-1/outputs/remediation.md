# Step 7: Remediation Task Descriptions

## Ecosystem Classification

- **Ecosystem**: Cargo (source dependency)
- **Task creation pattern**: Two tasks (upstream backport + downstream propagation)

---

## Task 1: Upstream Backport Task

**Proposed Jira Issue**:
- **Type**: Task
- **Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)
- **Labels**: ai-generated-jira, Security, CVE-2026-31812

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (tag v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (tag v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (retag of v0.4.8, quinn-proto 0.11.12)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z (from Ecosystem Mappings)
- Check for pinned versions or transitive dependency constraints that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent Vulnerability tracking issue)

---

## Task 2: Downstream Propagation Subtask

**Proposed Jira Issue**:
- **Type**: Task
- **Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
- **Labels**: ai-generated-jira, Security, CVE-2026-31812

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14 on release/0.4.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

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
- Depends on: TC-8001 (parent Vulnerability tracking issue)

---

## Proposed Jira Linkage

1. **Link** the upstream backport task to TC-8001 (Vulnerability) with type "Depend"
2. **Link** the downstream propagation task to TC-8001 (Vulnerability) with type "Depend"
3. **Link** the downstream propagation task as blocked by the upstream backport task with type "Blocks"
4. **Propose** transitioning TC-8001 to "In Progress"
5. **Propose** assigning TC-8001 to the current user

All actions above are **proposals** pending confirmation before execution.
