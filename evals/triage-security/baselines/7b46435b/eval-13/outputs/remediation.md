# Step 8 -- Remediation for CVE-2026-31812

## Triage Outcome

### 2.2.x Stream (in-scope)

The 2.2.x stream already ships the fixed version of quinn-proto (0.11.14) in versions 2.2.3 and 2.2.4. The upstream branch `release/0.4.z` already contains the fix at its latest build tag (v0.4.12). No new remediation task is needed for the 2.2.x stream.

**Actions for 2.2.x:**
- Correct Affects Versions: `[RHTPA 2.0.0]` -> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
- Post Affects Versions correction comment on TC-8001
- No remediation tasks created (fix already shipped in 2.2.3+)

### 2.1.x Stream (cross-stream impact -- Case B)

The 2.1.x stream is affected (all versions ship quinn-proto 0.11.9, which is < 0.11.14). No stream-specific CVE Jira exists for 2.1.x. Preemptive remediation tasks are created per Case B.

Since quinn-proto is a Cargo (source dependency) ecosystem, two preemptive tasks are created:
1. Upstream backport task (fix in the source repo on release/0.3.z)
2. Downstream propagation subtask (update the backend reference in rhtpa-release.0.3.z)

---

## Remediation Task 1: Upstream Backport (2.1.x, Preemptive)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)",
  description: <upstream-task-description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

### Task Description

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8, quinn-proto 0.11.9), 2.1.1 (v0.3.12, quinn-proto 0.11.9)
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

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Comment (Task 1)

After creating the upstream backport task (assume key TC-XXXX):

1. Re-fetch the description from Jira:
   ```
   upstream_desc = jira.get_issue(TC-XXXX, fields=["description"])
   ```

2. Write the description to a temp file and compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a format-tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.

3. Post the digest comment (before creating issue links or other comments):
   ```
   jira.add_comment(TC-XXXX, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `sha256-digest.py` (e.g., `sha256-md:a1b2c3...64chars`).

4. Link to the originating CVE Jira with "Related" (preemptive linkage):
   ```
   jira.create_link(
     inwardIssue: TC-8001,
     outwardIssue: TC-XXXX,
     type: "Related"
   )
   ```

---

## Remediation Task 2: Downstream Propagation Subtask (2.1.x, Preemptive)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)",
  description: <downstream-task-description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

### Task Description

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from TC-XXXX (upstream backport task).

The upstream backport (TC-XXXX) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy before
discussing in public channels or PRs.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: TC-XXXX (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

### Description Digest Comment (Task 2)

After creating the downstream propagation task (assume key TC-YYYY):

1. Re-fetch the description from Jira:
   ```
   downstream_desc = jira.get_issue(TC-YYYY, fields=["description"])
   ```

2. Write the description to a temp file and compute the digest:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a format-tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.

3. Post the digest comment (before creating issue links or other comments):
   ```
   jira.add_comment(TC-YYYY, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `sha256-digest.py` (e.g., `sha256-md:a1b2c3...64chars`).

4. Link to the originating CVE Jira with "Related" (preemptive linkage):
   ```
   jira.create_link(
     inwardIssue: TC-8001,
     outwardIssue: TC-YYYY,
     type: "Related"
   )
   ```

5. Link the downstream subtask as blocked by the upstream task:
   ```
   jira.create_link(
     inwardIssue: TC-XXXX,
     outwardIssue: TC-YYYY,
     type: "Blocks"
   )
   ```

---

## Cross-Stream Impact Comment on TC-8001

After creating the preemptive tasks, post a comment on TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: TC-XXXX (upstream backport, security-preemptive), TC-YYYY (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/mrizzi/sdlc-plugins) v0.12.1.
```

## Post-Triage Summary Comment on TC-8001

After all triage actions are complete:

1. Add `ai-cve-triaged` label to TC-8001.

2. Post summary comment:

```
## CVE-2026-31812 Triage Summary

### Version Impact

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

### Affects Versions Correction

Current: [RHTPA 2.0.0] -> Corrected: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
(scoped to stream 2.2.x per issue suffix [rhtpa-2.2])

### Triage Outcome

**2.2.x stream**: Fix already shipped in versions 2.2.3+ (quinn-proto 0.11.14).
No remediation tasks needed for this stream.

**2.1.x stream (cross-stream impact)**: Preemptive remediation tasks created:
- TC-XXXX: upstream backport -- bump quinn-proto to 0.11.14 on release/0.3.z (security-preemptive)
- TC-YYYY: downstream propagation -- update backend ref in rhtpa-release.0.3.z (security-preemptive, blocked by TC-XXXX)

@reporter-mention (PSIRT reporter)

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/mrizzi/sdlc-plugins) v0.12.1.
```

## Jira Linkage Summary

| Link Type | From | To | Purpose |
|-----------|------|----|---------|
| Related | TC-8001 | TC-XXXX | Preemptive upstream backport (2.1.x) |
| Related | TC-8001 | TC-YYYY | Preemptive downstream propagation (2.1.x) |
| Blocks | TC-XXXX | TC-YYYY | Downstream blocked by upstream |
