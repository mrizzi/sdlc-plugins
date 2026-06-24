# Step 1 -- Data Extraction for TC-8021

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.1 (from summary suffix `[rhtpa-2.1]`) |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 |
| Existing comments | None |
| Assignee | Unassigned |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (matches Version Streams table row: stream 2.1.x, Konflux Release Repo `git.example.com/rhtpa/rhtpa-release.0.3.z`)
- Issue stream scope: **2.1.x only** (scoped issue -- Steps 3-7 apply only to this stream)

## Ecosystem Detection

- Vulnerable library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: backend (from Ecosystem Mappings in security-matrix.md)
- Upstream branch: `release/0.3.z`

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |

## Additional References

- https://rustsec.org/advisories/RUSTSEC-2026-0088.html

## Step 1.5 -- External CVE Data Enrichment

In this eval, external API calls (MITRE CVE API and OSV.dev) are not executed. The fix threshold from the Jira description is used as the authoritative value:

- **Fix threshold**: tokio >= 1.42.0
- **Affected range**: versions before 1.42.0

## Version Impact Analysis (Step 2)

### Stream 2.1.x (issue-scoped stream)

The security matrix for stream 2.1.x (rhtpa-release.0.3.z) shows:

| Version | Build | Build Date | backend tag |
|---------|-------|------------|-------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 |

The mock lock file data does not include tokio versions by tag. However, the CVE description states versions before 1.42.0 are affected, and the issue description confirms this stream is affected with a preemptive task already created.

Since tokio is a Cargo dependency in the backend repository and the issue explicitly states the vulnerability applies to this stream, both versions 2.1.0 and 2.1.1 are affected.

### Stream 2.2.x (cross-stream analysis)

The security matrix for stream 2.2.x (rhtpa-release.0.4.z) shows versions 2.2.0 through 2.2.4. The originating CVE Jira TC-8020 already covers this stream with suffix `[rhtpa-2.2]`.

### Version Impact Table

| Version | Stream | tokio | Affected? | Notes |
|---------|--------|-------|-----------|-------|
| 2.1.0 | 2.1.x | < 1.42.0 | YES | Issue-scoped stream |
| 2.1.1 | 2.1.x | < 1.42.0 | YES | Issue-scoped stream |
| 2.2.0 | 2.2.x | -- | -- | Covered by TC-8020 (sibling CVE Jira) |
| 2.2.1 | 2.2.x | -- | -- | Covered by TC-8020 |
| 2.2.2 | 2.2.x | -- | -- | Covered by TC-8020, retag of 2.2.1 |
| 2.2.3 | 2.2.x | -- | -- | Covered by TC-8020 |
| 2.2.4 | 2.2.x | -- | -- | Covered by TC-8020 |
