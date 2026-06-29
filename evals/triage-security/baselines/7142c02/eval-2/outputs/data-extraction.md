# Step 1 -- Data Extraction for TC-8002

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | None |
| Issue status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains `[rhtpa-2.2]`, which maps to the **2.2.x** version stream
(Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This is a **stream-scoped** issue -- Steps 3-4 apply to the 2.2.x stream only.
However, the full version impact analysis (Step 2) covers all supported streams
(2.1.x and 2.2.x) to detect cross-stream impact.

## Ecosystem Detection

The vulnerable library is **serde_json**, a Rust crate. The ecosystem is **Cargo**.

From the security-matrix Ecosystem Mappings:
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch (2.1.x): `release/0.3.z`
- Upstream branch (2.2.x): `release/0.4.z`

## Vulnerability Description

A stack overflow vulnerability exists in serde_json versions before 1.0.135 when
deserializing deeply nested JSON input. An attacker can craft a JSON payload with
thousands of nested arrays or objects that causes unbounded recursion during
deserialization, leading to a stack overflow and process crash. The fix (1.0.135)
introduces a configurable recursion limit defaulting to 128 levels of nesting.
