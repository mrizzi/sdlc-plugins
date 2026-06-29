# Step 1.5 -- External CVE Data Enrichment: CVE-2026-48901

## Rationale

The Jira description for TC-8030 provides only imprecise affected version data:
- Affected versions: "versions prior to the fix"
- Fixed version: "see advisory"

These values cannot be used for version impact comparisons. External CVE databases are queried for structured, machine-readable version constraints.

## MITRE CVE API

**Query**: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

**Response** (parsed):

| Field | Value |
|-------|-------|
| Product | h2 |
| Vendor | hyperium |
| Status | affected |
| Version constraint | lessThan 0.4.8 |
| Version type | semver |

**Interpretation**: All versions of h2 below 0.4.8 are affected. The fix threshold is **0.4.8**.

## OSV.dev API

**Query**: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

**Response** (parsed):

| Field | Value |
|-------|-------|
| OSV ID | RUSTSEC-2026-0089 |
| Ecosystem | crates.io |
| Package | h2 |
| Introduced | 0 (all versions from the beginning) |
| Fixed | 0.4.8 |

**Interpretation**: The vulnerability was introduced from the initial release and is fixed in version **0.4.8**.

## Cross-Validation Table

| Source | Affected range | Fixed version | Status |
|--------|----------------|---------------|--------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) | Imprecise -- unusable for version comparison |
| MITRE CVE API | < 0.4.8 (semver) | 0.4.8 | Precise |
| OSV.dev | introduced 0, fixed 0.4.8 | 0.4.8 | Precise |

## Cross-Validation Result

**Agreement**: Both MITRE CVE API and OSV.dev report the same fix threshold:
- MITRE: lessThan **0.4.8**
- OSV.dev: fixed **0.4.8**

The external sources agree. The Jira description data is imprecise but not contradictory -- "versions prior to the fix" is consistent with the structured data.

## Enriched Fix Threshold

**Fix threshold: 0.4.8**

All h2 versions **below 0.4.8** are affected. Versions **>= 0.4.8** are not affected.

This enriched fix threshold is used in Step 2.3 for version impact comparisons, replacing the imprecise Jira description data.
