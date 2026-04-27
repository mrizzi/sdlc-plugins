## Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

**Result: FAIL**

### Analysis

The task description specifies that `vulnerability_count` should be computed via a correlated subquery using `COUNT(DISTINCT a.id)` through the join chain `sbom_package -> sbom_advisory -> advisory`:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

However, the implementation in `modules/fundamental/src/package/service/mod.rs` does not implement any subquery at all. The vulnerability count is hardcoded to zero:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The explicit `// TODO: implement subquery` comment confirms this is acknowledged missing functionality. Since no database query is performed, deduplication of advisories across SBOMs is irrelevant -- the count is always 0 regardless of the actual data state.

The test `test_vulnerability_count_deduplicates_across_sboms` seeds a package with 2 unique advisories shared across 3 SBOMs and asserts `vulnerability_count == 2`. This test would fail at runtime because the hardcoded value is 0, not 2.

Similarly, `test_package_with_vulnerabilities_has_count` expects `vulnerability_count == 3` for a package with 3 advisories, which would also fail.

This criterion is not met. The core computational logic required by the task has not been implemented.
