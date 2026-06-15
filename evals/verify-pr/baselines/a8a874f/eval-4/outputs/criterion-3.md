# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

This criterion requires that `vulnerability_count` accurately reflects the number of unique advisories affecting each package, computed via a join through `sbom_package -> sbom_advisory -> advisory` tables with `COUNT(DISTINCT a.id)` to avoid duplicates across multiple SBOMs.

The implementation in `modules/fundamental/src/package/service/mod.rs` does NOT implement this subquery. Instead, the value is hardcoded:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges that the actual computation has not been implemented. The task's Implementation Notes specify the required subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery is entirely absent from the diff. The count does not reflect unique advisories because it does not reflect anything -- it is always 0.

Furthermore, the test `test_vulnerability_count_deduplicates_across_sboms` seeds a package with shared advisories across multiple SBOMs and expects `vulnerability_count: 2`, but the hardcoded `0` would cause this test to fail at runtime. Similarly, `test_package_with_vulnerabilities_has_count` expects `vulnerability_count: 3` for a package with 3 advisories, which would also fail.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Code: `vulnerability_count: 0, // TODO: implement subquery`
- The TODO comment confirms the implementation is incomplete
- No correlated subquery joining `sbom_package`, `sbom_advisory`, and `advisory` exists in the diff
- Tests asserting non-zero counts (`assert_eq!(pkg.vulnerability_count, 3)` and `assert_eq!(pkg.vulnerability_count, 2)`) would fail at runtime with the hardcoded value
