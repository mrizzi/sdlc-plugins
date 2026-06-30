# Criterion 2: Packages with no vulnerabilities show vulnerability_count: 0

## Criterion Text
Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (vacuously, due to hardcoded value -- see Criterion 3 for the deeper issue)

## Reasoning

The service layer in `modules/fundamental/src/package/service/mod.rs` sets `vulnerability_count: 0` for ALL packages via a hardcoded value:

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

While packages with no vulnerabilities will indeed show `vulnerability_count: 0`, this is only because ALL packages show 0 regardless of their actual vulnerability count. The value is hardcoded rather than computed. This criterion technically passes in a trivial sense (zero-vulnerability packages do get 0), but the underlying implementation is incomplete. The real impact of the hardcoded value is captured in Criterion 3, which explicitly fails.

Additionally, there is a test (`test_package_without_vulnerabilities_has_zero_count`) that asserts `pkg.vulnerability_count` equals 0 for a package seeded without advisories. This test would pass given the hardcoded value, though it would not catch the bug since the hardcoded value coincidentally matches the expected result for this case.

## Evidence
- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- Test: `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs`
