# Step 1 -- Data Extraction: TC-8002

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server (from labels) |
| Product version (PSIRT-claimed) | RHTPA 2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 (i.e., < 1.0.135) |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | Not available (no PR link in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | None |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x only.

However, the full triage must still check all supported streams (2.1.x and 2.2.x) for cross-stream impact analysis (Step 7, Case B).

## Ecosystem Detection

The vulnerable library is **serde_json**, a Rust crate. Based on the Ecosystem Mappings in the security matrix, this maps to the **Cargo** ecosystem:

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`
- Source repository: backend

## Step 1.5 -- External CVE Data Enrichment

External CVE databases would be queried for cross-validation (MITRE CVE API and OSV.dev). Based on the Jira description data:

| Source | Affected range | Fixed version |
|--------|---------------|---------------|
| Jira description | < 1.0.135 | 1.0.135 |
| MITRE CVE API | (would query https://cveawg.mitre.org/api/cve/CVE-2026-28940) |
| OSV.dev | (would query https://api.osv.dev/v1/vulns/CVE-2026-28940) |

**Enriched fix threshold**: >= 1.0.135 (from Jira description; external APIs not called per eval constraints).

## Additional References

- GHSA: https://github.com/advisories/GHSA-2026-j9r2-m5vk
- RustSec: https://rustsec.org/advisories/RUSTSEC-2026-0019.html
- Description: Stack overflow on deeply nested JSON input. Versions before 1.0.135 are vulnerable to unbounded recursion during deserialization. Fix introduces a configurable recursion limit defaulting to 128 levels.
