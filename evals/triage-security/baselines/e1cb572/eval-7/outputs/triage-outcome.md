# Triage Outcome for TC-8006

## How Step 4.2 Handled the Pre-Existing Link

TC-8006 arrived with a pre-existing "Related" link to sibling TC-8001 (Link ID: 1990401, outward direction). Step 4.2 of the triage-security skill defines an explicit idempotency check for cross-stream sibling linking:

1. **The skill read TC-8006's `issuelinks` array** from the Step 1 data extraction (the `jira.get_issue` response).

2. **The skill checked whether any existing link satisfies all of**:
   - `type.name` is "Related"
   - `inwardIssue.key` or `outwardIssue.key` matches the sibling key (TC-8001)

3. **A matching link was found**: the existing outward Related link to TC-8001 (Link ID: 1990401) satisfies both conditions.

4. **Link creation was skipped**. The skill logged: "Related link to TC-8001 already exists -- skipping." No duplicate link was created.

This is the idempotent behavior defined in the SKILL.md Step 4.2 specification. The skill checks for existing links before creating new ones, preventing duplicate Related links when a link already exists between the current issue and a cross-stream sibling. Whether the link was created manually, by PSIRT, or by a prior triage run, the result is the same: the skill recognizes the existing link and does not create a redundant one.

## Overall Triage Analysis

### Stream Scope

TC-8006 is scoped to the **2.1.x** stream (suffix `[rhtpa-2.1]`).

### Version Impact (Stream 2.1.x)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

All versions in the 2.1.x stream ship quinn-proto 0.11.9, which is below the fixed version 0.11.14.

### Affects Versions Correction (Step 3)

- **Current**: [RHTPA 2.1.0]
- **Proposed**: [RHTPA 2.1.0, RHTPA 2.1.1]

PSIRT set only RHTPA 2.1.0, but lock file analysis shows version 2.1.1 also ships the vulnerable quinn-proto 0.11.9. The correction would add RHTPA 2.1.1 to the Affects Versions field (pending engineer confirmation).

### Sibling Check (Step 4)

- **TC-8001** (stream 2.2.x, In Progress) is a cross-stream companion, not a duplicate.
- Pre-existing Related link confirmed -- no new link needed (idempotent skip).
- No Affects Versions overlap between TC-8006 and TC-8001.
- Step 4.3 (cross-CVE overlap) skipped -- required custom fields not configured.
- Step 4.4 (preemptive task reconciliation) -- no preemptive tasks found.

### Lifecycle and Already-Fixed Checks (Steps 5-6)

- **Step 5**: Would verify that RHTPA 2.1.0 and 2.1.1 are still within support lifecycle via the product pages URL. (Not executed -- no external calls in eval mode.)
- **Step 6**: TC-8001 (sibling) has status "In Progress", not Closed/Done. No already-fixed scenario applies.

### Remediation Recommendation (Step 7 -- Case A)

All supported versions in the 2.1.x stream are affected. This is **Case A: Affected -- create remediation tasks**.

Since quinn-proto is a **Cargo (source dependency)** ecosystem, the skill would propose creating **two tasks**:

#### Task 1: Upstream Backport

- **Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)
- **Repository**: backend
- **Target Branch**: release/0.3.z
- **Labels**: ai-generated-jira, Security, CVE-2026-31812
- **Description**: Update quinn-proto dependency to >= 0.11.14 in Cargo.lock on branch release/0.3.z
- **Link**: Depend on TC-8006

#### Task 2: Downstream Propagation

- **Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
- **Repository**: rhtpa-release.0.3.z
- **Target Branch**: main
- **Source Pinning Method**: artifacts.lock.yaml (download URL contains tag)
- **Labels**: ai-generated-jira, Security, CVE-2026-31812
- **Link**: Depend on TC-8006, Blocked by upstream task
- **Description**: Update backend source reference in rhtpa-release.0.3.z once the upstream backport merges

### Cross-Stream Impact (Step 7 -- Case B)

The 2.2.x stream is also affected (versions 2.2.0, 2.2.1, 2.2.2). However, sibling TC-8001 already exists for stream 2.2.x and is In Progress. Per Case B step 4: "For streams that already have a CVE Jira, skip task creation -- those streams will be triaged through their own CVE issue."

A cross-stream impact comment would be posted to TC-8006:

> Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream 2.2.x based on lock file analysis. This stream is tracked by companion issue TC-8001 (see Related link).

No preemptive remediation tasks are needed for the 2.2.x stream since TC-8001 already exists.

### Post-Triage Actions

1. **Add label** `ai-cve-triaged` to TC-8006
2. **Post summary comment** to TC-8006 documenting the version impact table, Affects Versions correction, sibling landscape, and remediation tasks created
3. **Transition** TC-8006 to In Progress
4. **Assign** TC-8006 to current user

All proposed actions require engineer confirmation before execution.
