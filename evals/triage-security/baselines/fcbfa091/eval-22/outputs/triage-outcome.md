# Triage Outcome for TC-8021

## Summary

CVE-2026-31812 affects quinn-proto versions before 0.11.14. The issue is scoped to stream 2.2.x via the `[rhtpa-2.2]` suffix. Lock file analysis shows that product versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable versions of quinn-proto (0.11.9 and 0.11.12), while versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14). Cross-stream analysis reveals that the 2.1.x stream is also affected.

## Step 7 -- Concurrent Triage Detection

No concurrent triages detected for upstream component `quinn-proto`. The JQL search returned zero results. Proceeding silently to Case A/B/C branching without presenting any warning or options to the user.

## Triage Decision: Case A + Case B

### Case A -- Affected (scoped stream 2.2.x)

The issue's scoped stream (2.2.x) has affected versions: 2.2.0, 2.2.1, and 2.2.2. This triggers Case A -- create remediation tasks.

Since quinn-proto is a **Cargo** (source dependency) ecosystem package, two remediation tasks would be created:

1. **Upstream backport task** -- Update quinn-proto from the vulnerable version to >= 0.11.14 in the `rhtpa-backend` source repository on the `release/0.4.z` branch. The upstream fix PR is quinn-rs/quinn#2048.

2. **Downstream propagation subtask** -- After the upstream fix lands, update the source pinning in the `rhtpa-release.0.4.z` Konflux release repo (`artifacts.lock.yaml`) to reference a backend tag that includes the quinn-proto bump. This subtask is blocked by the upstream task.

Both tasks would be linked to TC-8021 with "Depend" link type.

### Case B -- Cross-stream impact (2.1.x)

The version impact analysis reveals that the **2.1.x stream** (outside this issue's scope) is also affected:
- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

Actions for Case B:
1. Post a cross-stream impact comment on TC-8021 noting that stream 2.1.x is also affected.
2. Search for sibling Vulnerability issues with the CVE-2026-31812 label and a `[rhtpa-2.1]` stream suffix.
3. If no sibling CVE Jira exists for 2.1.x, create preemptive remediation tasks with the `security-preemptive` label, linked to TC-8021 with "Related" link type.
4. If a sibling CVE Jira already exists for 2.1.x, skip preemptive task creation for that stream (it will be handled through its own triage).

### Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) is incorrect. There is no 2.0.x stream in the configuration. Based on lock file evidence, the corrected Affects Versions for the 2.2.x scoped stream should be:

- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14, which is the fixed version.

### Versions NOT Affected

Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14, which is at or above the fix threshold. These versions are not vulnerable and are excluded from Affects Versions and remediation scope.
