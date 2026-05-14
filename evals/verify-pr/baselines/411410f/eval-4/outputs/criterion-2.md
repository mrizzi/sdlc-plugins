# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PARTIAL PASS (with caveat)

## Analysis

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows that the vulnerability_count is hardcoded to 0 for ALL packages:

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

While this does mean packages with no vulnerabilities will show `vulnerability_count: 0`, this is only incidentally correct. The value is hardcoded to 0 for ALL packages regardless of whether they have vulnerabilities or not. The `// TODO: implement subquery` comment confirms that the actual vulnerability count computation has not been implemented.

This criterion technically passes in isolation (packages with no vulnerabilities do show 0), but the implementation is incomplete because it shows 0 for ALL packages, including those that DO have vulnerabilities. This is directly related to criterion 3's failure.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- The vulnerability_count is hardcoded to `0` with a TODO comment
- The correlated subquery specified in the Implementation Notes has not been implemented
- Test `test_package_with_vulnerabilities_has_count` expects `vulnerability_count: 3` but the implementation would always return 0
