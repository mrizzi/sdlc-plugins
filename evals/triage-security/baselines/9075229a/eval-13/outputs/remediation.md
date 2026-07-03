# Step 8 -- Remediation for TC-8001

## Triage Outcome

The issue TC-8001 is scoped to the **2.2.x** stream (from summary suffix `[rhtpa-2.2]`).

- **2.2.x stream (scoped)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 are not affected.
- **2.1.x stream (out of scope)**: Versions 2.1.0 and 2.1.1 are also affected based on cross-stream impact analysis.

This triggers **Case A** (affected -- create remediation tasks for the scoped 2.2.x stream) and **Case B** (cross-stream impact -- 2.1.x is also affected).

## Case A: Remediation Tasks for 2.2.x Stream

Since quinn-proto is a **Cargo** (source dependency) ecosystem, two tasks are created:

### Task 1: Upstream Backport Task

**Jira Creation Call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

```
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0, 2.2.1, 2.2.2
Source commit(s): v0.4.5, v0.4.8 (v0.4.9 is a retag of v0.4.8)

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

#### Description Digest Protocol for Upstream Backport Task

After creating the upstream backport task (assume it receives key TC-9001), the following description digest steps are performed **before** creating issue links or other comments:

1. **Re-fetch the description from Jira**: The description is re-fetched from the Jira API after creation because Jira normalizes content during storage. The raw description passed to `create_issue` must not be hashed directly.
   ```
   upstream_desc = jira.get_issue("TC-9001", fields=["description"])
   ```

2. **Write the description to a temporary file**: The fetched description content (markdown or ADF JSON, depending on the Jira access method) is written to a temporary file.
   ```
   Write description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest using scripts/sha256-digest.py**: The script auto-detects the input format (ADF JSON or markdown) and outputs a format-tagged digest.
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This produces output in the form `sha256-md:<64-char-hex>` (if markdown) or `sha256-adf:<64-char-hex>` (if ADF JSON).

4. **Post the digest comment on the created task**: A standalone comment is posted with the exact marker prefix `[sdlc-workflow] Description digest:` followed by the tagged digest. This comment must be posted before any issue links or other comments.
   ```
   jira.add_comment("TC-9001", "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>")
   ```
   The comment is posted in ADF format:
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

5. **Only after the digest comment is posted**, proceed to create the issue link:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: "TC-9001",
     type: "Depend"
   )
   ```

---

### Task 2: Downstream Propagation Subtask

**Jira Creation Call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task Description:**

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from TC-9001.

The upstream backport (TC-9001) bumps quinn-proto to 0.11.14
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

- Depends on: TC-9001 (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Protocol for Downstream Propagation Subtask

After creating the downstream propagation subtask (assume it receives key TC-9002), the following description digest steps are performed **before** creating issue links or other comments:

1. **Re-fetch the description from Jira**: The description is re-fetched from the Jira API after creation because Jira normalizes content during storage.
   ```
   downstream_desc = jira.get_issue("TC-9002", fields=["description"])
   ```

2. **Write the description to a temporary file**: The fetched description content is written to a temporary file.
   ```
   Write description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest using scripts/sha256-digest.py**: The script auto-detects the input format and outputs a format-tagged digest.
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This produces output in the form `sha256-md:<64-char-hex>` (if markdown) or `sha256-adf:<64-char-hex>` (if ADF JSON).

4. **Post the digest comment on the created task**: A standalone comment is posted with the exact marker prefix before any issue links or other comments.
   ```
   jira.add_comment("TC-9002", "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>")
   ```
   The comment is posted in ADF format:
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

5. **Only after the digest comment is posted**, proceed to create the issue links:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: "TC-9002",
     type: "Depend"
   )
   jira.create_link(
     inwardIssue: "TC-9001",
     outwardIssue: "TC-9002",
     type: "Blocks"
   )
   ```

---

## Case B: Cross-Stream Impact -- 2.1.x Stream

The version impact analysis reveals that the **2.1.x** stream is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9, which is < 0.11.14).

### Cross-Stream Impact Comment on TC-8001

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. This stream is tracked by companion issues
(see Related links) or may require separate PSIRT triage.
```

### Preemptive Remediation Check

A JQL search would be performed for sibling Vulnerability issues with label `CVE-2026-31812` and summary suffix `[rhtpa-2.1]` to check if a CVE Jira already exists for the 2.1.x stream. If no CVE Jira exists for 2.1.x, preemptive remediation tasks are created:

### Preemptive Upstream Backport Task for 2.1.x

**Jira Creation Call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task Description:**

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

Affected versions: 2.1.0, 2.1.1
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

- Depends on: TC-8001 (originating CVE tracking issue)
```

#### Description Digest Protocol for Preemptive Upstream Task (2.1.x)

After creating the preemptive upstream task (assume it receives key TC-9003), the following description digest steps are performed **before** creating issue links or other comments:

1. **Re-fetch the description from Jira**:
   ```
   preemptive_upstream_desc = jira.get_issue("TC-9003", fields=["description"])
   ```

2. **Write the description to a temporary file**:
   ```
   Write description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest using scripts/sha256-digest.py**:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   Produces `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.

4. **Post the digest comment** (before any links or other comments):
   ```
   jira.add_comment("TC-9003", "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>")
   ```
   Posted in ADF format:
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

5. **Only after the digest comment is posted**, create the "Related" link to the originating CVE (not "Depend", since this is preemptive):
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: "TC-9003",
     type: "Related"
   )
   ```

### Preemptive Downstream Propagation Subtask for 2.1.x

**Jira Creation Call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task Description:**

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
CVE-2026-31812 fix from TC-9003.

The upstream backport (TC-9003) bumps quinn-proto to 0.11.14
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

- Depends on: TC-9003 (upstream backport must merge first)
- Depends on: TC-8001 (originating CVE tracking issue)
```

#### Description Digest Protocol for Preemptive Downstream Task (2.1.x)

After creating the preemptive downstream task (assume it receives key TC-9004), the following description digest steps are performed **before** creating issue links or other comments:

1. **Re-fetch the description from Jira**:
   ```
   preemptive_downstream_desc = jira.get_issue("TC-9004", fields=["description"])
   ```

2. **Write the description to a temporary file**:
   ```
   Write description content to /tmp/task-desc.md
   ```

3. **Compute the SHA-256 digest using scripts/sha256-digest.py**:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   Produces `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.

4. **Post the digest comment** (before any links or other comments):
   ```
   jira.add_comment("TC-9004", "[sdlc-workflow] Description digest: sha256-md:<64-char-hex-digest>")
   ```
   Posted in ADF format:
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

5. **Only after the digest comment is posted**, create the links:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: "TC-9004",
     type: "Related"
   )
   jira.create_link(
     inwardIssue: "TC-9003",
     outwardIssue: "TC-9004",
     type: "Blocks"
   )
   ```

### Preemptive Tasks Comment on TC-8001

After creating the preemptive tasks, a comment is posted on the originating CVE Jira:

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: TC-9003 (security-preemptive), TC-9004 (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Description Digest Protocol Summary

The description digest protocol is applied identically to every remediation task created during this triage. The protocol ensures that `/implement-task` can verify description integrity in its Step 1.5. The key rules are:

1. **Always re-fetch** the description from the Jira API after `create_issue` -- never hash the description string passed to the creation call, because Jira normalizes content during storage.
2. **Always use `scripts/sha256-digest.py`** to compute the digest -- never compute SHA-256 manually. The script auto-detects the format (ADF JSON or markdown) and outputs a format-tagged digest.
3. **Post the digest comment before any other mutations** on the task -- before issue links, before other comments. The comment is a standalone comment, not appended to any other comment.
4. **The marker string is fixed**: `[sdlc-workflow] Description digest:` -- it does not vary per skill or per invocation.
5. **The full tagged digest** (e.g., `sha256-md:<64-char-hex>`) is posted as-is -- the format tag must not be stripped.

### Tasks Created Summary

| Task Key | Type | Stream | Labels | Link to TC-8001 |
|----------|------|--------|--------|-----------------|
| TC-9001 | Upstream backport | 2.2.x | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| TC-9002 | Downstream propagation | 2.2.x | ai-generated-jira, Security, CVE-2026-31812 | Depend |
| TC-9003 | Preemptive upstream backport | 2.1.x | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |
| TC-9004 | Preemptive downstream propagation | 2.1.x | ai-generated-jira, Security, CVE-2026-31812, security-preemptive | Related |

Additional links:
- TC-9002 is blocked by TC-9001 (link type: Blocks)
- TC-9004 is blocked by TC-9003 (link type: Blocks)
