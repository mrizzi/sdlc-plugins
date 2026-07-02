# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: FAIL (vacuously true due to hardcoding)

## Evidence

In `modules/fundamental/src/package/service/mod.rs`, the implementation hardcodes the vulnerability count:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

Every package -- regardless of whether it has vulnerabilities or not -- returns `vulnerability_count: 0`. While a package with no vulnerabilities would indeed show `0`, this is not a genuine implementation. It is a hardcoded placeholder. The TODO comment explicitly acknowledges this is incomplete.

The test `test_package_without_vulnerabilities_has_zero_count` would pass, but only because of the hardcoded value, not because the logic correctly determines there are no vulnerabilities.

## Conclusion

This criterion fails because the correct behavior (returning 0 for packages without vulnerabilities) is achieved by accident through hardcoding rather than through correct computation. The implementation does not distinguish between packages with and without vulnerabilities. Any package with actual vulnerabilities would also incorrectly return 0, demonstrating that the underlying logic is missing entirely.
