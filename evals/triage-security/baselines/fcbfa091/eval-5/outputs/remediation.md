# Step 8 -- Remediation

## PROPOSAL: Create Remediation Task for CVE-2026-40215 (2.2.x stream)

Ecosystem: RPM (system package). Per the skill's remediation template rules, RPM ecosystem produces a **single** remediation task targeting the Konflux release repo. No upstream backport task is needed because system packages are updated directly in the Konflux release repo lock files.

### Jira Issue Creation

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

A buffer over-read vulnerability in openssl-libs affects X.509 certificate chain
verification. Versions before 3.0.7-28.el9_4 are vulnerable. A remote attacker
can craft a certificate with a malformed Subject Alternative Name extension to
trigger an out-of-bounds read.

Affected versions: RHTPA 2.2.0 (3.0.7-25.el9_3), RHTPA 2.2.1 (3.0.7-27.el9_4),
RHTPA 2.2.2 (retag of 2.2.1)

Already fixed in: RHTPA 2.2.3 (3.0.7-28.el9_4), RHTPA 2.2.4 (3.0.7-28.el9_4)

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

Note: The fix was already picked up in build 0.4.11 (version 2.2.3, released
2026-03-23) as part of a routine RPM update. Versions 2.2.3 and 2.2.4 already
ship openssl-libs 3.0.7-28.el9_4. This task tracks formal verification and
ensures no regression in future builds.

## Implementation Notes

- Verify that rpms.lock.yaml pins openssl-libs >= 3.0.7-28.el9_4 on the
  current main branch
- If the current pinned version has regressed below 3.0.7-28.el9_4, update the
  package spec in rpms.in.yaml and regenerate rpms.lock.yaml
- Confirm via rpms.lock.yaml that openssl-libs 3.0.7-28.el9_4 (or later) is
  the resolved version

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)

---

### Linkage

After task creation:

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: "<task-key>",
  type: "Depend"
)
```

### Cross-Stream Impact (Case B)

The 2.1.x stream is also affected (openssl-libs 3.0.7-24.el9 in both 2.1.0 and
2.1.1). A cross-stream impact comment would be posted on TC-8005 noting that
stream 2.1.x is also affected. If no companion CVE Jira exists for the 2.1.x
stream, a preemptive remediation task (with `security-preemptive` label and
"Related" link type) would be created for that stream.
