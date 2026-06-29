# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Status: FAIL

## Analysis

The task description specifies that `vulnerability_count` should be computed via a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id)
FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

However, the actual diff in `modules/fundamental/src/package/service/mod.rs` shows:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The vulnerability count is hardcoded to `0` for every package. The subquery to compute the actual count from the database has NOT been implemented. The `// TODO: implement subquery` comment explicitly acknowledges this is incomplete.

This means:
- Packages with vulnerabilities will incorrectly show `vulnerability_count: 0`
- There is no deduplication logic because there is no counting logic at all
- The test `test_package_with_vulnerabilities_has_count` (which expects count = 3) would FAIL
- The test `test_vulnerability_count_deduplicates_across_sboms` (which expects count = 2) would FAIL

## Evidence

- `vulnerability_count: 0` is hardcoded in the service layer
- No subquery, no join, no COUNT expression anywhere in the diff
- The TODO comment confirms the implementation is incomplete
- Two of the three integration tests would fail at runtime

## Verdict

FAIL -- The vulnerability count is not computed at all. It is hardcoded to 0, making it impossible for the count to reflect unique advisories or any advisories. The core feature is unimplemented.
