# Step 7 -- Remediation for CVE-2026-31812

## Triage Outcome

**Case A: Affected -- create remediation tasks** for stream 2.2.x.

Within the 2.2.x stream scope, versions 2.2.0, 2.2.1, and 2.2.2 are affected (they ship quinn-proto < 0.11.14). Since quinn-proto is a **Cargo** (source dependency) ecosystem, two tasks are created: an upstream backport task and a downstream propagation subtask.

**Case B: Cross-stream impact** -- the 2.1.x stream is also affected (2.1.0 and 2.1.1 ship quinn-proto 0.11.9). A cross-stream impact comment would be posted to TC-8001. Since 2.1.x may or may not have its own CVE Jira, preemptive remediation tasks would be created for that stream if no companion CVE Jira exists.

---

## Remediation Task 1: Upstream Backport Task (Stream 2.2.x)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1/2.2.2)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.4.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)
- Note: builds v0.4.11+ already ship quinn-proto 0.11.14 on this branch,
  so the fix may already be present at branch HEAD

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Comment (Post-Creation)

After creating the upstream backport task, the following steps would be performed to post the description digest comment:

1. **Re-fetch the description** from Jira to get the stored representation:
   ```
   upstream_desc = jira.get_issue(<upstream-task-key>, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the digest:
   ```bash
   # Write the fetched description to a temp file
   # Then compute the digest:
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex-digest> (or sha256-adf:<64-char-hex-digest>)
   ```

3. **Post the digest comment** as a standalone comment on the upstream task (before any links or other comments):
   ```
   jira.add_comment(<upstream-task-key>,
     "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>")
   ```
   The comment uses ADF contentFormat with a single paragraph containing the marker and full tagged digest.

4. **Then create the issue link** to TC-8001:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream-task-key>,
     type: "Depend"
   )
   ```

---

## Remediation Task 2: Downstream Propagation Subtask (Stream 2.2.x)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

### Task Description

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

### Description Digest Comment (Post-Creation)

After creating the downstream propagation task, the following steps would be performed:

1. **Re-fetch the description** from Jira:
   ```
   downstream_desc = jira.get_issue(<downstream-task-key>, fields=["description"])
   ```

2. **Compute the digest**:
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex-digest> (or sha256-adf:<64-char-hex-digest>)
   ```

3. **Post the digest comment** as a standalone comment on the downstream task (before links or other comments):
   ```
   jira.add_comment(<downstream-task-key>,
     "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>")
   ```

4. **Then create the issue links**:
   ```
   # Link downstream task to the Vulnerability issue
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-key>,
     type: "Depend"
   )

   # Link downstream task as blocked by upstream task
   jira.create_link(
     inwardIssue: <upstream-task-key>,
     outwardIssue: <downstream-task-key>,
     type: "Blocks"
   )
   ```

---

## Cross-Stream Impact (Case B) -- Stream 2.1.x

### Cross-Stream Impact Comment on TC-8001

The following comment would be posted to TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s)
2.1.x based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

### Preemptive Remediation Tasks for 2.1.x (if no companion CVE Jira exists)

If no sibling Vulnerability issue with label CVE-2026-31812 and stream suffix `[rhtpa-2.1]` is found, the following preemptive tasks would be created:

#### Preemptive Upstream Backport Task (Stream 2.1.x)

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <upstream template with preemptive prefix>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

The description would include the preemptive prefix:

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream rhtpa-2.2).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.
```

Target branch: `release/0.3.z`

**Description Digest Comment** steps (same as above):
1. Re-fetch description: `jira.get_issue(<preemptive-upstream-task-key>, fields=["description"])`
2. Compute digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
3. Post digest comment: `jira.add_comment(<preemptive-upstream-task-key>, "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>")`
4. Link with "Related" (not "Depend") to originating CVE:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <preemptive-upstream-task-key>,
     type: "Related"
   )
   ```

#### Preemptive Downstream Propagation Task (Stream 2.1.x)

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <downstream template with preemptive prefix>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

Target branch: `main`
Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)

**Description Digest Comment** steps:
1. Re-fetch description: `jira.get_issue(<preemptive-downstream-task-key>, fields=["description"])`
2. Compute digest: `python3 scripts/sha256-digest.py /tmp/task-desc.md`
3. Post digest comment: `jira.add_comment(<preemptive-downstream-task-key>, "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>")`
4. Link with "Related" to originating CVE and "Blocks" from upstream:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <preemptive-downstream-task-key>,
     type: "Related"
   )
   jira.create_link(
     inwardIssue: <preemptive-upstream-task-key>,
     outwardIssue: <preemptive-downstream-task-key>,
     type: "Blocks"
   )
   ```

---

## Post-Triage Actions

After all remediation tasks are created:

1. **Add `ai-cve-triaged` label** to TC-8001
2. **Transition** TC-8001 to In Progress
3. **Assign** TC-8001 to the current user
4. **Post summary comment** to TC-8001 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
   - Triage outcome: remediation tasks created
   - Links to all remediation tasks (upstream + downstream for 2.2.x, preemptive upstream + downstream for 2.1.x if applicable)
   - @mention of the reporter (PSIRT analyst)
   - Comment Footnote: "This comment was AI-generated by sdlc-workflow/triage-security v0.11.0."

All Jira comments include the Comment Footnote as specified in `shared/comment-footnote.md` using the plugin version 0.11.0 from `plugins/sdlc-workflow/.claude-plugin/plugin.json`.
