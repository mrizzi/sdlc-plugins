# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains `[rhtpa-2.2]`. Mapping to configured Version Streams:

- `rhtpa-2.2` maps to stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)

Issue stream scope: **2.2.x** (scoped -- Steps 3-8 apply to this stream; cross-stream impact is reported via Case B)

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. This maps to the **Cargo** ecosystem, which is configured in both streams' Ecosystem Mappings tables with:

- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z` (2.2.x stream), `release/0.3.z` (2.1.x stream)

Ecosystem: **Cargo** (source dependency -- remediation produces 2 tasks: upstream backport + downstream propagation)

## Deployment Context Lookup

Affected component from label: `pscomponent:org/rhtpa-server`

Source Repositories table lookup:

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |

The Source Repositories table does not include a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`.

**Deployment context**: `upstream` (default -- Deployment Context column absent from Source Repositories table)
