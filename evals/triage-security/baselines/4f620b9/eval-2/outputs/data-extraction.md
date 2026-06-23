# Step 1 -- Data Extraction: TC-8002

## Extracted Fields

| Field | Value |
|-------|-------|
| **CVE ID** | CVE-2026-28940 |
| **Affected component** | `pscomponent:org/rhtpa-server` |
| **Product version (PSIRT-claimed)** | `[rhtpa-2.2]` -- maps to stream **2.2.x** |
| **Affects Versions (Jira field)** | RHTPA 2.2.0 |
| **Vulnerable library** | serde_json |
| **Affected version range** | versions before 1.0.135 |
| **Fixed version** | 1.0.135 |
| **CVSS** | 5.3 (Medium) |
| **Upstream fix PR** | (none listed in remote links) |
| **Advisory URL** | [GHSA-2026-j9r2-m5vk](https://github.com/advisories/GHSA-2026-j9r2-m5vk) |
| **CVE record URL** | [CVE-2026-28940](https://www.cve.org/CVERecord?id=CVE-2026-28940) |
| **Due date** | 2026-07-30 |
| **Existing comments** | (none) |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the configured **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. However, per the triage-security methodology, all supported streams are analyzed for version impact (Step 2) to detect cross-stream effects.

## Ecosystem Detection

The vulnerable library `serde_json` is a Rust crate. Based on the Ecosystem Mappings in the security matrix, this falls under the **Cargo** ecosystem.

- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Source repository**: rhtpa-backend (`release/0.3.z` for 2.1.x, `release/0.4.z` for 2.2.x)

## Vulnerability Summary

serde_json versions before 1.0.135 are vulnerable to a stack overflow when deserializing deeply nested JSON input. An attacker can craft a JSON payload with thousands of nested arrays or objects causing unbounded recursion during deserialization, leading to a stack overflow and process crash. The fix (1.0.135) introduces a configurable recursion limit defaulting to 128 levels of nesting.
