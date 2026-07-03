# Step 1 -- Data Extraction: TC-8005

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Upstream fix PR | -- (none in remote links) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | (none) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Matched Version Streams entry: 2.2.x at `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue stream scope: **2.2.x only**

## Ecosystem Detection

- Library: openssl-libs (system RPM package)
- Ecosystem: **RPM**
- Lock File: `rpms.lock.yaml` (configured in stream 2.2.x Ecosystem Mappings)
- Check Command: `git show <tag>:rpms.lock.yaml`
- Upstream Branch: -- (not applicable for RPM ecosystem)

## Deployment Context Lookup

- Affected repository from component label: org/rhtpa-server
- Source Repositories table: Deployment Context column is **absent**
- Deployment context: omitted (backward compatibility -- no Coordination Guidance subsection will be generated)
