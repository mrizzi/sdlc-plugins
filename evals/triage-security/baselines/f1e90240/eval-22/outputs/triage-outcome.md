# Step 8 -- Triage Outcome for TC-8021

## Summary

**CVE**: CVE-2026-31812
**Library**: quinn-proto
**Fix threshold**: >= 0.11.14
**Issue scope**: Stream 2.2.x (from summary suffix `[rhtpa-2.2]`)
**Ecosystem**: Cargo (source dependency)

## Version Impact Recap

| Version | Stream | quinn-proto | Affected? |
|---------|--------|-------------|-----------|
| 2.1.0 | 2.1.x | 0.11.9 | YES |
| 2.1.1 | 2.1.x | 0.11.9 | YES |
| 2.2.0 | 2.2.x | 0.11.9 | YES |
| 2.2.1 | 2.2.x | 0.11.12 | YES |
| 2.2.2 | 2.2.x | 0.11.12 | YES (retag of 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO |
| 2.2.4 | 2.2.x | 0.11.14 | NO |

## Step 3 -- Affects Versions Correction

The PSIRT-assigned Affects Versions field is **RHTPA 2.0.0**, which is incorrect -- there is no 2.0.x stream in the configured Version Streams. The issue is scoped to stream 2.2.x, so only 2.2.x affected versions should be set.

**Correction:**
- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14, which is at or above the fix threshold.

A comment would be posted documenting the correction with lock file evidence from `security-matrix.md`, scoped to the 2.2.x stream per the issue suffix.

## Step 4 -- Duplicate, Sibling, and Overlap Check

### Step 4.1/4.2 -- Sibling Detection

A JQL search for sibling Vulnerability issues with label `CVE-2026-31812` would identify any companion trackers for other streams. No sibling data was provided in this eval scenario, so we assume no siblings exist.

### Step 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component field (`customfield_10632`) is configured and set to `quinn-proto`. A search for other Vulnerability issues with the same component value would check whether a different CVE's remediation already bumps quinn-proto past 0.11.14. No overlap data was provided in this eval scenario, so we assume no cross-CVE overlap exists.

### Step 4.4 -- Preemptive Task Reconciliation

A search for preemptive tasks with labels `security-preemptive` and `CVE-2026-31812` would check for existing proactive remediation tasks. No preemptive task data was provided, so we assume none exist.

## Step 5 -- Version Lifecycle Check

A check against the product lifecycle page (https://access.example.com/product-life-cycle/rhtpa) would verify that all affected versions are still within support. For this eval, we assume both 2.1.x and 2.2.x streams are actively supported.

## Step 6 -- Already Fixed Check

No resolved sibling issues were found in Step 4, so the already-fixed check produces no results. Proceed to Step 7.

## Step 7 -- Concurrent Triage Detection

As documented in `concurrent-triage.md`, the JQL search for in-progress triages on the same upstream component (`quinn-proto`) returned zero results. No concurrent triages detected. Proceed to Case A/B/C branching.

## Triage Decision

### Case Determination

The issue is **scoped** to stream 2.2.x. Within that scope:
- **2.2.x versions affected**: 2.2.0, 2.2.1, 2.2.2 (3 of 5 versions)
- **2.2.x versions not affected**: 2.2.3, 2.2.4 (already ship the fix)

Since supported versions within the issue's scope ARE affected, this is **Case A: Affected -- create remediation tasks**.

Additionally, the version impact analysis reveals that the **2.1.x stream** (outside this issue's scope) is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). This triggers **Case B: Cross-stream impact**.

### Case B -- Cross-Stream Impact

A cross-stream impact comment would be posted on TC-8021:

> Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

A search for existing CVE Jiras for the 2.1.x stream with label `CVE-2026-31812` would determine whether preemptive tasks are needed. If no 2.1.x CVE Jira exists, preemptive remediation tasks would be created with the `security-preemptive` label and linked to TC-8021 via "Related" link type.

### Case A -- Remediation Task Creation (2.2.x stream)

Since quinn-proto is a **Cargo** (source dependency) ecosystem, **two tasks** would be created for the 2.2.x stream:

#### Task 1: Upstream Backport Task

- **Summary**: `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)`
- **Repository**: rhtpa-backend
- **Target Branch**: release/0.4.z
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Description**: Remediate CVE-2026-31812 by bumping quinn-proto to >= 0.11.14 on the release/0.4.z branch. The upstream fix PR is [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048). Affected versions: 2.2.0 (v0.4.5, quinn-proto 0.11.9), 2.2.1 (v0.4.8, quinn-proto 0.11.12), 2.2.2 (v0.4.9, retag of 2.2.1).
- **Note**: The upstream fix is already present at v0.4.11+ on the release/0.4.z branch, meaning the fix was already applied in the source repo. The upstream backport task may already be satisfied -- the engineer should verify whether the fix commit is already on the target branch.

#### Task 2: Downstream Propagation Subtask

- **Summary**: `Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
- **Repository**: rhtpa-release.0.4.z
- **Target Branch**: main
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Blocked by**: Task 1 (upstream backport)
- **Description**: Update the rhtpa-backend source reference in rhtpa-release.0.4.z to pick up the quinn-proto fix. Source pinning method: `artifacts.lock.yaml` (download URL contains tag). The fix is already present in tags v0.4.11 and v0.4.12. Versions 2.2.3 and 2.2.4 already ship the fix, confirming the upstream source has the patch.

#### Linkage

- Both tasks linked to TC-8021 with link type "Depend"
- Task 2 linked to Task 1 with link type "Blocks" (downstream blocked by upstream)
- TC-8021 transitioned to "In Progress"

### Post-Triage Summary

A summary comment would be posted on TC-8021 documenting:
1. The version impact table (all versions across both streams)
2. The Affects Versions correction: `[RHTPA 2.0.0]` corrected to `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
3. The triage outcome: Case A (remediation tasks created for 2.2.x) + Case B (cross-stream impact on 2.1.x)
4. Links to created remediation tasks
5. An @mention of the vulnerability issue's reporter

The `ai-cve-triaged` label would be added to TC-8021 to mark it as triaged.

### Key Observations

1. **PSIRT Affects Versions were incorrect**: RHTPA 2.0.0 does not correspond to any configured version stream. The correct affected versions within the issue's 2.2.x scope are RHTPA 2.2.0, 2.2.1, and 2.2.2.
2. **Fix already partially shipped**: Versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (the fixed version), meaning the upstream fix was incorporated in build v0.4.11. Only versions 2.2.0-2.2.2 remain affected.
3. **Cross-stream impact**: The 2.1.x stream is also affected (both versions ship quinn-proto 0.11.9), but this is outside the current issue's scope and would be handled by PSIRT creating a stream-specific CVE Jira or via preemptive remediation tasks (Case B).
4. **No concurrent triages**: No other engineer is actively triaging a CVE affecting quinn-proto, so remediation task creation can proceed without risk of duplication.
