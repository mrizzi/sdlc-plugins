# Step 8 -- Remediation

## Triage Outcome Determination

### 2.2.x stream (scoped)

Versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable openssl-libs. However, versions
2.2.3 and 2.2.4 already ship the fixed version (3.0.7-28.el9_4). The fix was
picked up in build 0.4.11 (released 2026-03-23). The latest released version
(2.2.4) is not affected.

**Outcome for 2.2.x**: The vulnerability is already remediated in the current
releases (2.2.3+). No new remediation task is required for this stream. Affected
versions (2.2.0-2.2.2) are recorded in Affects Versions for CVE tracking purposes.
Customers on 2.2.0-2.2.2 should upgrade to 2.2.3 or later.

### 2.1.x stream (cross-stream -- Case B)

All versions in the 2.1.x stream (2.1.0, 2.1.1) ship openssl-libs 3.0.7-24.el9,
which is vulnerable. No version in the 2.1.x stream has the fix. This triggers
Case B: cross-stream impact with proactive remediation.

**Cross-stream impact comment** (posted to TC-8005):

```
Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also affects
stream 2.1.x based on rpms.lock.yaml analysis. This stream is tracked by a
companion issue (see Related links) or may require separate PSIRT triage.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <task-key> (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive label.
When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link
them and remove the label.
```

## Preemptive Remediation Task -- 2.1.x stream

Since openssl-libs is an RPM system package present in rpms.lock.yaml (explicit
install), one task is created for the Konflux release repo.

### Jira issue creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.1)",
  description: <task-description-below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215", "security-preemptive"]
)
```

Link type: "Related" (preemptive -- originating CVE TC-8005 belongs to a different stream).

### Task description

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8005 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability was found in openssl-libs during X.509 certificate
chain verification. Versions before 3.0.7-28.el9_4 are vulnerable. A remote
attacker can craft a certificate with a malformed Subject Alternative Name extension
that triggers an out-of-bounds read, potentially leaking memory contents or causing
a crash. CVSS: 7.1 (High).

Affected versions in the 2.1.x stream:
- 2.1.0 (build v0.3.8): openssl-libs 3.0.7-24.el9
- 2.1.1 (build v0.3.12): openssl-libs 3.0.7-24.el9

Fixed version: openssl-libs 3.0.7-28.el9_4
Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Update openssl-libs to >= 3.0.7-28.el9_4 in rpms.lock.yaml (and rpms.in.yaml
  if applicable)
- The package is an explicit install in rpms.lock.yaml (not inherited from the
  base image)
- Regenerate the lock file after updating the package spec
- Verify the Konflux build pipeline triggers successfully with the updated package

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image
- [ ] No other package conflicts introduced

## Test Requirements

- [ ] Container image builds successfully with the updated openssl-libs

## Dependencies

- Depends on: TC-8005 (parent Vulnerability tracking issue)
```
