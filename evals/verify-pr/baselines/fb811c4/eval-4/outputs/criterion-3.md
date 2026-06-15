# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

This is the critical failure. The diff in `modules/fundamental/src/package/service/mod.rs` shows:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The vulnerability count is hardcoded to `0` for every package regardless of how many advisories exist. There is:
- No subquery to the advisory tables
- No join through `sbom_package` -> `sbom_advisory` -> `advisory`
- No `COUNT(DISTINCT ...)` expression
- No deduplication logic of any kind
- An explicit `// TODO: implement subquery` comment acknowledging the feature is not implemented

The task's Implementation Notes specify using a correlated subquery: `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`. This subquery is entirely absent from the implementation.

A package with 50 known vulnerabilities would still report `vulnerability_count: 0`. The count does not reflect unique advisories because it does not reflect any advisories at all.

Furthermore, two of the three tests would fail at runtime:
- `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3` but the service always returns 0
- `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2` but the service always returns 0

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- The TODO comment explicitly states the subquery is not implemented
- Tests asserting non-zero counts would fail at runtime against this implementation
