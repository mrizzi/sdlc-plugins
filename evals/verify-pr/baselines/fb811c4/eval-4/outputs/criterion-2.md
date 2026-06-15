# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (trivially, due to hardcoded stub)

## Analysis

The implementation in `modules/fundamental/src/package/service/mod.rs` hardcodes `vulnerability_count: 0` for every package:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

Because the value is hardcoded to 0 for all packages, packages with no vulnerabilities will indeed show `vulnerability_count: 0`. However, this is accidental correctness -- the value is 0 for ALL packages regardless of actual vulnerability count. The criterion's literal requirement is met, but the implementation is a stub that does not compute the real value.

The test `test_package_without_vulnerabilities_has_zero_count` asserts `assert_eq!(pkg.vulnerability_count, 0)`, which would pass with the hardcoded implementation -- but only because the hardcoded value happens to match the expected result for this specific scenario.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- The zero value is hardcoded, not computed from actual advisory data
- Test would pass incidentally, not because the logic is correct
