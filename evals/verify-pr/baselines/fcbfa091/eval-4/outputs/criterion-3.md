# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

This criterion requires that `vulnerability_count` be computed by counting unique (distinct) advisories affecting each package, avoiding double-counting advisories that appear across multiple SBOMs. The implementation notes specify a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

However, the diff in `modules/fundamental/src/package/service/mod.rs` shows that the `vulnerability_count` is **hardcoded to 0**:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges that the actual count computation has not been implemented. No subquery, no join, no `COUNT(DISTINCT ...)` -- the value is simply set to zero for every package, regardless of how many advisories affect it.

This means:
- A package with 5 unique advisories would show `vulnerability_count: 0` (incorrect)
- A package with advisories shared across 3 SBOMs would show `vulnerability_count: 0` (incorrect)
- The deduplication logic does not exist because no counting logic exists at all

The test `test_vulnerability_count_deduplicates_across_sboms` seeds a package with 2 unique advisories across 3 SBOMs and expects `vulnerability_count: 2`. This test would fail because the hardcoded value is 0.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- The TODO comment proves the subquery was never implemented
- No joins to `sbom_package`, `sbom_advisory`, or `advisory` tables appear anywhere in the diff
- Test `test_vulnerability_count_deduplicates_across_sboms` expects 2 but would receive 0
- Test `test_package_with_vulnerabilities_has_count` expects 3 but would receive 0
