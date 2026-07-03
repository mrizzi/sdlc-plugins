# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Verdict: PASS

## Analysis

The acceptance criterion requires that packages with no associated vulnerabilities display a `vulnerability_count` of `0`.

### Evidence from PR Diff

In `modules/fundamental/src/package/service/mod.rs`, the service layer constructs `PackageSummary` instances with:

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

The value is hardcoded to `0`. While this is a placeholder implementation (as indicated by the `// TODO: implement subquery` comment), it does technically satisfy this specific criterion: packages with no vulnerabilities will show `vulnerability_count: 0`.

### Test Coverage

The test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` validates this behavior:

```rust
async fn test_package_without_vulnerabilities_has_zero_count(ctx: &TestContext) {
    let pkg_id = ctx.seed_package("pkg-safe", "MIT").await;
    // ...
    assert_eq!(pkg.vulnerability_count, 0);
}
```

### Conclusion

This specific criterion is satisfied -- packages with no vulnerabilities do show `vulnerability_count: 0`. However, this is a side effect of the value being hardcoded to 0 for ALL packages, which causes criterion 3 to fail (see criterion-3.md).
