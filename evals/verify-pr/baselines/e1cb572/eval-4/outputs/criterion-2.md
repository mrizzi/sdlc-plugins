# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Verdict: PASS (partial -- see note)

## Analysis

The diff for `modules/fundamental/src/package/service/mod.rs` shows that `vulnerability_count` is hardcoded to `0` for all packages:

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

Since every package gets `vulnerability_count: 0`, packages with no vulnerabilities will indeed show `vulnerability_count: 0`. However, this is only incidentally correct -- it is a side effect of the value being hardcoded to 0 for ALL packages, not because a correct query computes the value.

The test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` asserts `pkg.vulnerability_count == 0`, which would pass with this hardcoded implementation.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- `vulnerability_count: 0` is hardcoded with a `// TODO: implement subquery` comment
- This criterion technically passes because hardcoded 0 satisfies the zero-vulnerability case
- However, the hardcoding reveals that the implementation is incomplete (see Criterion 3)

## Note

While this criterion is technically satisfied by the current code, the satisfaction is trivial/degenerate -- the value is correct for zero-vulnerability packages only because it is hardcoded to 0 for ALL packages. The TODO comment confirms this is an incomplete implementation.
