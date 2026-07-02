# Triage Outcome: TC-8021 (CVE-2026-31812)

## Summary

CVE-2026-31812 affects `quinn-proto` versions before 0.11.14. The vulnerability allows a remote attacker to cause a denial of service (DoS) by sending a QUIC transport frame that creates an excessive number of streams, leading to a panic.

## Version Impact Table

### Stream 2.2.x (in scope -- per issue suffix [rhtpa-2.2])

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | 0.11.12 | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | fixed version |
| 2.2.4 | 0.11.14 | NO | fixed version |

### Stream 2.1.x (cross-stream -- out of scope for this issue)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |

## Affects Versions Correction

PSIRT assigned `RHTPA 2.0.0` which is incorrect -- there is no 2.0.x version stream. The corrected Affects Versions (scoped to the 2.2.x stream) are:

- **Current**: [RHTPA 2.0.0]
- **Corrected**: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

## Concurrent Triage Detection (Step 7)

No concurrent triages detected on the `quinn-proto` upstream component (customfield_10632). JQL search for in-progress triages with `cf[10632] ~ 'quinn-proto'` returned zero results. Proceeding with remediation.

## Triage Decision: Case A + Case B

### Case A -- Affected (create remediation tasks for 2.2.x)

Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship quinn-proto < 0.11.14 and are affected. The ecosystem is Cargo (source dependency), so two remediation tasks would be created:

1. **Upstream backport task**: Bump `quinn-proto` to >= 0.11.14 in `rhtpa-backend` on branch `release/0.4.z`
   - Summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)"
   - Labels: ai-generated-jira, Security, CVE-2026-31812
   - Linked to TC-8021 with "Depend"

2. **Downstream propagation subtask**: Update backend source reference in `rhtpa-release.0.4.z` to pick up the upstream fix
   - Summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)"
   - Labels: ai-generated-jira, Security, CVE-2026-31812
   - Blocked by the upstream backport task
   - Linked to TC-8021 with "Depend"

Note: Versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (the fixed version) and are NOT affected. The fix was incorporated starting with build tag v0.4.11.

### Case B -- Cross-stream impact (2.1.x also affected)

The version impact analysis reveals that the 2.1.x stream (rhtpa-release.0.3.z) is also affected:
- 2.1.0 ships quinn-proto 0.11.9
- 2.1.1 ships quinn-proto 0.11.9

Both are below the fix threshold of 0.11.14.

Actions for Case B:
1. Post cross-stream impact comment on TC-8021:
   > Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream 2.1.x based on lock file analysis.

2. Search for sibling Vulnerability issues with label CVE-2026-31812 and stream suffix [rhtpa-2.1]. If no sibling exists for the 2.1.x stream, create preemptive remediation tasks:

   - **Preemptive upstream task**: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)"
     - Labels: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
     - Linked to TC-8021 with "Related" (not "Depend", because this is a different stream)

   - **Preemptive downstream task**: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)"
     - Labels: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
     - Blocked by the preemptive upstream task

   When PSIRT creates a stream-specific CVE Jira for 2.1.x, Step 4.4 reconciliation will link the preemptive tasks and remove the security-preemptive label.

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8021
2. Post summary comment on TC-8021 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, 2.2.1, 2.2.2)
   - Remediation tasks created (upstream + downstream for 2.2.x)
   - Preemptive tasks created for 2.1.x (if no sibling CVE Jira exists)
   - @mention of the issue reporter
3. Transition TC-8021 to In Progress
