# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (trivially -- see caveat)

## Analysis

The acceptance criterion requires that packages with no known vulnerabilities display `vulnerability_count: 0`.

### Evidence from Service Layer

In the PR diff for `modules/fundamental/src/package/service/mod.rs`, the service constructs all `PackageSummary` instances with a hardcoded value:

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

Every package, regardless of actual vulnerability status, returns `vulnerability_count: 0`. For the specific case of packages with no vulnerabilities, the returned value happens to be correct.

### Evidence from Tests

The test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` asserts:

```rust
async fn test_package_without_vulnerabilities_has_zero_count(ctx: &TestContext) {
    let pkg_id = ctx.seed_package("pkg-safe", "MIT").await;
    // ...
    assert_eq!(pkg.vulnerability_count, 0);
}
```

This test would pass with the current implementation because the value is hardcoded to 0.

### Caveat

This criterion is satisfied only because the value is hardcoded to `0` for all packages, not because a proper subquery computes the count. The `// TODO: implement subquery` comment confirms the logic is incomplete. This limitation is captured more precisely by Criterion 3's failure.

### Conclusion

Packages with no vulnerabilities do show `vulnerability_count: 0`. The criterion is technically met, though the result is a side effect of the incomplete implementation rather than correct computed behavior.
