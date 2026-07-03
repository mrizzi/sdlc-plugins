# Step 1 -- Data Extraction: TC-8040

## Extracted CVE Data

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
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

Summary suffix: `[rhtpa-2.2]`
Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)

This issue is **stream-scoped** to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library was analyzed for ecosystem classification.

- **Detected ecosystem**: Go modules
- **Ecosystem Mappings tables checked**:
  - Stream 2.1.x (`rhtpa-release.0.3.z`): Cargo, RPM
  - Stream 2.2.x (`rhtpa-release.0.4.z`): Cargo, RPM

**Result**: The detected ecosystem "Go modules" is **not listed** in any stream's Ecosystem Mappings table. The configured ecosystems are limited to Cargo and RPM. Automated triage cannot proceed for this ecosystem -- the skill does not have a configured lock file path, check command, or repository mapping for Go modules.

## Configuration Context (from CLAUDE.md)

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Jira version prefix: RHTPA
- Vulnerability issue type ID: 10024
- Product pages URL: https://access.example.com/product-life-cycle/rhtpa
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345

## Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

## Source Repositories

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |
