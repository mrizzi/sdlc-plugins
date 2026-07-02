# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Upstream fix PR | -- (none in remote links) |
| Advisory URL | [RHSA-2026:4021](https://access.redhat.com/errata/RHSA-2026:4021) |
| CVE record URL | [CVE-2026-40215](https://www.cve.org/CVERecord?id=CVE-2026-40215) |
| Due date | 2026-08-15 |
| Existing comments | (none) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local path: `/home/dev/repos/rhtpa-release.0.4.z`

This issue is **stream-scoped** to the 2.2.x stream. Steps 3 and 8 apply only to versions within this stream.

## Ecosystem Detection

- Vulnerable package: openssl-libs (system RPM package)
- Ecosystem: **RPM**
- Lock file: `rpms.lock.yaml`
- Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

RPM is listed in the Ecosystem Mappings table for both the 2.1.x and 2.2.x streams.

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: **upstream** (from Source Repositories table)
