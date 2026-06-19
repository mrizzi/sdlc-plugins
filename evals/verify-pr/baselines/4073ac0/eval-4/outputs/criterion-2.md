# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Verdict: FAIL

## Reasoning

While packages with no vulnerabilities will technically show `vulnerability_count: 0`, this is only because the implementation hardcodes the value to `0` for ALL packages, not because a proper computation returns zero for packages without vulnerabilities.

In `modules/fundamental/src/package/service/mod.rs`, the code maps every package to:

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

The `// TODO: implement subquery` comment explicitly acknowledges the subquery is not implemented. The value `0` is hardcoded regardless of whether the package has vulnerabilities or not. This means:

- A package with 5 vulnerabilities would also show `vulnerability_count: 0`
- The criterion's intent is that the count is computed correctly and happens to be zero for packages without vulnerabilities
- Since the count is never computed, this criterion is not genuinely satisfied

The test `test_package_with_vulnerabilities_has_count` expects `vulnerability_count: 3` for a package seeded with 3 advisories, but the hardcoded implementation would return 0, causing a test failure at runtime. This confirms the implementation is incomplete.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`, line with `vulnerability_count: 0, // TODO: implement subquery`
- The TODO comment is an explicit acknowledgment that the computation is missing
- Test `test_package_with_vulnerabilities_has_count` would fail at runtime (asserts `vulnerability_count == 3` but would get `0`)

## Result: FAIL
