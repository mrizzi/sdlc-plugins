# Step 8 -- Remediation: CVE-2026-31812

## Triage Outcome

- **2.2.x stream (in-scope)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected, but versions 2.2.3 and 2.2.4 already ship the fixed version (quinn-proto 0.11.14). The upstream branch `release/0.4.z` already contains the fix. The stream is effectively remediated -- no new remediation task is required.
- **2.1.x stream (cross-stream impact, Case B)**: All versions (2.1.0, 2.1.1) are affected. The upstream branch `release/0.3.z` does NOT have the fix. No CVE Jira exists for this stream. Preemptive remediation tasks are created per Case B.

## Case B -- Cross-Stream Impact Comment

The following comment would be posted to TC-8001:

```
Cross-stream impact: quinn-proto (versions before 0.11.14) also affects stream 2.1.x
based on lock file analysis. All 2.1.x versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9.
This stream is tracked by preemptive remediation tasks (see below) or may require
separate PSIRT triage.
```

## Preemptive Remediation Tasks for Stream 2.1.x

Since the ecosystem is Cargo (source dependency), two tasks are created: an upstream backport task and a downstream propagation subtask. These are preemptive (Case B) because no CVE Jira exists for the 2.1.x stream.

---

### Task 1: Upstream Backport (Preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related to TC-8001 (not Depend, because this is preemptive from a different stream)

#### Task Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8, quinn-proto 0.11.9), RHTPA 2.1.1 (v0.3.12, quinn-proto 0.11.9)
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
- quinn-proto is a transitive dependency via quinn -- the direct
  dependency version constraint on quinn may need updating as well

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

---

### Task 1 -- Description Digest Comment Steps

After creating the upstream backport task (e.g., assigned key TC-XXXX):

1. **Re-fetch the description** from Jira (the API may normalize content during storage):
   ```
   upstream_desc = jira.get_issue(TC-XXXX, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the digest:
   ```bash
   # Write fetched description to temp file
   echo "<fetched-description>" > /tmp/task-desc.md
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex-digest> (or sha256-adf:<64-char-hex-digest>)
   ```

3. **Post the digest comment** as an independent comment on TC-XXXX (before creating issue links or other comments):
   ```
   jira.add_comment(TC-XXXX, "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>")
   ```

   Using ADF contentFormat:
   ```json
   {
     "type": "doc",
     "version": 1,
     "content": [
       {
         "type": "paragraph",
         "content": [
           {
             "type": "text",
             "text": "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>"
           }
         ]
       }
     ]
   }
   ```

4. **Then create issue links**:
   ```
   jira.create_link(
     inwardIssue: TC-8001,
     outwardIssue: TC-XXXX,
     type: "Related"
   )
   ```

---

### Task 2: Downstream Propagation Subtask (Preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related to TC-8001 (preemptive); Blocks link from upstream task TC-XXXX

#### Task Description

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

---

### Task 2 -- Description Digest Comment Steps

After creating the downstream propagation task (e.g., assigned key TC-YYYY):

1. **Re-fetch the description** from Jira:
   ```
   downstream_desc = jira.get_issue(TC-YYYY, fields=["description"])
   ```

2. **Write the description to a temp file** and compute the digest:
   ```bash
   echo "<fetched-description>" > /tmp/task-desc.md
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex-digest> (or sha256-adf:<64-char-hex-digest>)
   ```

3. **Post the digest comment** as an independent comment on TC-YYYY (before creating issue links or other comments):
   ```
   jira.add_comment(TC-YYYY, "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>")
   ```

   Using ADF contentFormat:
   ```json
   {
     "type": "doc",
     "version": 1,
     "content": [
       {
         "type": "paragraph",
         "content": [
           {
             "type": "text",
             "text": "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>"
           }
         ]
       }
     ]
   }
   ```

4. **Then create issue links**:
   ```
   # Link downstream to originating CVE (preemptive - Related link)
   jira.create_link(
     inwardIssue: TC-8001,
     outwardIssue: TC-YYYY,
     type: "Related"
   )

   # Link downstream as blocked by upstream
   jira.create_link(
     inwardIssue: TC-XXXX,
     outwardIssue: TC-YYYY,
     type: "Blocks"
   )
   ```

---

## Post-Creation Comment on TC-8001

After creating both preemptive tasks, add a comment to the originating CVE Jira (TC-8001):

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: TC-XXXX (upstream backport, security-preemptive), TC-YYYY (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

## Post-Triage Summary

After all triage actions are complete:

1. **Add `ai-cve-triaged` label** to TC-8001.

2. **Post summary comment** to TC-8001 documenting:
   - Version impact table (all streams)
   - Affects Versions correction: `[RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
   - 2.2.x stream: Fix already present in 2.2.3+ (no remediation task created)
   - 2.1.x stream: Preemptive remediation tasks TC-XXXX and TC-YYYY created
   - @mention of the reporter (PSIRT analyst) using ADF mention node with their account ID
   - Comment Footnote appended (sdlc-workflow/triage-security vX.Y.Z)
