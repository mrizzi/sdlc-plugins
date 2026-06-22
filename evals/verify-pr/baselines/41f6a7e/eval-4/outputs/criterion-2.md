# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Verdict: FAIL

## Reasoning

While packages with no vulnerabilities will technically receive `vulnerability_count: 0` from this implementation, that is only because the value is hardcoded to `0` for ALL packages regardless of whether they have vulnerabilities or not. The criterion requires that the count is correctly computed and returns zero specifically for packages without vulnerabilities.

In `modules/fundamental/src/package/service/mod.rs`, the mapping code sets:

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

The `// TODO: implement subquery` comment explicitly acknowledges that the vulnerability counting logic is not implemented. The value `0` is hardcoded for every package, including those that have associated vulnerability advisories. This means:

- A package linked to 5 advisories would incorrectly show `vulnerability_count: 0`
- The test `test_package_with_vulnerabilities_has_count` seeds a package with 3 advisories and asserts `vulnerability_count == 3`, which would fail at runtime (receiving 0)
- The zero value for vulnerability-free packages is coincidentally correct but for the wrong reason -- the count is never computed

The criterion's intent is that a real computation determines the count, which happens to be zero for packages without vulnerabilities. A hardcoded zero does not satisfy this.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- `vulnerability_count: 0, // TODO: implement subquery`
- The TODO comment is an explicit admission that the subquery is not implemented
- Test `test_package_with_vulnerabilities_has_count` would fail at runtime (asserts `vulnerability_count == 3` but gets `0`), confirming the count is not computed
