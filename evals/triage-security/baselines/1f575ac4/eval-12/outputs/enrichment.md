# Step 1.5 -- External CVE Data Enrichment: CVE-2026-48901

## MITRE CVE API Response

Source: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

Parsed fields:
- **Product**: h2 (vendor: hyperium)
- **Affected range**: versions less than 0.4.8 (semver)
- **Fix threshold**: `lessThan: 0.4.8` -- versions < 0.4.8 are affected
- **Version type**: semver

Raw data:
```json
{
  "cveMetadata": {"cveId": "CVE-2026-48901"},
  "containers": {
    "cna": {
      "affected": [{
        "product": "h2",
        "vendor": "hyperium",
        "versions": [{
          "status": "affected",
          "lessThan": "0.4.8",
          "versionType": "semver"
        }]
      }]
    }
  }
}
```

## OSV.dev API Response

Source: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

Parsed fields:
- **Package**: h2 (ecosystem: crates.io)
- **Introduced**: 0 (all versions from the start)
- **Fixed**: 0.4.8
- **Alias**: RUSTSEC-2026-0089

Raw data:
```json
{
  "id": "RUSTSEC-2026-0089",
  "aliases": ["CVE-2026-48901"],
  "affected": [{
    "package": {"ecosystem": "crates.io", "name": "h2"},
    "ranges": [{
      "type": "SEMVER",
      "events": [
        {"introduced": "0"},
        {"fixed": "0.4.8"}
      ]
    }]
  }]
}
```

## Cross-Validation Table

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | < 0.4.8 (semver) | 0.4.8 |
| OSV.dev | introduced at 0, fixed at 0.4.8 | 0.4.8 |

## Analysis

- **MITRE and OSV.dev agree**: the fix threshold is **0.4.8**. All h2 versions below 0.4.8 are affected; versions >= 0.4.8 are not affected.
- **Jira description is imprecise**: it states "versions prior to the fix" and "see advisory" without providing a numeric version threshold. The external sources resolve this ambiguity.
- **Agreement**: both external sources agree on the fix threshold. The structured external data is used as the authoritative fix threshold for Step 2.3 comparisons, per the enrichment protocol (external data takes precedence over prose-parsed ranges).

## Enriched Fix Threshold

**Fix threshold for version impact analysis: h2 < 0.4.8 is affected; h2 >= 0.4.8 is not affected.**

This enriched threshold replaces the imprecise Jira description data and will be used in Step 2.3 for lock file version comparisons.
