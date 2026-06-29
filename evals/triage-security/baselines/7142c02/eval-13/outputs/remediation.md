# Step 7 -- Remediation for CVE-2026-31812 (TC-8001)

## Triage Outcome

This is **Case A + Case B**: The issue's scoped stream (2.2.x) has affected versions (2.2.0, 2.2.1, 2.2.2), and the cross-stream analysis reveals the 2.1.x stream is also affected.

Since quinn-proto is a **Cargo** (source dependency) ecosystem, each affected stream requires **two tasks**: an upstream backport task and a downstream propagation subtask.

---

## Case A: Scoped Stream (2.2.x) Remediation Tasks

### Task 1: Upstream Backport Task (2.2.x stream)

**Jira Creation Call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)",
  description: <see below>,
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

Affected versions: 2.2.0 (quinn-proto 0.11.9), 2.2.1 (quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1)
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
- Note: versions 2.2.3+ already ship 0.11.14 on this branch, so the
  fix may already be present at branch HEAD

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Steps for Upstream Backport Task (2.2.x)

After the task is created (assume key TC-8002):

1. **Re-fetch the task description from Jira:**
   ```
   jira.get_issue("TC-8002", fields=["description"])
   ```
2. **Write the re-fetched description to a temp file:**
   ```
   Write the description content to /tmp/task-desc.md
   ```
3. **Compute SHA-256 digest using scripts/sha256-digest.py:**
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a format-tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.
4. **Post digest comment on TC-8002 BEFORE creating issue links or other comments:**
   ```
   jira.add_comment("TC-8002", "[sdlc-workflow] Description digest: <tagged-digest-output>")
   ```
   Where `<tagged-digest-output>` is the exact output from `scripts/sha256-digest.py` (e.g., `sha256-md:a1b2c3...64chars`).
5. **Only after posting the digest comment**, proceed to create issue links (Depend link to TC-8001).

---

### Task 2: Downstream Propagation Subtask (2.2.x stream)

**Jira Creation Call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)",
  description: <see below>,
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
CVE-2026-31812 fix from TC-8002.

The upstream backport (TC-8002) bumps quinn-proto to 0.11.14
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

- Depends on: TC-8002 (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Steps for Downstream Propagation Subtask (2.2.x)

After the task is created (assume key TC-8003):

1. **Re-fetch the task description from Jira:**
   ```
   jira.get_issue("TC-8003", fields=["description"])
   ```
2. **Write the re-fetched description to a temp file:**
   ```
   Write the description content to /tmp/task-desc.md
   ```
3. **Compute SHA-256 digest using scripts/sha256-digest.py:**
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a format-tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.
4. **Post digest comment on TC-8003 BEFORE creating issue links or other comments:**
   ```
   jira.add_comment("TC-8003", "[sdlc-workflow] Description digest: <tagged-digest-output>")
   ```
   Where `<tagged-digest-output>` is the exact output from `scripts/sha256-digest.py`.
5. **Only after posting the digest comment**, proceed to create issue links (Blocks link from TC-8002, Depend link to TC-8001).

---

## Jira Linkage for 2.2.x Tasks

After digest comments are posted on both tasks:

1. **Link upstream task to vulnerability:**
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: "TC-8002", type: "Depend")
   ```

2. **Link downstream subtask as blocked by upstream:**
   ```
   jira.create_link(inwardIssue: "TC-8002", outwardIssue: "TC-8003", type: "Blocks")
   ```

3. **Link downstream subtask to vulnerability:**
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: "TC-8003", type: "Depend")
   ```

---

## Case B: Cross-Stream Impact (2.1.x stream)

The version impact analysis shows the 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9). Since the issue is scoped to 2.2.x, the 2.1.x stream is out of scope. No separate CVE Jira exists for the 2.1.x stream (would need to check via JQL), so **preemptive remediation tasks** are created.

### Cross-Stream Impact Comment on TC-8001

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. All 2.1.x versions (2.1.0, 2.1.1) ship
quinn-proto 0.11.9 which is within the vulnerable range.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

### Preemptive Task 1: Upstream Backport (2.1.x stream)

**Jira Creation Call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)",
  description: <see below>,
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

Affected versions: 2.1.0 (quinn-proto 0.11.9), 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8 (2.1.0), v0.3.12 (2.1.1)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)
- Note: the fix has NOT been backported to release/0.3.z yet (latest
  tag v0.3.12 still ships quinn-proto 0.11.9)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Steps for Preemptive Upstream Backport Task (2.1.x)

After the task is created (assume key TC-8004):

1. **Re-fetch the task description from Jira:**
   ```
   jira.get_issue("TC-8004", fields=["description"])
   ```
2. **Write the re-fetched description to a temp file:**
   ```
   Write the description content to /tmp/task-desc.md
   ```
3. **Compute SHA-256 digest using scripts/sha256-digest.py:**
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a format-tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.
4. **Post digest comment on TC-8004 BEFORE creating issue links or other comments:**
   ```
   jira.add_comment("TC-8004", "[sdlc-workflow] Description digest: <tagged-digest-output>")
   ```
   Where `<tagged-digest-output>` is the exact output from `scripts/sha256-digest.py`.
5. **Only after posting the digest comment**, proceed to create issue links (Related link to TC-8001).

---

### Preemptive Task 2: Downstream Propagation Subtask (2.1.x stream)

**Jira Creation Call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see below>,
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
CVE-2026-31812 fix from TC-8004.

The upstream backport (TC-8004) bumps quinn-proto to 0.11.14
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

- Depends on: TC-8004 (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

#### Description Digest Steps for Preemptive Downstream Propagation Subtask (2.1.x)

After the task is created (assume key TC-8005):

1. **Re-fetch the task description from Jira:**
   ```
   jira.get_issue("TC-8005", fields=["description"])
   ```
2. **Write the re-fetched description to a temp file:**
   ```
   Write the description content to /tmp/task-desc.md
   ```
3. **Compute SHA-256 digest using scripts/sha256-digest.py:**
   ```bash
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This outputs a format-tagged digest, e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`.
4. **Post digest comment on TC-8005 BEFORE creating issue links or other comments:**
   ```
   jira.add_comment("TC-8005", "[sdlc-workflow] Description digest: <tagged-digest-output>")
   ```
   Where `<tagged-digest-output>` is the exact output from `scripts/sha256-digest.py`.
5. **Only after posting the digest comment**, proceed to create issue links (Blocks link from TC-8004, Related link to TC-8001).

---

## Jira Linkage for 2.1.x Preemptive Tasks

After digest comments are posted on both preemptive tasks:

1. **Link preemptive upstream task to vulnerability (Related, not Depend):**
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: "TC-8004", type: "Related")
   ```

2. **Link preemptive downstream subtask as blocked by upstream:**
   ```
   jira.create_link(inwardIssue: "TC-8004", outwardIssue: "TC-8005", type: "Blocks")
   ```

3. **Link preemptive downstream subtask to vulnerability (Related, not Depend):**
   ```
   jira.create_link(inwardIssue: "TC-8001", outwardIssue: "TC-8005", type: "Related")
   ```

---

## Preemptive Tasks Comment on TC-8001

After creating preemptive tasks, post this comment on TC-8001:

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: TC-8004 (upstream backport), TC-8005 (downstream propagation) (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

---

## Summary of All Remediation Tasks

| Task Key | Type | Stream | Summary | Labels |
|----------|------|--------|---------|--------|
| TC-8002 | Upstream backport | 2.2.x | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x) | ai-generated-jira, Security, CVE-2026-31812 |
| TC-8003 | Downstream propagation | 2.2.x | Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (2.2.x) | ai-generated-jira, Security, CVE-2026-31812 |
| TC-8004 | Upstream backport (preemptive) | 2.1.x | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive |
| TC-8005 | Downstream propagation (preemptive) | 2.1.x | Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x) | ai-generated-jira, Security, CVE-2026-31812, security-preemptive |

## Description Digest Protocol Summary

For every task created above, the following sequence is mandatory:

1. Create the task via `jira.create_issue(...)`
2. **Re-fetch** the task description from Jira (do NOT use the description string passed to `create_issue`, because Jira normalizes content during storage)
3. Write the re-fetched description to a temp file
4. Compute the digest via `python3 scripts/sha256-digest.py /tmp/task-desc.md` (outputs format-tagged digest like `sha256-md:<64-hex-chars>` or `sha256-adf:<64-hex-chars>`)
5. Post the digest comment: `[sdlc-workflow] Description digest: <tagged-digest-output>`
6. **THEN** create issue links (Depend, Blocks, Related) and post other comments

The digest comment is posted **before** any issue links or other comments. The digest is computed from the **re-fetched** description, not the original string passed to `create_issue`. The full 64-character hex digest with format tag must be used -- no abbreviations, no placeholders, no hardcoded values.
