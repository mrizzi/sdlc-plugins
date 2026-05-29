# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Verdict: FAIL

## Analysis

The criterion requires that packages with no known vulnerabilities return `vulnerability_count: 0`. While the current implementation does technically return 0 for all packages, this is because the value is hardcoded rather than computed.

### Evidence from the diff

In `modules/fundamental/src/package/service/mod.rs`:

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

The `vulnerability_count` is hardcoded to `0` with a `// TODO: implement subquery` comment. This means:

1. The value `0` is returned for ALL packages, regardless of whether they have vulnerabilities or not.
2. There is no actual query to determine whether a package has vulnerabilities.
3. The `TODO` comment explicitly acknowledges the implementation is incomplete.

While one might argue this criterion is technically satisfied (packages with no vulnerabilities DO show 0), the implementation is a stub that returns 0 for everything. The criterion implicitly requires that the value be computed correctly -- a hardcoded 0 that coincidentally satisfies this one criterion while breaking criterion 3 (correct count for packages WITH vulnerabilities) does not represent a genuine implementation. The task description explicitly requires a correlated subquery to count advisories, and no such subquery exists.

This criterion fails because the implementation is a hardcoded stub, not a computed value.
