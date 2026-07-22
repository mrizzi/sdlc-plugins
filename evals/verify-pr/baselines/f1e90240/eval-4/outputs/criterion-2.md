# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (trivially, due to hardcoded value -- see caveats)

## Analysis

The service layer in `modules/fundamental/src/package/service/mod.rs` maps all packages with `vulnerability_count: 0`:

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

This means ALL packages -- regardless of whether they have vulnerabilities or not -- will return `vulnerability_count: 0`. For packages that genuinely have no vulnerabilities, the displayed value is correct. However, this is a trivial pass because the value is hardcoded to 0 for every package, not computed from actual data.

A test exists for the zero case (`test_package_without_vulnerabilities_has_zero_count`) which would pass at runtime since the value is always 0.

## Evidence

- **File:** `modules/fundamental/src/package/service/mod.rs`
- **Behavior:** All packages return `vulnerability_count: 0` due to hardcoded value
- **Test:** `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` asserts `vulnerability_count == 0` -- would pass
- **Caveat:** The criterion is technically met, but only because the value is hardcoded, not because the implementation correctly computes zero for packages without vulnerabilities

## Conclusion

This criterion passes in a narrow, literal sense: packages with no vulnerabilities do show `vulnerability_count: 0`. However, this is a side effect of the incomplete implementation (all packages show 0), not a result of correct computation. The underlying implementation is fundamentally incomplete, as noted in Criterion 3.
