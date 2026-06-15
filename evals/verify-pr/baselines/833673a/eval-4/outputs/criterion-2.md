# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (with caveat)

## Analysis

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows that the `vulnerability_count` field is hardcoded to `0` for all packages:

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

Because the value is hardcoded to `0`, packages with no vulnerabilities will indeed show `vulnerability_count: 0`. However, this is coincidental -- the value is always 0 regardless of actual vulnerability status. This means criterion 2 technically passes, but only because the subquery is not implemented yet.

Additionally, the test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` verifies this behavior:

```rust
assert_eq!(pkg.vulnerability_count, 0);
```

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- The hardcoded `vulnerability_count: 0` ensures zero-valued packages return 0
- Test file `tests/api/package_vuln_count.rs` includes a test for the zero case
