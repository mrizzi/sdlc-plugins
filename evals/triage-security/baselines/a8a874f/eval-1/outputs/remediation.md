# Step 7: Remediation Task Descriptions

## Overview

CVE-2026-31812 requires remediation in the **2.2.x stream**. The Cargo ecosystem mapping specifies:
- **Repository**: backend
- **Lock File**: Cargo.lock
- **Upstream Branch**: release/0.4.z

Two tasks are proposed: an upstream backport task to bump the dependency, and a downstream propagation subtask to update the release repo reference.

---

## Task 1: Upstream Backport Task (2.2.x stream)

**Proposed Issue Type**: Task (subtask of TC-8001)

| Field | Value |
|-------|-------|
| Summary | CVE-2026-31812: Bump quinn-proto to >= 0.11.14 in release/0.4.z |
| Repository | backend |
| Target Branch | release/0.4.z |
| Component | pscomponent:org/rhtpa-server |
| Labels | CVE-2026-31812, remediation-upstream |
| Dependencies | TC-8001 (parent vulnerability issue) |

### Description

Remediate CVE-2026-31812 by bumping the quinn-proto dependency to >= 0.11.14 in the backend repository on branch release/0.4.z. The quinn-proto crate before 0.11.14 is vulnerable to a denial of service via panic on large stream counts.

### Implementation Notes

- Update the quinn-proto dependency in the backend repository to version >= 0.11.14
- Run `cargo update -p quinn-proto` or manually edit `Cargo.toml` to set the minimum version
- Verify `Cargo.lock` reflects quinn-proto >= 0.11.14 after the update
- Upstream fix PR for reference: [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048)

### Acceptance Criteria

- [ ] quinn-proto dependency version in Cargo.toml and Cargo.lock is >= 0.11.14
- [ ] No dependency conflicts introduced by the version bump
- [ ] All existing tests pass with the updated dependency
- [ ] PR targets the release/0.4.z branch

---

## Task 2: Downstream Propagation Subtask (2.2.x stream)

**Proposed Issue Type**: Task (subtask of TC-8001)

| Field | Value |
|-------|-------|
| Summary | CVE-2026-31812: Update backend reference in rhtpa-release.0.4.z |
| Repository | rhtpa-release.0.4.z |
| Target Branch | main |
| Component | pscomponent:org/rhtpa-server |
| Labels | CVE-2026-31812, remediation-downstream |
| Dependencies | Blocked by upstream backport task (Task 1) |

### Description

Update the backend source pinning reference in the rhtpa-release.0.4.z Konflux release repository to pick up the upstream fix for CVE-2026-31812. This task is blocked by the upstream backport task and should only proceed after the upstream fix is merged.

### Implementation Notes

- Update the source pinning reference (in `artifacts.lock.yaml`) to point to the new backend tag that includes the quinn-proto >= 0.11.14 fix
- The download URL in artifacts.lock.yaml contains the backend tag; update it to the tag produced by the upstream backport merge

### Acceptance Criteria

- [ ] Backend reference in artifacts.lock.yaml is updated to the new tag containing the fix
- [ ] Konflux rebuild triggers successfully with the updated reference
- [ ] Rebuilt container image includes quinn-proto >= 0.11.14

---

## Jira Linkage

The following Jira link operations would be executed after task creation and engineer confirmation:

### Upstream Backport Task (Task 1) linkage
- **Link to TC-8001**: Create "Depend" link type between Task 1 and TC-8001 (Task 1 depends on TC-8001 as the parent vulnerability)

### Downstream Propagation Task (Task 2) linkage
- **Link to TC-8001**: Create "Depend" link type between Task 2 and TC-8001 (Task 2 depends on TC-8001 as the parent vulnerability)
- **Blocked by Task 1**: Create "Blocks" link type where Task 1 blocks Task 2 (downstream propagation cannot proceed until upstream backport is merged)

### Execution Note

All task creation and Jira linkage operations described above are **proposals only**. They would be executed after engineer confirmation via the Jira API (`createJiraIssue` for task creation, `linkJiraIssues` for link creation). Task transitions and status updates would similarly require engineer approval before execution.
