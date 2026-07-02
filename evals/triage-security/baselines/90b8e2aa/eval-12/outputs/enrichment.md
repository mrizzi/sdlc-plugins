# Step 1.5 -- External CVE Data Enrichment

## CVE-2026-48901 (h2)

### MITRE CVE API Response

Source: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

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

Extracted data:
- Product: h2 (vendor: hyperium)
- Affected range: versions < 0.4.8 (semver)
- Fix threshold: **0.4.8**

### OSV.dev API Response

Source: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

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

Extracted data:
- Package: h2 (ecosystem: crates.io)
- Introduced: 0 (all versions from initial release)
- Fixed: **0.4.8**

### Cross-Validation Table

| Source | Affected Range | Fixed Version | Fix Threshold |
|--------|---------------|---------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) | Not determinable |
| MITRE CVE API | < 0.4.8 (semver) | 0.4.8 | **0.4.8** |
| OSV.dev | introduced 0, fixed 0.4.8 | 0.4.8 | **0.4.8** |

### Cross-Validation Result

**Agreement.** Both external sources (MITRE CVE API and OSV.dev) agree on the fix threshold: **0.4.8**. The Jira description was imprecise ("versions prior to the fix" / "see advisory") and did not provide a numeric threshold. The external structured data resolves this ambiguity.

**Enriched fix threshold: h2 < 0.4.8 is affected; h2 >= 0.4.8 is fixed.**

This enriched fix threshold will be used in Step 2.3 for version impact comparisons. The external data takes precedence because it provides machine-readable version constraints rather than prose-parsed ranges.
