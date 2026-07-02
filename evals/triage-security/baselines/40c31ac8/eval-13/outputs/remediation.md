# Step 8 -- Remediation: CVE-2026-31812

## Triage Outcome

- **Case A** applies for stream 2.2.x: versions 2.2.0, 2.2.1, and 2.2.2 are affected.
- **Case B** applies: stream 2.1.x is also affected (cross-stream impact). Preemptive remediation tasks are created for 2.1.x since no sibling CVE Jira exists for that stream.

Since the ecosystem is **Cargo** (source dependency), each stream requires **two tasks**: an upstream backport task and a downstream propagation subtask.

---

## Case A: Standard Remediation Tasks (Stream 2.2.x)

### Task 1: Upstream Backport (2.2.x)

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description:**

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (quinn-proto 0.11.9), 2.2.1 (quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

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
```

**Jira API call:**

```
upstream_task_2_2 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <upstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

#### Description Digest Comment (Task 1)

After creating the upstream task, post a description digest comment before any links or other comments:

1. Re-fetch the description from Jira:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a format-tagged digest, e.g. `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.
3. Post the digest comment:
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

### Task 2: Downstream Propagation (2.2.x)

**Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description:**

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
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

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Jira API call:**

```
downstream_task_2_2 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <downstream-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

#### Description Digest Comment (Task 2)

After creating the downstream task, post a description digest comment before any links or other comments:

1. Re-fetch the description from Jira:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a format-tagged digest, e.g. `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.
3. Post the digest comment:
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

### Linkage (2.2.x tasks)

After creating both tasks and posting their digest comments:

1. Link upstream task to TC-8001:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")
   ```
2. Link downstream task as blocked by upstream task:
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```
3. Link downstream task to TC-8001:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")
   ```

---

## Case B: Preemptive Remediation Tasks (Stream 2.1.x)

Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). No sibling CVE Jira exists for stream 2.1.x, so preemptive remediation tasks are created.

### Task 3: Upstream Backport -- Preemptive (2.1.x)

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description:**

```
## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (quinn-proto 0.11.9), 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
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
```

**Jira API call:**

```
upstream_task_2_1 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)",
  description: <upstream-preemptive-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

#### Description Digest Comment (Task 3)

After creating the preemptive upstream task, post a description digest comment before any links or other comments:

1. Re-fetch the description from Jira:
   ```
   upstream_desc = jira.get_issue(<upstream-task-2-1-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a format-tagged digest, e.g. `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.
3. Post the digest comment:
   ```
   jira.add_comment(<upstream-task-2-1-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

### Task 4: Downstream Propagation -- Preemptive (2.1.x)

**Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description:**

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <upstream-task-2-1-key>.

The upstream backport (<upstream-task-2-1-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

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

- Depends on: <upstream-task-2-1-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

**Jira API call:**

```
downstream_task_2_1 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <downstream-preemptive-task-description above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

#### Description Digest Comment (Task 4)

After creating the preemptive downstream task, post a description digest comment before any links or other comments:

1. Re-fetch the description from Jira:
   ```
   downstream_desc = jira.get_issue(<downstream-task-2-1-key>, fields=["description"])
   ```
2. Write the description to a temp file and compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a format-tagged digest, e.g. `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.
3. Post the digest comment:
   ```
   jira.add_comment(<downstream-task-2-1-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

### Linkage (2.1.x preemptive tasks)

After creating both preemptive tasks and posting their digest comments:

1. Link upstream preemptive task to TC-8001 with "Related" (not "Depend", because this is a preemptive task for a different stream):
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-2-1-key>, type: "Related")
   ```
2. Link downstream preemptive task as blocked by upstream preemptive task:
   ```
   jira.create_link(inwardIssue: <upstream-task-2-1-key>, outwardIssue: <downstream-task-2-1-key>, type: "Blocks")
   ```
3. Link downstream preemptive task to TC-8001 with "Related":
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-2-1-key>, type: "Related")
   ```

---

## Cross-Stream Impact Comment on TC-8001

Post a comment on TC-8001 documenting the cross-stream impact and preemptive tasks:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-2-1-key> (upstream backport, security-preemptive)
- 2.1.x: <downstream-task-2-1-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Post-Triage Summary

After all remediation actions, the following post-triage actions would be performed on TC-8001:

1. **Add the `ai-cve-triaged` label** to TC-8001.

2. **Post a summary comment** on TC-8001 documenting:
   - Version impact table (all streams)
   - Affects Versions correction: `[RHTPA 2.0.0]` -> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
   - Triage outcome: remediation tasks created for 2.2.x (standard) and 2.1.x (preemptive)
   - Links to all remediation tasks created
   - @mention of the vulnerability issue's reporter

   The summary comment includes the Comment Footnote (sdlc-workflow/triage-security v0.11.1).
