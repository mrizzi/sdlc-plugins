# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (trivially, due to hardcoded zero -- see Criterion 3 for the underlying problem)

## Analysis

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows:

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

The `vulnerability_count` field is hardcoded to `0` for ALL packages. This means packages with no vulnerabilities will indeed show `vulnerability_count: 0`, so this specific criterion is technically satisfied.

However, the reason it shows zero is not because a proper query determined there are no vulnerabilities -- it is because the value is unconditionally hardcoded to 0. This is a superficial pass: the behavior is correct for zero-vulnerability packages only because the implementation returns 0 for ALL packages, including those that DO have vulnerabilities.

The test `test_package_without_vulnerabilities_has_zero_count` in `tests/api/package_vuln_count.rs` verifies this scenario and would pass (asserting `vulnerability_count == 0` for a package seeded without advisories). But this passing result is misleading because the hardcoded zero makes it impossible for ANY package to show a non-zero count.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- `vulnerability_count: 0` hardcoded
- File: `tests/api/package_vuln_count.rs` -- `test_package_without_vulnerabilities_has_zero_count` asserts zero, which would pass

## Conclusion

Technically satisfied, but only because the hardcoded zero happens to produce the correct result for this specific case. The underlying implementation is incomplete, which is captured in the FAIL verdict for Criterion 3.
