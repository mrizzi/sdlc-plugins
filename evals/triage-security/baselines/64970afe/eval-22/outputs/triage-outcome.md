# Triage Outcome -- TC-8021 (CVE-2026-31812)

## Summary

CVE-2026-31812 affects the quinn-proto crate (versions before 0.11.14), which is a Cargo (Rust) source dependency in the rhtpa-backend repository. The vulnerability allows a remote attacker to cause a denial of service (DoS) via panic by sending a QUIC transport frame that creates an excessive number of streams. CVSS score is 7.5 (High).

## Version Impact Table

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed version |

## Affects Versions Correction (Step 3)

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Corrected (scoped to 2.2.x stream)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

The PSIRT-assigned version "RHTPA 2.0.0" is incorrect -- no 2.0.x stream exists in the configuration. The correction is scoped to the 2.2.x stream per the issue suffix `[rhtpa-2.2]`. Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14 (the fixed version).

## Concurrent Triage Detection (Step 7)

No concurrent triages detected for upstream component quinn-proto. JQL search for in-progress triages with `cf[10632] ~ 'quinn-proto' AND status IN ('In Progress', 'Code Review') AND key != TC-8021` returned zero results. Proceeding to remediation.

## Triage Decision: Case A + Case B

### Case A -- Affected: Create Remediation Tasks (2.2.x stream)

The issue is scoped to stream 2.2.x. Within this stream, versions 2.2.0, 2.2.1, and 2.2.2 are affected. Since quinn-proto is a **Cargo** (source) dependency, two remediation tasks are required per the skill's ecosystem-based task creation rules:

1. **Upstream backport task** -- Bump quinn-proto to >= 0.11.14 in the rhtpa-backend source repository on the `release/0.4.z` branch. The upstream fix PR is available at quinn-rs/quinn#2048. Since versions 2.2.3+ already ship the fixed version, the upstream branch may already contain the fix. The upstream fix check (Step 2.5) should confirm whether `release/0.4.z` HEAD already includes quinn-proto 0.11.14.

2. **Downstream propagation subtask** -- Update the backend source reference in the Konflux release repo (`rhtpa-release.0.4.z`) to point to the upstream commit/tag that includes the fix. This subtask is blocked by the upstream task. The propagation would produce a new build that ships quinn-proto >= 0.11.14 for versions that need a respin (2.2.0, 2.2.1, 2.2.2).

Note: Since version 2.2.3 (build 0.4.11) already includes quinn-proto 0.11.14, the upstream fix is already present in the later builds. The remediation may focus on producing respins for the earlier affected versions or documenting that users should upgrade to >= 2.2.3.

### Case B -- Cross-Stream Impact (2.1.x stream)

The version impact analysis reveals that stream **2.1.x** (outside this issue's scope) is also affected:
- 2.1.0: quinn-proto 0.11.9 (affected)
- 2.1.1: quinn-proto 0.11.9 (affected)

Since this issue is scoped to 2.2.x, Case B applies:

1. **Post cross-stream impact comment** on TC-8021:
   > Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

2. **Check for existing CVE Jiras** for the 2.1.x stream -- search for sibling Vulnerability issues with the CVE-2026-31812 label and a `[rhtpa-2.1]` stream suffix.

3. **If no 2.1.x CVE Jira exists**: Create preemptive remediation tasks for the 2.1.x stream with the `security-preemptive` label, linked to TC-8021 with "Related" link type. Two tasks (upstream + downstream) following the Cargo ecosystem pattern:
   - Upstream: bump quinn-proto on `release/0.3.z` branch
   - Downstream: update backend reference in `rhtpa-release.0.3.z`

4. **If a 2.1.x CVE Jira exists**: Skip task creation for that stream -- it will be triaged through its own CVE issue.

### Case C -- Not Applicable

Case C (close as Not a Bug) does not apply because supported versions ARE affected within the issue's scoped stream.

## Post-Triage Actions

1. **Add `ai-cve-triaged` label** to TC-8021
2. **Post summary comment** to TC-8021 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
   - Remediation tasks created (upstream + downstream for 2.2.x, preemptive for 2.1.x if applicable)
   - @mention of the issue reporter (PSIRT analyst)
   - Comment Footnote per shared/comment-footnote.md

## Jira Mutations Required (pending engineer confirmation)

| Action | Details |
|--------|---------|
| Assign issue | Assign TC-8021 to current user |
| Transition | New -> Assigned |
| Correct Affects Versions | Remove RHTPA 2.0.0; add RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |
| Create upstream task (2.2.x) | Bump quinn-proto >= 0.11.14 in rhtpa-backend on release/0.4.z |
| Create downstream subtask (2.2.x) | Update backend ref in rhtpa-release.0.4.z (blocked by upstream task) |
| Create preemptive upstream task (2.1.x) | Bump quinn-proto >= 0.11.14 in rhtpa-backend on release/0.3.z (if no 2.1.x CVE Jira exists) |
| Create preemptive downstream subtask (2.1.x) | Update backend ref in rhtpa-release.0.3.z (if no 2.1.x CVE Jira exists) |
| Post cross-stream impact comment | Document 2.1.x impact on TC-8021 |
| Add label | ai-cve-triaged |
| Post summary comment | Full triage audit trail with version impact table |
