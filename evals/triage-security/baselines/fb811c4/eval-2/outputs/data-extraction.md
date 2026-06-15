# Step 1: Data Extraction - TC-8002

## CVE Information

- **CVE ID**: CVE-2026-28940
- **Summary**: serde_json - Stack overflow on deeply nested input [rhtpa-2.2]
- **GHSA**: GHSA-2026-j9r2-m5vk

## Affected Component

- **Vulnerable library**: serde_json
- **Ecosystem**: Cargo (Rust crate)
- **Affected version range**: versions before 1.0.135 (< 1.0.135)
- **Fixed version**: 1.0.135
- **CVSS**: 5.3 (Medium)

## Vulnerability Details

A stack overflow vulnerability exists in serde_json versions prior to 1.0.135. When deserializing deeply nested JSON input, an attacker can craft a JSON payload with thousands of nested arrays or objects that causes unbounded recursion during deserialization, leading to a stack overflow and process crash. The fix introduces a configurable recursion limit that defaults to 128 levels of nesting.

## Issue Metadata

- **Jira Key**: TC-8002
- **Issue Type**: Vulnerability
- **Status**: New
- **Labels**: CVE-2026-28940, pscomponent:org/rhtpa-server
- **Affects Versions**: RHTPA 2.2.0
- **Due Date**: 2026-07-30
- **Assignee**: Unassigned

## Stream Scope

- **Stream tag**: [rhtpa-2.2]
- **Scoped stream**: 2.2.x (Konflux release repo: rhtpa-release.0.4.z)

## Component Mapping

- **Component label**: pscomponent:org/rhtpa-server
- **Source repository**: rhtpa-backend
- **Lock file**: Cargo.lock
- **Check command**: `git show <tag>:Cargo.lock`
- **Upstream branch**: release/0.4.z

## References

- https://github.com/advisories/GHSA-2026-j9r2-m5vk
- https://www.cve.org/CVERecord?id=CVE-2026-28940
- https://rustsec.org/advisories/RUSTSEC-2026-0019.html
