# Step 1 -- Data Extraction: TC-8011

## Extracted Fields

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | versions before 5.98.0 |
| Fixed version | 5.98.0 |
| CVSS | 7.8 (High) |
| Upstream fix PR | Not provided in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 |
| Existing comments | None |
| Assignee | Unassigned |
| Status | New |

## Custom Fields

| Custom Field | Value |
|---|---|
| customfield_10632 (Upstream Affected Component) | webpack |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Library: webpack
- Ecosystem: **npm** (webpack is a JavaScript/TypeScript build tool)
- Lock file: `package-lock.json` (per npm ecosystem convention)
- This is a source dependency ecosystem, so remediation would require two tasks (upstream backport + downstream propagation)

## Remote Links

- [GHSA-2026-wk55-m3rr](https://github.com/advisories/GHSA-2026-wk55-m3rr) -- GitHub Advisory
- [CVE-2026-45678](https://www.cve.org/CVERecord?id=CVE-2026-45678) -- CVE Record

## Issue Links

No existing issue links on TC-8011.

## Step 1.5 -- External CVE Data Enrichment

(Simulated -- external APIs not called per eval instructions)

The Jira description states:
- Affected versions: before 5.98.0
- Fixed version: 5.98.0

Cross-validation: Using the Jira description fix threshold of **5.98.0** as the authoritative fix threshold for version impact analysis, since external APIs were not queried.
