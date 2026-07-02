# Step 8 -- Remediation

## Triage Outcome: Case A -- Affected

The version impact analysis confirms that versions within the issue's stream scope
(2.2.x) are affected: RHTPA 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14.

Additionally, the 2.1.x stream is also affected (Case B -- cross-stream impact).
A cross-stream impact comment would be posted noting that stream 2.1.x (versions
2.1.0, 2.1.1) also ships the vulnerable quinn-proto version.

Since the ecosystem is **Cargo** (a source dependency), two remediation tasks are
created per Important Rule 8: an upstream backport task and a downstream
propagation subtask with a Blocks dependency between them.

---

## Task 1: Upstream Backport Task

**Proposed Jira issue creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5, quinn-proto 0.11.9), RHTPA 2.2.1 (v0.4.8, quinn-proto 0.11.12), RHTPA 2.2.2 (v0.4.9, retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8, v0.4.9

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Task 2: Downstream Propagation Subtask

**Proposed Jira issue creation:**

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Jira Linkage (Proposed)

After creating both remediation tasks, the following links would be established:

1. **Link upstream task to CVE Vulnerability issue:**
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

2. **Link downstream subtask to CVE Vulnerability issue:**
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )
   ```

3. **Link downstream subtask as blocked by upstream task:**
   ```
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

## Post-Creation Actions (Proposed)

1. **Propose adding `ai-cve-triaged` label** to TC-8001 to mark it as triaged.

2. **Propose transitioning** TC-8001 to In Progress (if not already).

3. **Post summary comment** on TC-8001 documenting the triage outcome:

   ```
   Triage complete for CVE-2026-31812 (quinn-proto < 0.11.14):

   Version impact:
   | Version | quinn-proto | Affected? |
   |---------|-------------|-----------|
   | 2.2.0   | 0.11.9      | YES       |
   | 2.2.1   | 0.11.12     | YES       |
   | 2.2.2   | --          | YES (retag of 2.2.1) |
   | 2.2.3   | 0.11.14     | NO        |
   | 2.2.4   | 0.11.14     | NO        |

   Affects Versions corrected: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

   Remediation tasks created:
   - <upstream-task-key> (upstream backport: bump quinn-proto to 0.11.14 on release/0.4.z)
   - <downstream-task-key> (downstream propagation: update backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)

   Cross-stream impact: 2.1.x stream (versions 2.1.0, 2.1.1) also ships
   vulnerable quinn-proto 0.11.9. Tracked by companion issues or may require
   separate PSIRT triage.
   ```

All actions described above are proposals for engineer confirmation. No Jira
mutations are executed without explicit approval per the skill's guardrails.
