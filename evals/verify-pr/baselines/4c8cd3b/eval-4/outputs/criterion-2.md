# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (partial — see notes)

## Analysis

The acceptance criterion requires that packages without vulnerabilities return a `vulnerability_count` of `0`.

### Evidence from PR diff

In `modules/fundamental/src/package/service/mod.rs`, the diff shows:

```diff
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

The field is hardcoded to `0` for ALL packages, with a `// TODO: implement subquery` comment. This means packages with no vulnerabilities will correctly show `vulnerability_count: 0`, but this is only because the value is hardcoded to `0` for every package, not because a proper query was implemented.

### Test Evidence

The test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` does assert `vulnerability_count == 0` for a package with no vulnerabilities. This test would pass with the current implementation since the value is always 0.

### Conclusion

While the literal criterion ("packages with no vulnerabilities show 0") would be met by the current hardcoded implementation, this is a trivially true consequence of criterion 3 failing (all packages show 0, regardless of actual vulnerability count). The zero-count behavior is technically present but not because of correct implementation logic.
