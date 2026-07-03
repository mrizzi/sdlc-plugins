# Triage Outcome for TC-8021 (CVE-2026-31812)

## Version Impact Summary

**CVE-2026-31812**: quinn-proto denial of service -- panic on large stream counts. Versions before 0.11.14 are vulnerable. Fixed in 0.11.14.

### Stream 2.2.x (issue-scoped)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | (retag) | YES | same as 2.2.1 |
| 2.2.3 | 0.11.14 | NO | fixed version |
| 2.2.4 | 0.11.14 | NO | fixed version |

### Stream 2.1.x (cross-stream)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 0.11.9 | YES | < 0.11.14 |

## Affects Versions Correction

- **Current (PSIRT-assigned):** RHTPA 2.0.0
- **Proposed (from lock file evidence):** RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

RHTPA 2.0.0 does not correspond to any configured version stream and is incorrect. The correction is scoped to stream 2.2.x per the issue suffix `[rhtpa-2.2]`. Versions 2.2.3 and 2.2.4 are excluded because they already ship quinn-proto 0.11.14 (the fixed version).

## Concurrent Triage Detection (Step 7)

No concurrent triages detected for upstream component `quinn-proto`. Proceeding to remediation.

## Triage Decision

### Case A -- Affected (2.2.x stream): Create Remediation Tasks

Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship vulnerable quinn-proto (< 0.11.14). Since this is a **Cargo** (source dependency) ecosystem, two remediation tasks are needed:

**Task 1 -- Upstream Backport:**
- **Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)
- **Repository:** rhtpa-backend
- **Target Branch:** release/0.4.z
- **Action:** Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- **Labels:** ai-generated-jira, Security, CVE-2026-31812
- **Link:** Depend on TC-8021

**Task 2 -- Downstream Propagation (blocked by Task 1):**
- **Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
- **Repository:** rhtpa-release.0.4.z
- **Target Branch:** main
- **Action:** Update the backend source reference (in artifacts.lock.yaml) to pick up the upstream fix once Task 1 merges
- **Source Pinning Method:** artifacts.lock.yaml (download URL contains tag)
- **Labels:** ai-generated-jira, Security, CVE-2026-31812
- **Link:** Depend on TC-8021; Blocked by Task 1

### Case B -- Cross-Stream Impact (2.1.x stream)

The version impact analysis reveals that the **2.1.x** stream is also affected:
- 2.1.0 ships quinn-proto 0.11.9 (vulnerable)
- 2.1.1 ships quinn-proto 0.11.9 (vulnerable)

Since TC-8021 is scoped to 2.2.x, the 2.1.x impact is handled as cross-stream:

1. **Post cross-stream impact comment** on TC-8021:
   > Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

2. **Check for sibling CVE Jiras** for the 2.1.x stream (search for issues with label CVE-2026-31812 and summary suffix `[rhtpa-2.1]`).

3. **If no sibling CVE Jira exists for 2.1.x**, create preemptive remediation tasks:
   - Upstream backport task for release/0.3.z with `security-preemptive` label and "Related" link to TC-8021
   - Downstream propagation task for rhtpa-release.0.3.z with `security-preemptive` label

4. **If a sibling CVE Jira exists for 2.1.x**, skip task creation for that stream -- it will be triaged through its own CVE issue. Create a "Related" link between TC-8021 and the sibling issue.

### Coordination Guidance

The affected repository (rhtpa-backend) has deployment context **upstream** (default). Remediation task Implementation Notes would include:

> This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Post-Triage Actions

1. **Add `ai-cve-triaged` label** to TC-8021
2. **Transition TC-8021 to In Progress** (if not already)
3. **Post summary comment** on TC-8021 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 replaced with RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2)
   - Remediation tasks created (upstream + downstream for 2.2.x)
   - Cross-stream impact on 2.1.x
   - @mention of the issue reporter
   - Comment Footnote for skill triage-security

## Key Findings

1. **PSIRT Affects Versions was incorrect:** RHTPA 2.0.0 does not exist in any configured stream. Corrected to RHTPA 2.2.0, 2.2.1, 2.2.2 based on lock file evidence.
2. **Partial fix already present:** The 2.2.x stream was partially fixed starting with version 2.2.3 (build v0.4.11), which bumped quinn-proto to 0.11.14. Only versions 2.2.0 through 2.2.2 require remediation.
3. **Cross-stream impact:** The 2.1.x stream is also affected (both versions ship quinn-proto 0.11.9), requiring either companion CVE triage or preemptive remediation.
4. **No concurrent triages:** No other active triages on the quinn-proto component were detected, so remediation tasks can be created without risk of duplication.
