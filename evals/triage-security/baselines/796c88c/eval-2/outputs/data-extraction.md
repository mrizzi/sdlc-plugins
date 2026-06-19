# Data Extraction: TC-8002

## CVE Information

- **CVE ID**: CVE-2026-28940
- **Advisory**: GHSA-2026-j9r2-m5vk
- **Summary**: Stack overflow on deeply nested input in serde_json
- **CVSS**: 5.3 (Medium)

## Affected Package

- **Library**: serde_json
- **Ecosystem**: Cargo (Rust)
- **Affected versions**: < 1.0.135
- **Fixed version**: 1.0.135

## Issue Metadata

- **Jira Key**: TC-8002
- **Issue Type**: Vulnerability
- **Status**: New
- **Labels**: CVE-2026-28940, pscomponent:org/rhtpa-server
- **Affects Versions**: RHTPA 2.2.0
- **Stream Scope**: 2.2.x (from `[rhtpa-2.2]` suffix in summary)
- **Due Date**: 2026-07-30
- **Assignee**: Unassigned

## Ecosystem Detection

- **Ecosystem**: Cargo
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Source repository**: rhtpa-backend (backend component)

## Version Streams to Check

Per the Security Configuration, two version streams are configured:

| Stream | Konflux Release Repo |
|--------|----------------------|
| 2.1.x | rhtpa-release.0.3.z |
| 2.2.x | rhtpa-release.0.4.z |

All versions across all supported streams must be checked.
