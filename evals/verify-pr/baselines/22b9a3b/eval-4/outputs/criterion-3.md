# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The acceptance criterion requires that `vulnerability_count` reflects unique advisories only, meaning that if the same advisory is linked to a package through multiple SBOMs, it should only be counted once. The task's Implementation Notes specify a correlated subquery using `COUNT(DISTINCT a.id)` to achieve this deduplication.

### Evidence from Service Layer

In the PR diff for `modules/fundamental/src/package/service/mod.rs`:

```rust
+        let items = items.into_iter().map(|p| {
+            PackageSummary {
+                id: p.id,
+                name: p.name,
+                version: p.version,
+                license: p.license,
+                vulnerability_count: 0, // TODO: implement subquery
+            }
+        }).collect();
```

The `vulnerability_count` is hardcoded to `0` for all packages. The `// TODO: implement subquery` comment explicitly acknowledges that the required correlated subquery has not been implemented. The task's Implementation Notes specify:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery is entirely absent from the implementation.

### Evidence from Tests

The test `test_vulnerability_count_deduplicates_across_sboms` in `tests/api/package_vuln_count.rs` asserts:

```rust
async fn test_vulnerability_count_deduplicates_across_sboms(ctx: &TestContext) {
    let pkg_id = ctx.seed_package_with_shared_advisories("pkg-dedup", 2, 3).await;
    // ...
    assert_eq!(pkg.vulnerability_count, 2);
}
```

This test expects `vulnerability_count` to be `2` (representing 2 unique advisories shared across 3 SBOMs). With the hardcoded value of `0`, this test would fail at runtime.

Similarly, `test_package_with_vulnerabilities_has_count` expects `vulnerability_count` to be `3`, which would also fail against the hardcoded `0`.

### Impact

This is a critical deficiency. The core feature of this task -- computing the actual vulnerability count via a database subquery -- has not been implemented. The hardcoded zero means:
- Packages with vulnerabilities incorrectly show zero
- The deduplication logic (`COUNT(DISTINCT ...)`) does not exist because the query itself does not exist
- Two of the three test cases would fail at runtime

### Conclusion

The count does NOT reflect unique advisories. The subquery specified in the Implementation Notes has not been implemented at all. The `vulnerability_count` field is hardcoded to `0` for every package. This criterion is not satisfied.
