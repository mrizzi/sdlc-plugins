# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (with caveat)

## Analysis

The service code in `modules/fundamental/src/package/service/mod.rs` maps all packages to include `vulnerability_count: 0`:

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

For packages with no vulnerabilities, the value will indeed be `0`. This criterion is technically satisfied.

However, there is a significant caveat: because the value is hardcoded to `0` for ALL packages (not computed via the specified subquery), this criterion passes only because the hardcoded default happens to match the expected value for the zero-vulnerability case. The actual computation is not implemented -- see Criterion 3 for the impact.

The test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` verifies this case:

```rust
assert_eq!(pkg.vulnerability_count, 0);
```

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Diff lines 25-33: hardcoded `vulnerability_count: 0` for all packages
- Test file: `tests/api/package_vuln_count.rs`, function `test_package_without_vulnerabilities_has_zero_count`
- The zero case is satisfied by the hardcoded value, but this is coincidental rather than the result of a correct computation
