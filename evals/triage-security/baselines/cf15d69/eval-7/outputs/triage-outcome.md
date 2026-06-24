# Triage Outcome: TC-8006

## How Step 4.2 Handled the Pre-existing Link

### Background

TC-8006 (stream [rhtpa-2.1]) arrived with a pre-existing "Related" link to sibling TC-8001 (stream [rhtpa-2.2]). Both issues track CVE-2026-31812 for the quinn-proto library, but for different version streams. The link already existed in the issue's `issuelinks` array before triage began.

### Step 4.2 Procedure Applied

Step 4.2 of the triage-security skill requires cross-stream coordination with different-stream siblings. The first action in Step 4.2 is an **idempotent link check**: before creating a Related link, the skill inspects the current issue's `issuelinks` array (fetched in Step 1) for any existing link where:

1. `type.name` is `"Related"`
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key

### Evaluation

For TC-8006, the `issuelinks` array contained:
```
- Link ID: 1990401
  Type: Related
  Direction: outward (TC-8006 -> TC-8001)
```

This link satisfies both criteria:
- Criterion 1: type.name is "Related" -- YES
- Criterion 2: outwardIssue.key is TC-8001 -- YES

### Outcome

**The skill correctly identified the pre-existing link and skipped link creation.** No `jira.create_link()` call was made. The log message produced:

> "Related link to TC-8001 already exists -- skipping"

This is the idempotent behavior specified in Step 4.2: the skill checks for existing links before creating new ones, preventing duplicate link errors from Jira and ensuring triage can be re-run safely on the same issue without side effects.

### Remaining Step 4.2 Actions

After the link check (whether skipped or created), Step 4.2 continues with:

1. **Affects Versions overlap check**: Verified that TC-8006 (RHTPA 2.1.0) and TC-8001 (RHTPA 2.2.0, RHTPA 2.2.1) have no overlapping versions. Each issue correctly carries only versions from its own stream.

2. **Sibling landscape presentation**: The companion issue table was presented showing TC-8001 (2.2.x, In Progress) and TC-8006 (2.1.x, New).

## Overall Triage Summary

### Issue: TC-8006
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto (Cargo/Rust ecosystem)
- **Fix threshold**: 0.11.14
- **Stream scope**: 2.1.x
- **CVSS**: 7.5 (High)

### Version Impact (stream 2.1.x only)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

Both versions in the 2.1.x stream ship quinn-proto 0.11.9, which is vulnerable (below fix threshold 0.11.14).

### Affects Versions Correction (Step 3)

- Current: [RHTPA 2.1.0]
- Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]
- Reason: Lock file analysis confirms both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9, which is within the affected range (< 0.11.14). PSIRT only listed 2.1.0; 2.1.1 is also affected and should be added.

### Sibling Check (Step 4)

- Sibling TC-8001 found for stream 2.2.x (status: In Progress)
- Pre-existing Related link confirmed -- no new link created (idempotent)
- No Affects Versions overlap between TC-8006 and TC-8001
- No same-stream duplicates
- No cross-CVE overlap (fields not configured)
- No preemptive tasks found

### Triage Classification: Case A -- Affected, Create Remediation Tasks

Both versions in the 2.1.x stream are affected. Remediation is needed:

- **Ecosystem**: Cargo (source dependency) -- requires **two** remediation tasks:
  1. **Upstream backport task**: Bump quinn-proto to >= 0.11.14 on branch `release/0.3.z` in the backend repository
  2. **Downstream propagation subtask**: Update the source tag reference in rhtpa-release.0.3.z (artifacts.lock.yaml) to pick up the upstream fix. Blocked by the upstream task.

- **Cross-stream impact (Case B)**: Stream 2.2.x is also partially affected (versions 2.2.0-2.2.2), but TC-8001 already exists and is In Progress for that stream. No preemptive tasks needed for stream 2.2.x.

### Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8006
2. Post summary comment to TC-8006 documenting version impact, Affects Versions correction, and remediation task links
3. All comments include the Comment Footnote per skill requirements
