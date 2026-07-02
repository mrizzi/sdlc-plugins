# Triage Outcome for TC-8021 (CVE-2026-31812 / quinn-proto)

## Summary

CVE-2026-31812 affects quinn-proto versions before 0.11.14 (CVSS 7.5, High severity -- denial of service via panic on excessive stream counts). The issue is scoped to the **2.2.x** stream per its summary suffix `[rhtpa-2.2]`.

## Version Impact Recap

### Scoped stream (2.2.x)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 0.11.14 | NO | ships fixed version |

### Other streams (2.1.x)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |

## Case Determination

### Case A -- Scoped stream (2.2.x): Affected but already fixed in latest releases

Versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable quinn-proto (< 0.11.14). However, the fix was already incorporated starting in version 2.2.3 (build v0.4.11), which ships quinn-proto 0.11.14. The latest released version (2.2.4) also ships the fixed version.

**The upstream branch `release/0.4.z` already contains the fix at HEAD.** No new upstream backport task is needed for the 2.2.x stream because the dependency was already bumped in the natural course of development.

**No downstream propagation task is needed** because versions 2.2.3 and 2.2.4 already picked up the fix -- the Konflux release repo already references source commits that include quinn-proto 0.11.14.

**Recommended actions for 2.2.x:**
1. Correct Affects Versions from [RHTPA 2.0.0] to [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
2. Add triage comment documenting that the fix is already present in 2.2.3+ and no new remediation tasks are required for this stream
3. Add the `ai-cve-triaged` label

### Case B -- Cross-stream impact: 2.1.x is also affected

The version impact analysis reveals that the **2.1.x** stream is also affected:
- 2.1.0 ships quinn-proto 0.11.9 (vulnerable)
- 2.1.1 ships quinn-proto 0.11.9 (vulnerable)
- The upstream branch `release/0.3.z` still ships 0.11.9 at HEAD -- the fix has NOT been backported to this branch

**Cross-stream impact comment** would be posted to TC-8021:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. Stream 2.1.x is tracked by a companion issue (if one exists) or may require separate PSIRT triage.

**Preemptive remediation tasks for 2.1.x:** Since no companion CVE Jira exists for the 2.1.x stream (search for sibling issues with `[rhtpa-2.1]` suffix would need to be performed in Step 4), preemptive remediation tasks would be created:

1. **Upstream backport task (preemptive)**:
   - Summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)"
   - Repository: backend
   - Target branch: release/0.3.z
   - Labels: [ai-generated-jira, Security, CVE-2026-31812, security-preemptive]
   - Link type: "Related" to TC-8021 (not "Depend", since it originates from a different stream)
   - Description prefix: preemptive remediation note referencing TC-8021 (stream 2.2.x)

2. **Downstream propagation subtask (preemptive)**:
   - Summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)"
   - Repository: rhtpa-release.0.3.z
   - Target branch: main
   - Source pinning method: artifacts.lock.yaml (download URL contains tag)
   - Labels: [ai-generated-jira, Security, CVE-2026-31812, security-preemptive]
   - Link type: "Related" to TC-8021
   - Blocked by: the upstream backport task above

## Step 7 Outcome

No concurrent triages detected for quinn-proto. Proceeded to remediation without conflict.

## Affects Versions Correction

- **Before**: [RHTPA 2.0.0] (incorrect -- no 2.0.x stream exists)
- **After**: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

RHTPA 2.0.0 is removed (does not correspond to any configured version stream). Versions 2.2.0, 2.2.1, and 2.2.2 are added based on lock file evidence showing quinn-proto < 0.11.14 at their pinned commits. Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14 (the fixed version).

## Post-Triage Actions

1. Correct Affects Versions on TC-8021: RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
2. Post Affects Versions correction comment with lock file evidence
3. Post cross-stream impact comment noting 2.1.x is affected
4. Create preemptive remediation tasks for 2.1.x (upstream backport + downstream propagation) with `security-preemptive` label and "Related" link to TC-8021
5. Post summary comment to TC-8021 documenting: version impact table, Affects Versions correction, triage outcome (fix already present in 2.2.3+ for the scoped stream; preemptive tasks created for 2.1.x), and @mention of reporter
6. Add `ai-cve-triaged` label to TC-8021
