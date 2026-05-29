## Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

### Verdict: PASS (trivially, due to hardcoded value)

### Analysis

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows that `vulnerability_count` is hardcoded to `0`:

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

While packages with no vulnerabilities will indeed show `vulnerability_count: 0`, this is because **all** packages show `vulnerability_count: 0` -- the value is hardcoded rather than computed. The `// TODO: implement subquery` comment explicitly acknowledges that the actual computation is not yet implemented.

This criterion technically passes in isolation (a package with zero vulnerabilities does show 0), but the implementation is trivially correct only because the field is unconditionally set to 0. The real vulnerability counting logic is missing entirely, which directly causes Criterion 3 to fail.

### Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- The TODO comment confirms the subquery implementation is deferred, not completed.
