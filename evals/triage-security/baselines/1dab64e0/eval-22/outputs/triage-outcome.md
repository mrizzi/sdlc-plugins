# Triage Outcome for TC-8021 (CVE-2026-31812 / quinn-proto)

## Triage Decision: Case A + Case B (Affected -- create remediation tasks with cross-stream impact)

### Rationale

The version impact analysis shows that within the issue's scoped stream (2.2.x), three versions are affected:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO (fixed) |
| 2.2.4 | 0.11.14 | NO (fixed) |

Since supported versions within the scoped stream ARE affected (2.2.0, 2.2.1, 2.2.2), this is **Case A** -- remediation tasks must be created.

Additionally, the 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14). Since this issue is scoped to 2.2.x, the 2.1.x impact triggers **Case B** -- a cross-stream impact comment should be posted, and if no sibling CVE Jira exists for 2.1.x, preemptive remediation tasks should be created.

### Step 7 -- Concurrent Triage Detection

No concurrent triages detected for upstream component `quinn-proto`. Proceeding with remediation task creation.

### Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Version `RHTPA 2.0.0` is incorrect:
- There is no 2.0.x version stream in the configuration.
- Correct scoped Affects Versions (for 2.2.x stream): `RHTPA 2.2.0`, `RHTPA 2.2.1`, `RHTPA 2.2.2`
- Versions 2.2.3 and 2.2.4 are NOT affected (they ship quinn-proto 0.11.14, which meets the fix threshold).

Proposed correction: `[RHTPA 2.0.0]` -> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

### Remediation Tasks (Step 8, Case A)

Since quinn-proto is a Cargo (source dependency) ecosystem, **two tasks** are required per affected stream:

#### Task 1: Upstream Backport (2.2.x stream)
- **Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)
- **Repository**: rhtpa-backend
- **Target Branch**: release/0.4.z
- **Labels**: ai-generated-jira, Security, CVE-2026-31812
- **Description**: Update quinn-proto dependency to >= 0.11.14 in Cargo.lock. The upstream fix is available at https://github.com/quinn-rs/quinn/pull/2048.
- **Link**: Depend -> TC-8021 (Vulnerability issue)

#### Task 2: Downstream Propagation (2.2.x stream)
- **Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)
- **Repository**: rhtpa-release.0.4.z
- **Target Branch**: main
- **Labels**: ai-generated-jira, Security, CVE-2026-31812
- **Description**: Update rhtpa-backend source reference in the Konflux release repo to pick up the quinn-proto fix. Source pinning method: artifacts.lock.yaml (download URL contains tag).
- **Link**: Blocked by upstream backport task; Depend -> TC-8021

### Cross-Stream Impact (Step 8, Case B)

The 2.1.x stream is also affected:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

Actions:
1. Post a cross-stream impact comment on TC-8021:
   > Cross-stream impact: quinn-proto (versions before 0.11.14) also affects stream 2.1.x based on lock file analysis. This stream is tracked by a companion issue (see Related links) or may require separate PSIRT triage.

2. Search for sibling CVE Jiras with label CVE-2026-31812 scoped to 2.1.x. If no sibling exists, create preemptive remediation tasks for the 2.1.x stream with the `security-preemptive` label and "Related" link type to TC-8021.

### Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8021
2. Post summary comment on TC-8021 with:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, 2.2.1, 2.2.2)
   - Remediation tasks created (upstream backport + downstream propagation for 2.2.x)
   - Cross-stream impact notice (2.1.x also affected)
   - @mention of the issue reporter
3. Transition TC-8021 to In Progress

### Key Finding: Already Fixed in Latest Versions

Versions 2.2.3 (build v0.4.11) and 2.2.4 (build v0.4.12) already ship quinn-proto 0.11.14, which is the fixed version. The vulnerability was resolved in those builds before this CVE triage. Remediation only needs to cover versions 2.2.0 through 2.2.2, which will be addressed by the upstream backport task targeting the release/0.4.z branch.
