# Step 8 -- Remediation

## Triage Outcome

**Case A: Affected -- create remediation task**

The 2.2.x stream (issue scope) has affected versions: 2.2.0, 2.2.1, 2.2.2.

**Case B: Cross-stream impact**

The 2.1.x stream is also affected (all versions: 2.1.0, 2.1.1 ship openssl-libs 3.0.7-24.el9, which is below the fix threshold). Since the issue is scoped to 2.2.x and no sibling CVE Jira exists for the 2.1.x stream (would be checked via JQL in live triage), a preemptive remediation task would be created for the 2.1.x stream.

## Remediation Task -- 2.2.x Stream (Primary)

**Ecosystem:** RPM (system package) -- single task, no upstream backport needed.

**Origin:** explicit install (openssl-libs present in rpms.lock.yaml)

### Jira Issue Creation (would execute)

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)",
  description: <see task description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability in openssl-libs during X.509 certificate chain verification allows a remote attacker to craft a certificate with a malformed Subject Alternative Name extension that triggers an out-of-bounds read, potentially leaking sensitive memory contents or causing a crash. CVSS: 7.1 (High).

Affected versions in the 2.2.x stream:
- 2.2.0 (build 0.4.5): openssl-libs 3.0.7-25.el9_3
- 2.2.1 (build 0.4.8): openssl-libs 3.0.7-27.el9_4
- 2.2.2 (build 0.4.9): retag of 2.2.1

Already fixed in:
- 2.2.3 (build 0.4.11): openssl-libs 3.0.7-28.el9_4
- 2.2.4 (build 0.4.12): openssl-libs 3.0.7-28.el9_4

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Package origin: explicit install (present in rpms.lock.yaml)
- Update the openssl-libs package spec in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml if the repo uses a lock file generation workflow
- Note: versions 2.2.3+ already ship the fixed openssl-libs. This task ensures the lock file spec is updated to prevent regression in future builds

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image
- [ ] No other package conflicts introduced

## Test Requirements

- [ ] Container image builds successfully with the updated package spec

## Dependencies

- Depends on: TC-8005 (parent tracking issue)

---

## Preemptive Remediation Task -- 2.1.x Stream (Cross-stream, Case B)

Since the 2.1.x stream is also affected and has no stream-specific CVE Jira, a preemptive task would be created.

### Jira Issue Creation (would execute)

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.1.x)",
  description: <see task description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215", "security-preemptive"]
)
```

Link type: **Related** (not Depend) to TC-8005, since this is a cross-stream preemptive task.

### Preemptive Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8005 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

Affected versions in the 2.1.x stream:
- 2.1.0 (build 0.3.8): openssl-libs 3.0.7-24.el9
- 2.1.1 (build 0.3.12): openssl-libs 3.0.7-24.el9

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Package origin: explicit install (present in rpms.lock.yaml)
- Update the openssl-libs package spec in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml if the repo uses a lock file generation workflow

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated package spec

## Dependencies

- Depends on: TC-8005 (parent tracking issue -- Related link, not Depend)
