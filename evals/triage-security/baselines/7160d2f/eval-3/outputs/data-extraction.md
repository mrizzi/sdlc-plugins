# Data Extraction: TC-8003

## Issue Metadata

| Field | Value |
|---|---|
| Key | TC-8003 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Assignee | Unassigned |
| Due Date | 2026-07-15 |

## Labels

- CVE-2026-31812
- pscomponent:org/rhtpa-server

## Affects Versions

- RHTPA 2.2.0

## CVE Details

| Field | Value |
|---|---|
| CVE ID | CVE-2026-31812 |
| Affected Package | quinn-proto |
| Affected Versions | versions before 0.11.14 |
| Fixed Version | 0.11.14 |
| CVSS Score | 7.5 (High) |
| Advisory | GHSA-2026-qp73-x4mq |

## Stream Identification

| Field | Value |
|---|---|
| Stream suffix | [rhtpa-2.2] |
| Version prefix | RHTPA |
| Stream | rhtpa-2.2 |

## Vulnerability Summary

A remote attacker can cause a panic in the quinn-proto crate (before version 0.11.14) by sending a QUIC transport frame that creates an excessive number of streams. This is a denial-of-service vulnerability with a High severity CVSS score of 7.5.

## Remote Links

- [GHSA-2026-qp73-x4mq](GitHub Advisory)
- [CVE-2026-31812](CVE Record)
