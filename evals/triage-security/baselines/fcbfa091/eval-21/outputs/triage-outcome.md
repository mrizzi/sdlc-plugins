# Triage Outcome for TC-8020

## Summary

**Issue**: TC-8020 -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**CVE**: CVE-2026-31812
**Library**: quinn-proto
**Fix threshold**: 0.11.14
**Issue stream scope**: 2.2.x

## Version Impact Summary

### Stream 2.2.x (issue-scoped)

| Product Version | quinn-proto | Affected? |
|-----------------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO |
| 2.2.4 | 0.11.14 | NO |

### Stream 2.1.x (out of scope for this issue)

| Product Version | quinn-proto | Affected? |
|-----------------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

## Affects Versions Correction (Step 3)

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Proposed correction**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

The PSIRT-assigned version RHTPA 2.0.0 is incorrect -- no 2.0.x stream exists in the configured Version Streams. Lock file analysis confirms that versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto below the 0.11.14 fix threshold. Versions 2.2.3 and 2.2.4 already ship the fixed version and are not included. The 2.1.x versions are affected but belong to a different stream scope and are excluded from this issue's Affects Versions.

## Concurrent Triage Detection (Step 7)

**Concurrent triage detected.** TC-8019 is currently In Progress, assigned to engineer-b@example.com, and targets the same upstream component (quinn-proto). Step 7 fires before Case A/B/C branching and requires the engineer to choose:

1. **Wait** -- pause until TC-8019 completes, then re-run to detect overlap
2. **Skip** -- skip remediation task creation entirely
3. **Proceed** -- create tasks with `concurrent-triage-overlap` label for cross-detection

The triage decision below assumes the engineer chooses to proceed (Option 3), but the actual path depends on user input.

## Triage Decision

### Case A + Case B applies

Since this issue is scoped to stream 2.2.x and versions 2.2.0, 2.2.1, and 2.2.2 are affected, this is **Case A: Affected -- create remediation tasks** for the 2.2.x stream.

Additionally, the version impact analysis shows that **stream 2.1.x is also affected** (all versions ship quinn-proto 0.11.9, well below the fix threshold). This triggers **Case B: Cross-stream impact**. A cross-stream impact comment is posted to TC-8020, and if no companion CVE Jira exists for stream 2.1.x, proactive (preemptive) remediation tasks are created with the `security-preemptive` label.

### Remediation Tasks (if engineer proceeds)

Since quinn-proto is a **Cargo** (source dependency) ecosystem, two tasks are created per affected stream:

**For stream 2.2.x (issue-scoped -- standard remediation):**

1. **Upstream backport task** -- Bump quinn-proto from vulnerable version to >= 0.11.14 in the `rhtpa-backend` source repository on branch `release/0.4.z`. References upstream fix PR quinn-rs/quinn#2048.
   - Link type: Depend (from TC-8020)
   - Labels: security, CVE-2026-31812, concurrent-triage-overlap (if Option 3 chosen)

2. **Downstream propagation subtask** -- Update the `artifacts.lock.yaml` reference in the `rhtpa-release.0.4.z` Konflux release repo to point to the new backend build containing the fix.
   - Blocked by: upstream backport task
   - Link type: subtask of upstream task

**For stream 2.1.x (cross-stream -- preemptive, if no companion CVE Jira exists):**

1. **Preemptive upstream backport task** -- Bump quinn-proto to >= 0.11.14 in `rhtpa-backend` on branch `release/0.3.z`.
   - Labels: security, CVE-2026-31812, security-preemptive
   - Link type: Related (to TC-8020, not Depend)

2. **Preemptive downstream propagation subtask** -- Update `artifacts.lock.yaml` in `rhtpa-release.0.3.z`.
   - Blocked by: preemptive upstream task

### Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8020
2. Post summary comment to TC-8020 with version impact table, Affects Versions correction, remediation task links, and @mention of the issue reporter
3. If Option 3 was chosen in Step 7, the `concurrent-triage-overlap` label is added so TC-8019's triage Step 4.3 detects the overlap
