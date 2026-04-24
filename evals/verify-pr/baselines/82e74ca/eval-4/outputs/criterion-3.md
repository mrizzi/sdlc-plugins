# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Result: FAIL

## Analysis

The acceptance criterion requires that `vulnerability_count` reflects only unique (deduplicated) advisories, avoiding double-counting when the same advisory appears across multiple SBOMs.

### Evidence from PR Diff

In `modules/fundamental/src/package/service/mod.rs`, the vulnerability count is hardcoded:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The implementation does not include any subquery to count advisories. The task's Implementation Notes specify a correlated subquery using `COUNT(DISTINCT a.id)` to ensure deduplication:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp 
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id 
JOIN advisory a ON sa.advisory_id = a.id 
WHERE sp.package_id = p.id
```

This subquery has not been implemented at all. The `DISTINCT` keyword would be responsible for deduplication, but since no query exists, there is no deduplication logic.

### Test Evidence

The test `test_vulnerability_count_deduplicates_across_sboms` in `tests/api/package_vuln_count.rs` explicitly tests this behavior:

```rust
async fn test_vulnerability_count_deduplicates_across_sboms(ctx: &TestContext) {
    let pkg_id = ctx.seed_package_with_shared_advisories("pkg-dedup", 2, 3).await;
    // ...
    assert_eq!(pkg.vulnerability_count, 2);
}
```

This test seeds a package with 2 unique advisories shared across 3 SBOMs and expects a count of 2. With the hardcoded value of 0, this test would fail.

### Conclusion

No advisory counting or deduplication logic has been implemented. The vulnerability count is hardcoded to 0 for all packages. This criterion is not satisfied.
