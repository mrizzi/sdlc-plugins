# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | 2.2.x (mapped from suffix `[rhtpa-2.2]` to Version Streams table entry `2.2.x`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Ecosystem | RPM (system package) |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| Due date | 2026-08-15 |
| Existing comments | (none) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** stream in the Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `openssl-libs` is an RPM system package. The 2.2.x stream's Ecosystem Mappings table shows:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

Investigation method: rpms.lock.yaml inspection (lock file configured for RPM ecosystem), supplemented by SBOM verification via cosign.

## Vulnerability Description

A buffer over-read vulnerability in openssl-libs during X.509 certificate chain verification. The `X509_verify_cert()` code path fails to properly validate the length field of a Subject Alternative Name extension. A remote attacker can craft a certificate with a malformed extension to trigger an out-of-bounds read, potentially leaking sensitive memory contents or causing a crash.
