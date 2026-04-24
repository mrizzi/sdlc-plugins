## Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

**Result: FAIL**

### Analysis

The task description specifies that `vulnerability_count` should be computed via a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

However, the actual implementation in `modules/fundamental/src/package/service/mod.rs` does not implement any subquery at all. Instead, the vulnerability count is hardcoded to zero:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly confirms that the required database query to count distinct advisories was never written. Since the count is always 0 regardless of actual data, it does not reflect unique advisories -- it reflects nothing.

The test `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2` for a package seeded with shared advisories. This test would fail at runtime because the hardcoded value is 0, not 2.

This criterion is clearly unmet.
