# Triage Outcome for TC-8020 (CVE-2026-31812 / quinn-proto)

## Triage Decision: Case A + Case B (Affected with Cross-Stream Impact)

### Rationale

The version impact analysis shows that **supported versions in the 2.2.x stream are affected**:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.2.0 | 0.11.9 | YES |
| RHTPA 2.2.1 | 0.11.12 | YES |
| RHTPA 2.2.2 | 0.11.12 (retag of 2.2.1) | YES |
| RHTPA 2.2.3 | 0.11.14 | NO (fixed) |
| RHTPA 2.2.4 | 0.11.14 | NO (fixed) |

Since supported versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto versions below the fix threshold (0.11.14), this is **Case A** -- affected versions exist and remediation is needed.

Additionally, the cross-stream check reveals that the **2.1.x stream is also affected** (all versions ship quinn-proto 0.11.9). Since TC-8020 is scoped to the 2.2.x stream (per the `[rhtpa-2.2]` suffix), the 2.1.x impact triggers **Case B** -- cross-stream impact requiring proactive remediation or a cross-stream notice.

### Step 7 Gate: Concurrent Triage

Before proceeding to remediation task creation, Step 7 detected that TC-8019 is actively being triaged by engineer-b@example.com for the same upstream component (quinn-proto). The engineer must choose:

1. **Wait** -- pause until TC-8019 completes
2. **Skip** -- skip task creation for TC-8020
3. **Proceed** -- create tasks with `concurrent-triage-overlap` label

Remediation task creation (below) only proceeds if the engineer selects option 3.

### Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is incorrect and must be corrected:

- **Current**: RHTPA 2.0.0 (no 2.0.x stream exists; this is a PSIRT error)
- **Corrected** (scoped to 2.2.x): RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

Versions 2.2.3 and 2.2.4 are excluded because they already ship the fixed version (quinn-proto 0.11.14).

### Case A Actions: Remediation Tasks for 2.2.x Stream

Since quinn-proto is a **Cargo** (source dependency) ecosystem, two tasks are required:

**Task 1 -- Upstream Backport (source repo fix)**
- Issue type: Task
- Summary: `Bump quinn-proto to >= 0.11.14 in rhtpa-backend (release/0.4.z) [CVE-2026-31812]`
- Labels: `CVE-2026-31812`, `security`, `concurrent-triage-overlap` (if Proceed chosen in Step 7)
- Description: Bump quinn-proto from vulnerable versions to >= 0.11.14 in the rhtpa-backend repository on the release/0.4.z branch. Upstream fix PR: quinn-rs/quinn#2048.
- Link: Depend (TC-8020 depends on this task)

**Task 2 -- Downstream Propagation (Konflux release repo update)**
- Issue type: Task (subtask of Task 1)
- Summary: `Propagate quinn-proto fix to rhtpa-release.0.4.z [CVE-2026-31812]`
- Labels: `CVE-2026-31812`, `security`
- Description: After the upstream fix lands, update the artifacts.lock.yaml in rhtpa-release.0.4.z to reference a backend build tag that includes quinn-proto >= 0.11.14.
- Blocked by: Task 1 (upstream backport)
- Link: Depend (TC-8020 depends on this task)

### Case B Actions: Cross-Stream Impact on 2.1.x

The 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9), but TC-8020 is scoped to 2.2.x only.

**Cross-stream impact comment** posted to TC-8020:
> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis.
> These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.

**Check for existing CVE Jiras for 2.1.x**: Search for sibling Vulnerability issues with label CVE-2026-31812 and suffix `[rhtpa-2.1]`.

- If a 2.1.x CVE Jira exists: link as Related and skip proactive task creation for 2.1.x (that stream's CVE will be triaged separately).
- If no 2.1.x CVE Jira exists: create **preemptive remediation tasks** for the 2.1.x stream with `security-preemptive` label and "Related" link type to TC-8020.

### Not Applicable: Case C

Case C (no supported versions affected) does not apply because versions 2.2.0, 2.2.1, and 2.2.2 are confirmed affected.

### Post-Triage Summary

After all actions are complete:
1. Add label `ai-cve-triaged` to TC-8020.
2. Post a summary comment to TC-8020 documenting:
   - Version impact table (both streams)
   - Affects Versions correction: RHTPA 2.0.0 replaced with RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
   - Triage outcome: Case A (remediation tasks created for 2.2.x) + Case B (cross-stream notice for 2.1.x)
   - Links to all remediation tasks created
   - @mention of the issue reporter (PSIRT analyst)
   - Comment Footnote per shared/comment-footnote.md with skill name `triage-security`

### Key Observations

1. **Partially fixed in latest releases**: The vulnerability was already remediated in RHTPA 2.2.3 and 2.2.4 (which ship quinn-proto 0.11.14). This means the fix has already been applied upstream -- the remediation tasks for 2.2.x may need to focus on backporting or patch releases for the older 2.2.0-2.2.2 versions that are still in support.

2. **PSIRT Affects Versions was incorrect**: PSIRT assigned "RHTPA 2.0.0" which does not correspond to any configured version stream. This is a common PSIRT error that the triage process corrects.

3. **Concurrent triage risk**: TC-8019 is in progress for the same component. The engineer should coordinate with engineer-b@example.com to avoid duplicate remediation work.

4. **Due date pressure**: The due date of 2026-07-15 is imminent (6 days away), which favors the "Proceed" option in Step 7 rather than waiting for TC-8019 to complete.
