# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Result: FAIL

## Analysis

The acceptance criterion requires that packages without any known vulnerabilities display `vulnerability_count: 0`.

### Evidence from PR Diff

In `modules/fundamental/src/package/service/mod.rs`, the implementation hardcodes the vulnerability count:

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

While packages with no vulnerabilities would technically show `vulnerability_count: 0`, this is only because **all** packages are hardcoded to return 0. The `// TODO: implement subquery` comment explicitly acknowledges that the actual vulnerability counting logic has not been implemented.

### Why this is a FAIL

Although the literal text of this criterion is technically satisfied (packages with no vulnerabilities do show 0), this must be evaluated in conjunction with criterion 3, which requires that the count reflects unique advisories. The implementation is a stub that does not perform any actual counting. The task's Implementation Notes specify a correlated subquery (`SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ...`), which has not been implemented.

The test `test_package_with_vulnerabilities_has_count` expects `vulnerability_count == 3` for a package with 3 advisories, but the current implementation would return 0 for that package, meaning this test would fail at runtime.

The vulnerability count computation described in the task requirements has not been implemented. The `TODO` comment in the code confirms this is intentionally incomplete.

### Conclusion

The implementation is a stub. While the literal wording of this isolated criterion might appear satisfied, the vulnerability count is not actually computed -- it is hardcoded to 0 for all packages. The required subquery logic is missing entirely. This represents an incomplete implementation that would cause test failures.
