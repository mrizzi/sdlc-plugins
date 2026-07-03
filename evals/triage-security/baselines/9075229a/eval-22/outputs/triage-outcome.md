# Triage Outcome: TC-8021 (CVE-2026-31812 / quinn-proto)

## Version Impact Summary

| Stream | Version | quinn-proto | Affected? |
|--------|---------|-------------|-----------|
| 2.1.x | 2.1.0 | 0.11.9 | YES |
| 2.1.x | 2.1.1 | 0.11.9 | YES |
| **2.2.x** | **2.2.0** | **0.11.9** | **YES** |
| **2.2.x** | **2.2.1** | **0.11.12** | **YES** |
| **2.2.x** | **2.2.2** | **0.11.12 (retag of 2.2.1)** | **YES** |
| 2.2.x | 2.2.3 | 0.11.14 | NO |
| 2.2.x | 2.2.4 | 0.11.14 | NO |

Fix threshold: quinn-proto >= 0.11.14

## Triage Decision: Case A + Case B

### Case A -- Affected (create remediation tasks for scoped stream 2.2.x)

The issue is scoped to stream **2.2.x** via the summary suffix `[rhtpa-2.2]`. Within this stream, versions **2.2.0, 2.2.1, and 2.2.2** are affected. They ship quinn-proto versions 0.11.9 and 0.11.12, both below the fix threshold of 0.11.14.

Versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (the fixed version) and are NOT affected.

**Ecosystem**: Cargo (source dependency) -- requires **two remediation tasks**:

1. **Upstream backport task**: Bump quinn-proto to >= 0.11.14 in the source repository `rhtpa-backend` on branch `release/0.4.z`. The fix is available via upstream PR quinn-rs/quinn#2048.

2. **Downstream propagation subtask**: After the upstream fix is merged, update the Konflux release repo `rhtpa-release.0.4.z` to reference the new backend build that includes the quinn-proto fix. This subtask is blocked by the upstream task.

Both tasks would be linked to TC-8021 with link type "Depend".

### Case B -- Cross-stream impact (proactive remediation for 2.1.x)

The version impact analysis reveals that stream **2.1.x** is also affected:
- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

This stream is outside the current issue's scope (scoped to 2.2.x).

**Cross-stream impact actions:**

1. **Post cross-stream impact comment** on TC-8021:
   > Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. Stream 2.1.x is tracked by companion issues (see Related links) or may require separate PSIRT triage.

2. **Check for existing CVE Jiras** for stream 2.1.x: Search for sibling Vulnerability issues with label CVE-2026-31812 and summary suffix `[rhtpa-2.1]` (Step 4 JQL results).

3. **If no existing CVE Jira for 2.1.x**: Create preemptive remediation tasks with `security-preemptive` label:
   - Upstream backport task for `rhtpa-backend` on branch `release/0.3.z`
   - Downstream propagation subtask for `rhtpa-release.0.3.z`
   - Both linked to TC-8021 with link type "Related" (not "Depend", since this is preemptive)

4. **If a CVE Jira already exists for 2.1.x**: Skip task creation for that stream -- it will be triaged through its own CVE issue.

### Affects Versions Correction (Step 3)

| Current | Proposed |
|---------|----------|
| RHTPA 2.0.0 | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

Rationale: RHTPA 2.0.0 is incorrect -- no 2.0.x stream exists in the configuration. The correct Affects Versions for the scoped stream (2.2.x) are 2.2.0, 2.2.1, and 2.2.2 based on lock file evidence showing quinn-proto < 0.11.14. Versions 2.2.3 and 2.2.4 are excluded because they ship the fixed version.

### Concurrent Triage (Step 7)

No concurrent triages detected for the `quinn-proto` upstream component. Proceeding with remediation task creation without risk of duplication.

## Post-Triage Actions

1. **Add `ai-cve-triaged` label** to TC-8021.
2. **Post summary comment** to TC-8021 documenting:
   - Version impact table (above)
   - Affects Versions correction: RHTPA 2.0.0 replaced with RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
   - Remediation tasks created (upstream + downstream for 2.2.x stream)
   - Cross-stream impact on 2.1.x
   - @mention of the issue reporter (PSIRT analyst)
   - Comment Footnote per shared/comment-footnote.md (skill: triage-security)
3. **All Jira mutations require engineer confirmation** before execution.
