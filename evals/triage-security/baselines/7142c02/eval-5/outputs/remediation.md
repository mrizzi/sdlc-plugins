# Step 7 — Remediation Task

## Triage Decision

**Case A: Affected** — versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship
a vulnerable version of openssl-libs. One remediation task is required.

**Ecosystem**: RPM (system package) — single task for Konflux release repo.
No upstream backport task needed.

**Dependency chain**: explicit install (openssl-libs present in rpms.lock.yaml).
SBOM verification was skipped because cosign is not available.

---

## Task Description

### Summary

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)

### Labels

`ai-generated-jira`, `Security`, `CVE-2026-40215`

### Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability in openssl-libs (versions before 3.0.7-28.el9_4)
allows a remote attacker to craft a certificate with a malformed Subject Alternative
Name extension that triggers an out-of-bounds read during X.509 certificate chain
verification, potentially leaking sensitive memory contents or causing a crash.
CVSS: 7.1 (High).

Affected versions in the 2.2.x stream:
- 2.2.0 ships openssl-libs 3.0.7-25.el9_3
- 2.2.1 ships openssl-libs 3.0.7-27.el9_4
- 2.2.2 ships openssl-libs 3.0.7-27.el9_4 (retag of 2.2.1)

Versions 2.2.3 and 2.2.4 already ship the fixed version (3.0.7-28.el9_4).

Advisory: https://access.redhat.com/errata/RHSA-2026:4021

## Implementation Notes

- Update the openssl-libs package version in rpms.in.yaml to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to pick up the updated package version
- Verify the Konflux build pipeline triggers successfully with the updated package

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image
- [ ] No other package conflicts introduced

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
