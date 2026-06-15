# Step 1: Data Extraction

## CVE Details

- **CVE ID**: CVE-2026-33501
- **Vulnerable library**: h2
- **Affected version range**: versions before 0.4.8 (< 0.4.8)
- **Fixed version**: 0.4.8
- **CVSS**: 7.5 (High)
- **Ecosystem**: Cargo (Rust crate — h2 is listed in the Cargo Ecosystem Mappings for both streams)

## Vulnerability Description

Memory exhaustion via CONTINUATION frames. Versions of h2 before 0.4.8 are vulnerable to memory exhaustion caused by a peer sending an excessive number of CONTINUATION frames following a HEADERS frame. The h2 library accumulates all CONTINUATION frame data without enforcing a size limit on the accumulated header block, allowing an attacker to consume unbounded memory on the server.

## Stream Scope

- **Scope**: UNSCOPED
- **Reasoning**: The issue summary is "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" — there is no stream suffix (e.g., no "(2.1.x)" or "(2.2.x)" appended). An unscoped vulnerability issue covers ALL version streams. The version impact analysis must check all streams.

## Source References

- Advisory: [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7)
- CVE Record: [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501)
- Upstream fix PR: [hyperium/h2#812](https://github.com/hyperium/h2/pull/812)

## Jira Issue Details

- **Key**: TC-8004
- **Status**: New
- **Labels**: CVE-2026-33501, pscomponent:org/rhtpa-server
- **Affects Versions** (current): RHTPA 2.1.0, RHTPA 2.2.0
- **Due Date**: 2026-08-01
- **Assignee**: Unassigned
