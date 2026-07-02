# Step 8 -- Remediation

## Triage Outcome

**Case A (Affected)**: Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship a vulnerable openssl-libs (before 3.0.7-28.el9_4). However, the fix is already present in versions 2.2.3 and 2.2.4 (the latest releases in this stream). No new code change is required for the 2.2.x stream -- the vulnerability was remediated in build 0.4.11.

**Case B (Cross-stream impact)**: The 2.1.x stream is also affected -- all versions (2.1.0, 2.1.1) ship openssl-libs 3.0.7-24.el9, which is before the fix threshold. A preemptive remediation task would be created for the 2.1.x stream if no companion CVE Jira exists for that stream.

## Remediation Task -- 2.2.x Stream (Scoped)

Since the fix is already present in RHTPA 2.2.3+ (openssl-libs 3.0.7-28.el9_4), no new remediation task is required for the 2.2.x stream. The Affects Versions are set for advisory tracking purposes only.

## Remediation Task -- 2.1.x Stream (Preemptive, Case B)

The following preemptive remediation task would be created for the 2.1.x stream, which has no companion CVE Jira for CVE-2026-40215. This is a system package (RPM) task with explicit install origin.

---

### Task Summary

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.1.x)

### Labels

ai-generated-jira, Security, CVE-2026-40215, security-preemptive

### Task Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8005 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability in openssl-libs (versions before 3.0.7-28.el9_4)
allows a remote attacker to craft a certificate with a malformed Subject Alternative
Name extension that triggers an out-of-bounds read during X.509 certificate chain
verification. This can leak sensitive memory contents or cause a crash.

Affected versions in 2.1.x stream:
- RHTPA 2.1.0 (build 0.3.8, tag v0.3.8): openssl-libs 3.0.7-24.el9
- RHTPA 2.1.1 (build 0.3.12, tag v0.3.12): openssl-libs 3.0.7-24.el9

CVSS: 7.1 (High)
Advisory: RHSA-2026:4021 (https://access.redhat.com/errata/RHSA-2026:4021)
CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Update the openssl-libs package version in rpms.in.yaml (or equivalent package spec) to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to lock the updated version
- The fix is available via Red Hat advisory RHSA-2026:4021
- Verify the updated package is available in the configured RPM repositories

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated openssl-libs

## Dependencies

- Depends on: TC-8005 (parent tracking issue, linked via "Related")

---

### Jira Link Type

Link to originating CVE Jira (TC-8005) with **Related** (not "Depend"), because this is a preemptive task from a cross-stream analysis and the originating CVE belongs to the 2.2.x stream.
