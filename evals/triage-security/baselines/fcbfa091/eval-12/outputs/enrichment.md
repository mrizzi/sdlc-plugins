# Step 1.5 -- External CVE Data Enrichment

## Context

The Jira description for TC-8030 provides only imprecise version data:
- **Affected range**: "versions prior to the fix" (no semver constraint)
- **Fixed version**: "see advisory" (no version number)

External CVE databases are queried to obtain structured, machine-readable version constraints.

## 1. MITRE CVE API

**Query**: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

**Response** (parsed):

| Field | Value |
|-------|-------|
| Product | h2 |
| Vendor | hyperium |
| Affected range | lessThan 0.4.8 (semver) |
| Version type | semver |

The MITRE CVE record provides a structured `lessThan` constraint: versions **strictly less than 0.4.8** are affected. This means 0.4.8 is the fix version.

## 2. OSV.dev API

**Query**: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

**Response** (parsed):

| Field | Value |
|-------|-------|
| ID | RUSTSEC-2026-0089 |
| Aliases | CVE-2026-48901 |
| Package | h2 |
| Ecosystem | crates.io |
| Introduced | 0 (all versions from inception) |
| Fixed | 0.4.8 |

The OSV.dev record confirms that all versions of h2 prior to 0.4.8 are affected, and version 0.4.8 is the fix.

## 3. Cross-Validation

| Source | Affected range | Fixed version | Precision |
|--------|---------------|---------------|-----------|
| Jira description | "versions prior to the fix" | "see advisory" | IMPRECISE -- no machine-readable constraint |
| MITRE CVE API | < 0.4.8 (semver) | 0.4.8 | PRECISE -- structured lessThan field |
| OSV.dev | introduced 0, fixed 0.4.8 | 0.4.8 | PRECISE -- structured semver range |

**Result: Agreement.** Both external sources agree on the fix threshold:
- MITRE: `lessThan 0.4.8` (semver)
- OSV.dev: `fixed 0.4.8`

The Jira description was imprecise but does not contradict the external data -- it simply lacked specificity. No engineer intervention is needed.

## Enriched Fix Threshold

**Fix threshold for Step 2.3**: `< 0.4.8` (h2 versions strictly less than 0.4.8 are affected)

This enriched threshold replaces the imprecise Jira description data for all downstream version impact comparisons. The external data takes precedence because it provides machine-readable version constraints rather than prose-parsed ranges.
