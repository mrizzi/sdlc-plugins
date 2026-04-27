# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (partial -- see caveat)

## Analysis

The acceptance criterion requires that packages with no known vulnerabilities should show `vulnerability_count: 0`.

### Evidence from Service Layer

In the PR diff for `modules/fundamental/src/package/service/mod.rs`, the service maps all packages to a hardcoded value:

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

This means **all** packages currently return `vulnerability_count: 0`, not just packages with no vulnerabilities. While this technically satisfies the criterion for the zero-vulnerability case, it is a side effect of the implementation being incomplete -- the count is hardcoded to 0 for every package, regardless of actual vulnerability status.

### Evidence from Tests

The test file `tests/api/package_vuln_count.rs` includes a test that verifies this behavior:

```rust
async fn test_package_without_vulnerabilities_has_zero_count(ctx: &TestContext) {
    let pkg_id = ctx.seed_package("pkg-safe", "MIT").await;
    // ...
    assert_eq!(pkg.vulnerability_count, 0);
}
```

This test would pass with the current hardcoded implementation, but it does not validate that the zero is computed correctly via the subquery -- it merely asserts the hardcoded value.

### Caveat

The hardcoded `vulnerability_count: 0` means this criterion is trivially satisfied, but only because the actual subquery logic has not been implemented (see `// TODO: implement subquery`). This is directly relevant to Criterion 3, which requires correct counting.

### Conclusion

Packages with no vulnerabilities do show `vulnerability_count: 0`. However, this is achieved via hardcoding rather than computed logic. The criterion is technically met as stated, but the implementation is incomplete. The incompleteness is more precisely captured by Criterion 3's failure.
