# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The task's Implementation Notes specify that the vulnerability count should be computed using a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp 
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id 
JOIN advisory a ON sa.advisory_id = a.id 
WHERE sp.package_id = p.id
```

The `COUNT(DISTINCT a.id)` is critical for ensuring that advisories shared across multiple SBOMs are not double-counted.

However, the PR diff in `modules/fundamental/src/package/service/mod.rs` shows:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The subquery is **not implemented**. The `vulnerability_count` is hardcoded to `0` with an explicit TODO comment. There is no database query that performs the join through `sbom_package`, `sbom_advisory`, and `advisory` tables, and therefore no deduplication logic exists.

While a test exists (`test_vulnerability_count_deduplicates_across_sboms`) that would verify this behavior, the underlying implementation is absent. The test asserts `pkg.vulnerability_count == 2`, but the actual code would return `0` for all packages, meaning this test would fail at runtime.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- line contains `vulnerability_count: 0, // TODO: implement subquery`
- No correlated subquery is present in the diff
- No JOIN through `sbom_package`, `sbom_advisory`, `advisory` tables
- No `COUNT(DISTINCT ...)` logic
- The deduplication test (`test_vulnerability_count_deduplicates_across_sboms`) would fail because the hardcoded value of 0 does not match the expected value of 2
