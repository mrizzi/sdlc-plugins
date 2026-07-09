# Step 1.5 -- External CVE Data Enrichment

## CVE-2026-48901 (h2)

### 1. MITRE CVE API Response

Source: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

Parsed structured data:

| Field | Value |
|-------|-------|
| Product | h2 |
| Vendor | hyperium |
| Affected range | lessThan 0.4.8 (semver) |
| Version type | semver |

The MITRE record provides a precise machine-readable fix threshold: versions **less than 0.4.8** are affected.

### 2. OSV.dev API Response

Source: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

Parsed structured data:

| Field | Value |
|-------|-------|
| OSV ID | RUSTSEC-2026-0089 |
| Aliases | CVE-2026-48901 |
| Package | h2 |
| Ecosystem | crates.io |
| Introduced | 0 (all versions from the beginning) |
| Fixed | 0.4.8 |

The OSV record confirms the fix threshold: versions **introduced from 0, fixed at 0.4.8**.

### 3. Cross-Validation

| Source | Affected range | Fixed version |
|--------|---------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | < 0.4.8 | 0.4.8 |
| OSV.dev | introduced 0, fixed 0.4.8 | 0.4.8 |

**Agreement**: MITRE and OSV.dev both report the same fix threshold: **0.4.8**. The Jira description is imprecise ("versions prior to the fix" / "see advisory") but does not contradict the external sources.

**Enriched fix threshold**: **0.4.8** (from MITRE and OSV.dev, in agreement)

The external data takes precedence because it provides machine-readable version constraints rather than the prose-parsed ranges from the Jira description. This enriched threshold will be used in Step 2.3 for version impact comparisons.

### Enrichment Summary

The Jira description lacked precise version thresholds. External CVE databases resolved this gap:
- MITRE CVE API: `lessThan: 0.4.8` (semver)
- OSV.dev: `fixed: 0.4.8`
- Both sources agree -- high confidence in the fix threshold

**Versions of h2 < 0.4.8 are affected. Versions >= 0.4.8 are not affected.**
