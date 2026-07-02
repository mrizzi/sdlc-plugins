# Step 1 -- Data Extraction: TC-8006

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x**
- Konflux release repo: git.example.com/rhtpa/rhtpa-release.0.3.z
- Local path: /home/dev/repos/rhtpa-release.0.3.z

The issue is **stream-scoped** to 2.1.x. Steps 3 and 4 apply only to the 2.1.x stream for Affects Versions correction, while version impact analysis (Step 2) still checks all streams for cross-stream awareness.

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: rhtpa-backend (upstream branch: `release/0.3.z` for 2.1.x stream)

## Existing Issue Links

The issue has the following pre-existing links:

- **Related** (outward): TC-8001 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]) -- Link ID: 1990401

## Remote Links

- GHSA-2026-qp73-x4mq (GitHub Advisory)
- CVE-2026-31812 (CVE Record)
