# Step 1 -- Data Extraction: TC-8005

## Parsed CVE Data

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
| Upstream fix PR | _(none in remote links)_ |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | _(none)_ |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)
- Triage is scoped to the 2.2.x stream only

## Ecosystem Detection

- Library: openssl-libs
- Ecosystem: **RPM** (system package)
- Lock file: `rpms.lock.yaml` (configured in 2.2.x stream Ecosystem Mappings)
- Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

## Embargo Check (Step 1.7)

No Embargo policy URL is configured in Security Configuration. Step 1.7 skipped.

## Notes

- PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, which does not correspond to any configured version stream (no 2.0.x stream exists). This will need correction in Step 3.
- The issue is scoped to stream 2.2.x per the `[rhtpa-2.2]` suffix. Cross-stream impact on 2.1.x will be noted but Affects Versions correction will only include 2.2.x versions.
