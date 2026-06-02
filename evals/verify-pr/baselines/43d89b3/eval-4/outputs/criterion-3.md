# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The implementation in `modules/fundamental/src/package/service/mod.rs` hardcodes `vulnerability_count: 0` with a `// TODO: implement subquery` comment. The actual subquery to count unique advisories -- described in the Implementation Notes as `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id` -- has not been implemented.

Because no subquery exists, there is no deduplication logic. The count does not reflect unique advisories; it always returns 0 regardless of the actual advisory data.

The test `test_vulnerability_count_deduplicates_across_sboms` in `tests/api/package_vuln_count.rs` seeds a package with 2 unique advisories shared across 3 SBOMs and asserts `vulnerability_count == 2`. This test would FAIL with the current implementation since the hardcoded value is 0, not 2.

```rust
async fn test_vulnerability_count_deduplicates_across_sboms(ctx: &TestContext) {
    let pkg_id = ctx.seed_package_with_shared_advisories("pkg-dedup", 2, 3).await;
    let resp = ctx.get("/api/v2/package").await;
    let body: PaginatedResults<PackageSummary> = resp.json().await;
    let pkg = body.items.iter().find(|p| p.id == pkg_id).unwrap();
    assert_eq!(pkg.vulnerability_count, 2);
}
```

This criterion is not satisfied because the core functionality (the correlated subquery with COUNT(DISTINCT)) has not been implemented.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- `vulnerability_count: 0, // TODO: implement subquery`
- No subquery implementation exists in the diff
- Test `test_vulnerability_count_deduplicates_across_sboms` would fail (expects 2, gets 0)
- The Implementation Notes specify the subquery pattern but it was not implemented
