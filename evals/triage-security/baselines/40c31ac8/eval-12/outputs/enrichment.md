# Step 1.5 -- External CVE Data Enrichment

## CVE-2026-48901 (h2)

### Source 1: MITRE CVE API

URL: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

Parsed data from the CNA affected block:
- Product: h2
- Vendor: hyperium
- Affected range: versions < 0.4.8 (semver)
- Fix threshold: **0.4.8** (from `lessThan` field)

### Source 2: OSV.dev API

URL: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

Parsed data from the affected ranges:
- Package: h2 (ecosystem: crates.io)
- Alias: RUSTSEC-2026-0089
- Introduced: 0 (all versions from the start)
- Fixed: **0.4.8**

### Cross-Validation Table

| Source | Affected Range | Fixed Version |
|--------|----------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | < 0.4.8 (semver, `lessThan`) | 0.4.8 |
| OSV.dev | introduced 0 -- fixed 0.4.8 | 0.4.8 |

### Analysis

- The Jira description is **imprecise** -- it provides no specific version threshold, only "versions prior to the fix" and "see advisory."
- Both external sources **agree**: the fix threshold is **0.4.8**. All h2 versions below 0.4.8 are affected.
- MITRE CVE API provides a `lessThan: "0.4.8"` constraint with `versionType: "semver"`, meaning the affected range is `< 0.4.8`.
- OSV.dev provides an explicit `fixed: "0.4.8"` event, confirming that 0.4.8 is the first non-vulnerable version.

### Enriched Fix Threshold

**0.4.8** (cross-validated, agreement between MITRE and OSV.dev)

This enriched threshold replaces the imprecise Jira description data and will be used for all version impact comparisons in Step 2.
