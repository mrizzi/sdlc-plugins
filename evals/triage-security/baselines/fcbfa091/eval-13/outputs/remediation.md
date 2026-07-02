# Step 8 -- Remediation: CVE-2026-31812

## Triage Outcome

- **Case A (Affected):** Stream 2.2.x (scoped) has affected versions 2.2.0, 2.2.1, 2.2.2. Create remediation tasks.
- **Case B (Cross-stream impact):** Stream 2.1.x (out of scope) is also affected in all versions (2.1.0, 2.1.1). Create preemptive remediation tasks.

The ecosystem is **Cargo** (source dependency), so each stream requires **two tasks**: an upstream backport task and a downstream propagation subtask.

---

## Stream 2.2.x -- Standard Remediation Tasks (Case A)

### Task 1: Upstream Backport Task

**Jira creation call:**

```
upstream_task_2_2 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

```markdown
## Repository

backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (v0.4.5, quinn-proto 0.11.9), 2.2.1 (v0.4.8, quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1)
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

#### Description Digest Comment -- Upstream Backport Task (2.2.x)

After creating the upstream backport task, perform the description digest protocol:

1. **Re-fetch the description from Jira** (do NOT hash the string passed to create_issue -- Jira normalizes content during storage):
   ```
   upstream_desc = jira.get_issue(<upstream-task-2.2-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file and compute SHA-256 digest:**
   ```
   # Write the re-fetched description to a temp file
   # Then compute the digest using the script:
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output will be either sha256-md:<64-char-hex> or sha256-adf:<64-char-hex>
   # depending on whether the Jira API returned markdown or ADF JSON
   ```

3. **Post the digest comment BEFORE creating any issue links or other comments:**
   ```
   jira.add_comment(<upstream-task-2.2-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```
   Where `<tagged-digest>` is the full output from `scripts/sha256-digest.py` (e.g., `sha256-md:a1b2c3...64chars`).

4. **Only after the digest comment is posted**, proceed to create issue links:
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream-task-2.2-key>,
     type: "Depend"
   )
   ```

---

### Task 2: Downstream Propagation Subtask

**Jira creation call:**

```
downstream_task_2_2 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812"]
)
```

**Task description:**

```markdown
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from <upstream-task-2.2-key>.

The upstream backport (<upstream-task-2.2-key>) bumps quinn-proto to 0.11.14
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

- Depends on: <upstream-task-2.2-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Comment -- Downstream Propagation Subtask (2.2.x)

After creating the downstream propagation subtask, perform the description digest protocol:

1. **Re-fetch the description from Jira** (do NOT hash the string passed to create_issue):
   ```
   downstream_desc = jira.get_issue(<downstream-task-2.2-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file and compute SHA-256 digest:**
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex> or sha256-adf:<64-char-hex>
   ```

3. **Post the digest comment BEFORE creating any issue links or other comments:**
   ```
   jira.add_comment(<downstream-task-2.2-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

4. **Only after the digest comment is posted**, proceed to create issue links:
   ```
   # Link downstream subtask to the vulnerability issue
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-2.2-key>,
     type: "Depend"
   )

   # Link downstream subtask as blocked by upstream task
   jira.create_link(
     inwardIssue: <upstream-task-2.2-key>,
     outwardIssue: <downstream-task-2.2-key>,
     type: "Blocks"
   )
   ```

---

## Stream 2.1.x -- Preemptive Remediation Tasks (Case B)

Stream 2.1.x is outside the issue's scope (TC-8001 is scoped to 2.2.x) but is also affected. These tasks are created proactively with the `security-preemptive` label and linked with "Related" (not "Depend") to the originating CVE.

### Task 3: Preemptive Upstream Backport Task

**Jira creation call:**

```
upstream_task_2_1 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description:**

```markdown
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

#### Description Digest Comment -- Preemptive Upstream Backport Task (2.1.x)

After creating the preemptive upstream backport task, perform the description digest protocol:

1. **Re-fetch the description from Jira** (do NOT hash the string passed to create_issue):
   ```
   upstream_desc_2_1 = jira.get_issue(<upstream-task-2.1-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file and compute SHA-256 digest:**
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex> or sha256-adf:<64-char-hex>
   ```

3. **Post the digest comment BEFORE creating any issue links or other comments:**
   ```
   jira.add_comment(<upstream-task-2.1-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

4. **Only after the digest comment is posted**, proceed to create issue links (using "Related" for preemptive tasks):
   ```
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <upstream-task-2.1-key>,
     type: "Related"
   )
   ```

---

### Task 4: Preemptive Downstream Propagation Subtask

**Jira creation call:**

```
downstream_task_2_1 = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]
)
```

**Task description:**

```markdown
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
CVE-2026-31812 fix from <upstream-task-2.1-key>.

The upstream backport (<upstream-task-2.1-key>) bumps quinn-proto to 0.11.14
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

- Depends on: <upstream-task-2.1-key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Comment -- Preemptive Downstream Propagation Subtask (2.1.x)

After creating the preemptive downstream propagation subtask, perform the description digest protocol:

1. **Re-fetch the description from Jira** (do NOT hash the string passed to create_issue):
   ```
   downstream_desc_2_1 = jira.get_issue(<downstream-task-2.1-key>, fields=["description"])
   ```

2. **Write the re-fetched description to a temp file and compute SHA-256 digest:**
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   # Output: sha256-md:<64-char-hex> or sha256-adf:<64-char-hex>
   ```

3. **Post the digest comment BEFORE creating any issue links or other comments:**
   ```
   jira.add_comment(<downstream-task-2.1-key>,
     "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

4. **Only after the digest comment is posted**, proceed to create issue links:
   ```
   # Link to originating CVE with "Related" (preemptive)
   jira.create_link(
     inwardIssue: "TC-8001",
     outwardIssue: <downstream-task-2.1-key>,
     type: "Related"
   )

   # Link downstream subtask as blocked by upstream task
   jira.create_link(
     inwardIssue: <upstream-task-2.1-key>,
     outwardIssue: <downstream-task-2.1-key>,
     type: "Blocks"
   )
   ```

---

## Description Digest Protocol Summary

For every remediation task created (all 4 tasks above), the description digest protocol follows this exact sequence:

1. **Create the task** via `jira.create_issue(...)`.
2. **Re-fetch the description** from Jira using `jira.get_issue(<task-key>, fields=["description"])`. This is mandatory because Jira normalizes content during storage -- the stored description may differ from the string passed to `create_issue`.
3. **Write the re-fetched description** to a temp file (e.g., `/tmp/task-desc.md`).
4. **Compute the SHA-256 digest** using `python3 scripts/sha256-digest.py /tmp/task-desc.md`. The script auto-detects the format (markdown vs ADF JSON) and outputs a format-tagged digest: either `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.
5. **Post the digest comment** on the task: `jira.add_comment(<task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")`. The comment marker is exactly `[sdlc-workflow] Description digest:` followed by the full tagged digest value.
6. **Only then create issue links** (`jira.create_link(...)`) and any other comments. The digest comment MUST be posted before issue links or other comments.

Key rules from the protocol:
- Never hash the description string passed to `create_issue` -- always re-fetch from Jira after creation
- Never use placeholder, abbreviated, or example hashes -- the digest must be the actual 64-character hex value computed from the re-fetched description
- Never strip the format tag (`sha256-md:` or `sha256-adf:`) -- it is part of the digest value
- The digest comment is a standalone comment, not embedded in other comments
- Digest comments are posted BEFORE issue links -- this ordering is mandatory

## Cross-Stream Impact Comment

After creating all preemptive tasks for stream 2.1.x, post a comment on TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. All versions in 2.1.x (2.1.0, 2.1.1) ship
quinn-proto 0.11.9.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-2.1-key> (upstream backport, security-preemptive),
         <downstream-task-2.1-key> (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```
