# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (trivially, due to hardcoded zero -- see note)

## Analysis

The acceptance criterion requires that packages with no vulnerabilities return `vulnerability_count: 0`.

### Evidence from PR Diff

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

The `vulnerability_count` field is hardcoded to `0` for ALL packages, not just those with no vulnerabilities. While this technically means packages with no vulnerabilities will show `vulnerability_count: 0`, this is a side effect of an incomplete implementation -- ALL packages return zero regardless of their actual vulnerability count.

### Test Evidence

The test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` asserts `vulnerability_count == 0` for a package without vulnerabilities, which would pass trivially due to the hardcoded zero.

### Conclusion

This criterion is technically satisfied in the narrow sense, but only because the implementation is incomplete. The zero value is not computed from the database -- it is a hardcoded constant. This is a vacuous pass that masks the bug identified in Criterion 3.
