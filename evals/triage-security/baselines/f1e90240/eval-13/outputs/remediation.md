# Step 8 -- Remediation for TC-8001 (CVE-2026-31812)

## Triage Outcome

- **Case A**: Affected versions exist in the scoped stream (2.2.x) -- create remediation tasks.
- **Case B**: Cross-stream impact detected -- stream 2.1.x is also affected. Post cross-stream impact comment and create preemptive remediation tasks if no sibling CVE Jira exists for 2.1.x.

Ecosystem: **Cargo** (source dependency) -- two tasks per stream: upstream backport + downstream propagation.

---

## Case A -- Remediation Tasks for Stream 2.2.x

### Task 1: Upstream Backport Task (2.2.x)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (v0.4.8 retag)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (or transitive -- to be confirmed via Cargo.lock inspection)
- Note: upstream branch release/0.4.z already ships 0.11.14 at tags v0.4.11+.
  The fix is already present on the branch HEAD. Remediation may be a no-op
  if the branch tip already includes the bump -- verify that no older release
  branches are stuck at a pre-fix version.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
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

#### Description Digest Comment (Task 1)

After creating the upstream backport task, perform the following steps before creating any links or other comments:

1. Fetch the created task's description from Jira:
   ```
   jira.get_issue(<upstream-task-key>, fields=["description"])
   ```
2. Write the fetched description to a temp file (e.g., `/tmp/task-desc.md`).
3. Compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs either `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>` depending on the format returned by Jira.
4. Post the digest as a standalone comment on the upstream task:
   ```
   jira.add_comment(<upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   where `<tagged-digest>` is the full output from step 3 (e.g., `sha256-md:a1b2c3...64chars`).

---

### Task 2: Downstream Propagation Subtask (2.2.x)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Description**:

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct (or transitive) -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Comment (Task 2)

After creating the downstream propagation subtask, perform the following steps before creating any links or other comments:

1. Fetch the created task's description from Jira:
   ```
   jira.get_issue(<downstream-task-key>, fields=["description"])
   ```
2. Write the fetched description to a temp file (e.g., `/tmp/task-desc.md`).
3. Compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
4. Post the digest as a standalone comment on the downstream task:
   ```
   jira.add_comment(<downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

### Jira Linkage (2.2.x tasks)

After both tasks are created and their digest comments posted:

1. Link upstream task to the Vulnerability issue:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <upstream-task-key>, type: "Depend")
   ```
2. Link downstream subtask as blocked by upstream task:
   ```
   jira.create_link(inwardIssue: <upstream-task-key>, outwardIssue: <downstream-task-key>, type: "Blocks")
   ```
3. Link downstream subtask to the Vulnerability issue:
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <downstream-task-key>, type: "Depend")
   ```
4. Transition TC-8001 to In Progress (if not already).
5. Add comment to TC-8001:
   ```
   Remediation tasks created:
   - <upstream-task-key> (upstream backport: bump quinn-proto to 0.11.14 on release/0.4.z)
   - <downstream-task-key> (downstream propagation: update rhtpa-backend ref in rhtpa-release.0.4.z, blocked by <upstream-task-key>)
   ```

---

## Case B -- Cross-Stream Impact (2.1.x)

### Cross-Stream Impact Comment

Post a comment on TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
(versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9) based on lock
file analysis. This stream is tracked by companion issues (see Related
links) or may require separate PSIRT triage.
```

### Sibling Check

Search for sibling Vulnerability issues with the same CVE label scoped to 2.1.x:

```
jira.search_jql(
  "project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001"
)
```

- **If a sibling for 2.1.x exists**: skip preemptive task creation for 2.1.x -- that stream will be triaged through its own CVE issue.
- **If no sibling for 2.1.x exists**: create preemptive remediation tasks (below).

### Preemptive Task 3: Upstream Backport (2.1.x -- preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

```
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8), 2.1.1 (v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (or transitive -- to be confirmed via Cargo.lock inspection)
- Note: upstream branch release/0.3.z does NOT yet include the fix (latest
  tag v0.3.12 ships quinn-proto 0.11.9). An upstream PR is required to bump
  quinn-proto to >= 0.11.14 on this branch before the downstream propagation
  can proceed.

### Remediation approach (direct dependency)

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (originating tracking issue -- Related link, not Depend)
```

#### Description Digest Comment (Preemptive Task 3)

After creating the preemptive upstream backport task, perform the following steps before creating any links or other comments:

1. Fetch the created task's description from Jira:
   ```
   jira.get_issue(<preemptive-upstream-task-key>, fields=["description"])
   ```
2. Write the fetched description to a temp file (e.g., `/tmp/task-desc.md`).
3. Compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
4. Post the digest as a standalone comment on the preemptive upstream task:
   ```
   jira.add_comment(<preemptive-upstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

---

### Preemptive Task 4: Downstream Propagation Subtask (2.1.x -- preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Description**:

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <preemptive-upstream-task-key>.

The upstream backport (<preemptive-upstream-task-key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: direct (or transitive) -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <preemptive-upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8001 (originating tracking issue -- Related link, not Depend)
```

#### Description Digest Comment (Preemptive Task 4)

After creating the preemptive downstream propagation subtask, perform the following steps before creating any links or other comments:

1. Fetch the created task's description from Jira:
   ```
   jira.get_issue(<preemptive-downstream-task-key>, fields=["description"])
   ```
2. Write the fetched description to a temp file (e.g., `/tmp/task-desc.md`).
3. Compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
4. Post the digest as a standalone comment on the preemptive downstream task:
   ```
   jira.add_comment(<preemptive-downstream-task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

### Jira Linkage (2.1.x preemptive tasks)

After both preemptive tasks are created and their digest comments posted:

1. Link preemptive upstream task to the originating CVE Jira with "Related" (not "Depend"):
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <preemptive-upstream-task-key>, type: "Related")
   ```
2. Link downstream subtask as blocked by upstream task:
   ```
   jira.create_link(inwardIssue: <preemptive-upstream-task-key>, outwardIssue: <preemptive-downstream-task-key>, type: "Blocks")
   ```
3. Link preemptive downstream task to the originating CVE Jira with "Related":
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: <preemptive-downstream-task-key>, type: "Related")
   ```
4. Post comment on TC-8001:
   ```
   Preemptive remediation tasks created for streams without CVE Jiras:
   - 2.1.x: <preemptive-upstream-task-key> (upstream backport, security-preemptive)
   - 2.1.x: <preemptive-downstream-task-key> (downstream propagation, security-preemptive)

   These tasks use the "Related" link type and carry the security-preemptive
   label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
   reconciliation will link them and remove the label.
   ```

---

## Post-Triage Summary

After all triage actions are complete:

1. **Add `ai-cve-triaged` label** to TC-8001.
2. **Post summary comment** on TC-8001 documenting:
   - Version impact table (all streams)
   - Affects Versions correction: `[RHTPA 2.0.0]` -> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
   - Triage outcome: Remediation tasks created for 2.2.x; preemptive tasks created for 2.1.x
   - Links to all created tasks (upstream + downstream for both streams)
   - @mention of the reporter (ADF mention node with reporter's account ID)
   - Comment Footnote: `This comment was AI-generated by sdlc-workflow/triage-security v0.13.2.`

All Jira comments include the Comment Footnote per `shared/comment-footnote.md` using skill name `triage-security` and plugin version `0.13.2`.
