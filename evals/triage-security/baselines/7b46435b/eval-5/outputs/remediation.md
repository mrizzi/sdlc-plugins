# Step 8 -- Remediation

## Triage Outcome: Case A + Case B

**Case A -- Affected**: Versions 2.2.0, 2.2.1, and 2.2.2 in the scoped 2.2.x
stream ship a vulnerable openssl-libs. Remediation task required.

**Case B -- Cross-stream impact**: The 2.1.x stream is also affected (2.1.0
ships 3.0.7-24.el9, 2.1.1 ships 3.0.7-24.el9 -- both before the fix threshold
3.0.7-28.el9_4). This is flagged for companion issue coordination.

## Remediation Task -- 2.2.x Stream (System Package / RPM)

Since openssl-libs is an RPM system package with an explicit install origin
(present in rpms.lock.yaml), a single remediation task is created in the
Konflux release repo. No upstream backport task is needed for RPM packages.

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)",
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

A buffer over-read vulnerability in openssl-libs allows a remote attacker to
craft a certificate with a malformed Subject Alternative Name extension that
triggers an out-of-bounds read during X.509 certificate chain verification,
potentially leaking sensitive memory contents or causing a crash.

Affected versions in the 2.2.x stream:
- 2.2.0 (v0.4.5): openssl-libs 3.0.7-25.el9_3
- 2.2.1 (v0.4.8): openssl-libs 3.0.7-27.el9_4
- 2.2.2 (v0.4.9): retag of 2.2.1

Fixed in: openssl-libs 3.0.7-28.el9_4 (already shipped in 2.2.3+)

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-40215
CVSS: 7.1 (High)
Due date: 2026-08-15

Package origin: explicit install (openssl-libs found in rpms.lock.yaml).

## Implementation Notes

- Update the openssl-libs package version in rpms.in.yaml (or equivalent
  package spec) to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to reflect the updated package version
- The fix is already available via RHSA-2026:4021; no custom patching needed
- Verify the updated package resolves from the configured RPM repositories
- Note: versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already ship the
  fixed version -- this confirms the package is available in the repo

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image
- [ ] No other package conflicts introduced by the update

## Test Requirements

- [ ] Container image builds successfully with the updated openssl-libs
- [ ] Verify the installed openssl-libs version in the built image matches
      or exceeds 3.0.7-28.el9_4

## Dependencies

- Depends on: TC-8005 (parent Vulnerability tracking issue)

---

### Linkage

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: "<remediation-task-key>",
  type: "Depend"
)
```

## Cross-Stream Impact Notice (Case B)

The 2.1.x stream is also affected by CVE-2026-40215:

| Version | Tag | openssl-libs | Affected? |
|---------|-----|-------------|-----------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES |

### Comment to post on TC-8005

```
Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also
affects stream 2.1.x based on rpms.lock.yaml analysis.

- 2.1.0 (v0.3.8): openssl-libs 3.0.7-24.el9
- 2.1.1 (v0.3.12): openssl-libs 3.0.7-24.el9

The 2.1.x stream is tracked by a companion issue (if one exists with suffix
[rhtpa-2.1]) or may require separate PSIRT triage.
```

If no companion CVE Jira exists for the 2.1.x stream, a preemptive
remediation task would be created with:
- Labels: `["ai-generated-jira", "Security", "CVE-2026-40215", "security-preemptive"]`
- Link type: "Related" (not "Depend") to TC-8005
- Summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.1)"
- Description prefix noting preemptive origin from TC-8005 (stream 2.2.x)
