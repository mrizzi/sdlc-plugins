# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: FAIL

## Reasoning

While the PR does produce `vulnerability_count: 0` for all packages, this is NOT because the implementation correctly detects packages without vulnerabilities. Instead, the value is **hardcoded to 0 for every package**, regardless of whether the package has vulnerabilities or not.

In `modules/fundamental/src/package/service/mod.rs`, the implementation shows:

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

The `// TODO: implement subquery` comment explicitly confirms that the actual vulnerability counting logic has not been implemented. The task's implementation notes specify that a correlated subquery joining through `sbom_package`, `sbom_advisory`, and `advisory` tables should compute this count, but no such query exists in the diff.

While technically a package with no vulnerabilities would show 0 (since everything shows 0), the criterion's intent is that the system correctly computes the count. A hardcoded value that happens to return the right answer for the zero-vulnerability case but returns the wrong answer for every other case does not satisfy this criterion.

This criterion FAILS because the implementation is incomplete -- the vulnerability count is not dynamically computed.
