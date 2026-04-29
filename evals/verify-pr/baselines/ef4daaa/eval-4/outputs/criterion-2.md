# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (with caveat)

## Analysis

The acceptance criterion requires that packages with no vulnerabilities return `vulnerability_count: 0`.

### Evidence from PR Diff

In `modules/fundamental/src/package/service/mod.rs`, the service layer constructs `PackageSummary` with a hardcoded value:

```diff
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

The value `vulnerability_count: 0` is hardcoded for ALL packages, not just those without vulnerabilities. While this means packages with no vulnerabilities will indeed show `vulnerability_count: 0`, the implementation is incomplete -- every package will show 0 regardless of actual vulnerability count.

### Test Evidence

The test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` does assert this:

```rust
assert_eq!(pkg.vulnerability_count, 0);
```

This test would pass with the current implementation since the value is always 0. However, the test `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3`, which would FAIL with the current hardcoded implementation.

### Conclusion

Narrowly, packages with no vulnerabilities will show 0. However, this is only because ALL packages show 0 due to the incomplete implementation. The criterion is trivially satisfied but in a way that exposes a deeper problem (see criterion 3).
