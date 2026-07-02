# Triage Outcome for TC-8020

## Issue Summary

- **Issue**: TC-8020
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Affected range**: < 0.11.14
- **Fixed version**: 0.11.14
- **Stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Ecosystem**: Cargo (Rust)

## Version Impact Summary

### In-scope stream (2.2.x)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | 0.11.12 (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO |
| 2.2.4 | 0.11.14 | NO |

### Out-of-scope stream (2.1.x -- cross-stream)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

## Step 3 -- Affects Versions Correction

- **Current Affects Versions**: RHTPA 2.0.0 (incorrect -- no 2.0 stream exists)
- **Proposed Affects Versions** (scoped to 2.2.x): RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14 (at or above the fix threshold)
- Correction requires engineer confirmation before Jira update

## Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

- **Step 4.1-4.2**: JQL search for sibling issues with label CVE-2026-31812 would be executed (no mock data provided for siblings, so assume no siblings found)
- **Step 4.3**: Cross-CVE overlap detection -- uses customfield_10632 (quinn-proto) to search for other CVE Jiras affecting the same component. Requires PS Component and Stream custom fields to also be configured; those are not explicitly listed in the mock Security Configuration, so this sub-step would be skipped per the prerequisite check
- **Step 4.4**: Preemptive task reconciliation -- search for existing preemptive tasks with labels `security-preemptive` and `CVE-2026-31812` for stream 2.2.x. Assume none found

## Step 5 -- Version Lifecycle Check

- Product pages URL: https://access.example.com/product-life-cycle/rhtpa
- Affected versions (2.2.0, 2.2.1, 2.2.2) would be checked against product lifecycle
- Assume all are within support lifecycle (actively supported)

## Step 6 -- Already Fixed Check

- No resolved sibling issues found (from Step 4)
- Proceed to Step 7

## Step 7 -- Concurrent Triage Detection

**WARNING**: Concurrent triage detected.

TC-8019 (status: In Progress, assignee: engineer-b@example.com) is actively being triaged on the same upstream component (quinn-proto).

Three options presented:
1. **Wait** -- pause until TC-8019 completes
2. **Skip** -- skip remediation task creation
3. **Proceed** -- create tasks with `concurrent-triage-overlap` label

The engineer must select an option before proceeding to Step 8.

## Step 8 -- Triage Decision (pending Step 7 resolution)

### Determination: Case A + Case B

**Case A (Affected -- in-scope stream 2.2.x):** Versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14 and are affected. Remediation tasks are required (subject to Step 7 outcome).

Since the ecosystem is **Cargo** (source dependency), two remediation tasks would be created:

1. **Upstream backport task** -- Backport the quinn-proto fix (bump to >= 0.11.14) in the rhtpa-backend source repository on branch `release/0.4.z`
2. **Downstream propagation subtask** -- Update the Konflux release repo (`rhtpa-release.0.4.z`) to reference the new backend build that includes the fix. This task is blocked by the upstream task.

Both tasks would be linked to TC-8020 with "Depend" link type.

**Case B (Cross-stream impact -- 2.1.x):** The 2.1.x stream (versions 2.1.0, 2.1.1) is also affected but is outside this issue's scope. Cross-stream impact actions:

- Post a cross-stream impact comment on TC-8020 noting that quinn-proto < 0.11.14 also affects stream 2.1.x
- Check for existing sibling CVE Jiras for 2.1.x with label CVE-2026-31812
- If no sibling CVE Jira exists for 2.1.x: create preemptive remediation tasks with `security-preemptive` label, linked to TC-8020 with "Related" link type
- If a sibling CVE Jira exists for 2.1.x: skip task creation for that stream (it will be triaged through its own issue)

### Post-Triage Actions (after Step 8 completes)

1. Add `ai-cve-triaged` label to TC-8020
2. Post summary comment to TC-8020 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
   - Concurrent triage warning (TC-8019)
   - Remediation tasks created (if any, depending on Step 7 resolution)
   - @mention of the issue reporter
   - Comment Footnote per `shared/comment-footnote.md`

## Key Findings

1. **PSIRT Affects Versions are incorrect**: RHTPA 2.0.0 does not correspond to any configured stream. The correct versions for the 2.2.x scope are RHTPA 2.2.0, RHTPA 2.2.1, and RHTPA 2.2.2.
2. **Partial fix already shipped**: Versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (the fix version), so they are not affected.
3. **Cross-stream impact**: The 2.1.x stream is also affected (quinn-proto 0.11.9 in both versions), requiring either sibling CVE tracking or preemptive remediation.
4. **Concurrent triage conflict**: TC-8019 is actively being triaged on the same upstream component (quinn-proto). The engineer must resolve this before remediation tasks can be created to avoid duplicates.
5. **Deployment context**: Defaults to `upstream` (no Deployment Context column in Source Repositories table).
