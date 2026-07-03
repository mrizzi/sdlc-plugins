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
| Existing comments | (none) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the configured Version Stream **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3-4 apply only to the 2.2.x stream. Cross-stream impact on other streams (2.1.x) is handled via Case B in Step 8.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The 2.2.x stream's `security-matrix.md` Ecosystem Mappings table lists **Cargo** as a supported ecosystem with:

- **Repository**: backend
- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock`
- **Upstream Branch**: `release/0.4.z`

Ecosystem: **Cargo** (source dependency)

## Deployment Context Lookup

The component label `pscomponent:org/rhtpa-server` identifies the affected repository as **rhtpa-backend**.

Source Repositories mapping from CLAUDE.md:

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | customer-shipped |

Deployment context for rhtpa-backend: **customer-shipped**

This deployment context will be used in Step 8 (Remediation) to generate coordination guidance in remediation task descriptions. The `customer-shipped` context indicates this component is shipped to customers and requires coordination with Product Security for CVE assignment, advisory preparation, and formal disclosure.

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | cross-stream |
| 2.1.1 | 2.1.x | 0.11.9 | YES | cross-stream |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | 0.11.14 | NO | |

### Affects Versions Mismatch

PSIRT assigned **RHTPA 2.0.0** as the Affects Version, but no 2.0.x stream exists in the Version Streams configuration. Based on lock file analysis:

- **Affected within scope (2.2.x)**: 2.2.0, 2.2.1, 2.2.2
- **Not affected within scope (2.2.x)**: 2.2.3, 2.2.4 (ship quinn-proto 0.11.14, which is the fixed version)
- **Cross-stream affected (2.1.x)**: 2.1.0, 2.1.1

The Affects Versions field must be corrected to reflect the actual affected versions within the 2.2.x stream scope.
