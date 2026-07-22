# Step 1.5 -- External CVE Data Enrichment

## CVE-2026-48901 (h2)

### 1. MITRE CVE API Response

Source: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

Parsed structured data:

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Product | h2 |
| Vendor | hyperium |
| Affected range | lessThan 0.4.8 (semver) |
| Version type | semver |

The MITRE CVE record provides a machine-readable `lessThan` constraint:
versions **< 0.4.8** are affected. This means version 0.4.8 is the fix version.

### 2. OSV.dev API Response

Source: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

Parsed structured data:

| Field | Value |
|-------|-------|
| OSV ID | RUSTSEC-2026-0089 |
| Aliases | CVE-2026-48901 |
| Package | h2 |
| Ecosystem | crates.io |
| Introduced | 0 (all versions from initial release) |
| Fixed | 0.4.8 |
| Range type | SEMVER |

The OSV.dev record confirms: all versions from 0 up to (but not including) **0.4.8**
are affected. Version 0.4.8 is the fix.

### 3. Cross-Validation

Fix threshold comparison for CVE-2026-48901 (h2):

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | < 0.4.8 | 0.4.8 |
| OSV.dev | introduced 0, fixed 0.4.8 | 0.4.8 |

**Assessment**: The Jira description is imprecise -- it says "versions prior to the fix"
and "see advisory" without providing a specific version threshold. Both external sources
(MITRE CVE API and OSV.dev) **agree** on the fix threshold: versions < 0.4.8 are
affected, and 0.4.8 is the fix version.

Since the Jira description does not contradict the external data (it is merely imprecise),
and both external sources agree, the external structured data is used as the
authoritative fix threshold.

### Enriched Fix Threshold

| Parameter | Value |
|-----------|-------|
| Affected range | < 0.4.8 |
| Fix version | 0.4.8 |
| Confidence | High (two independent external sources agree) |
| Source precedence | MITRE CVE API + OSV.dev (structured, machine-readable) over Jira description (prose, imprecise) |

This enriched fix threshold (< 0.4.8) will be used in Step 2.3 for version impact
comparisons instead of the imprecise Jira description data.
