# Data Extraction — TC-8005

## Parsed CVE Data

| Field | Value |
|-------|-------|
| Jira Key | TC-8005 |
| CVE ID | CVE-2026-40215 |
| Summary | openssl-libs - Buffer over-read in X.509 certificate verification |
| Issue Type | Vulnerability |
| Status | New |
| CVSS | 7.1 (High) |
| Vulnerable Package | openssl-libs |
| Affected Version Range | versions before 3.0.7-28.el9_4 |
| Fixed Version | 3.0.7-28.el9_4 |
| Ecosystem | RPM |
| Stream Scope | [rhtpa-2.2] — 2.2.x stream |
| Component Label | pscomponent:org/rhtpa-server |
| Labels | CVE-2026-40215, pscomponent:org/rhtpa-server |
| Affects Versions (current) | RHTPA 2.0.0 |
| Due Date | 2026-08-15 |
| Assignee | Unassigned |

## Ecosystem Detection

The ecosystem is **RPM** (system package), not Cargo. This is determined by:

1. **Library name**: `openssl-libs` is an RPM package name (system library), not a Cargo crate or npm package.
2. **Ecosystem Mappings** in security-matrix.md for the 2.2.x stream confirms RPM as a configured ecosystem with lock file `rpms.lock.yaml`.
3. **Lock file source**: The openssl-libs version data comes from `rpms.lock.yaml`, not `Cargo.lock`.

## Remote Links

| Type | URL |
|------|-----|
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Red Hat Security Advisory | https://access.redhat.com/errata/RHSA-2026:4021 |

## Vulnerability Description

A buffer over-read vulnerability exists in the `X509_verify_cert()` code path where the extension parser does not properly validate the length field of a Subject Alternative Name extension. A remote attacker can craft a certificate with a malformed extension that triggers an out-of-bounds read, potentially leaking sensitive memory contents or causing a crash. The fix adds bounds checking before reading extension data.
