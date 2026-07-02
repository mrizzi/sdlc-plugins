# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

## Verdict: PASS (incidental)

## Analysis

In `modules/fundamental/src/package/service/mod.rs`, the `vulnerability_count` field is hardcoded to `0` for all packages:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

Because the value is hardcoded to 0, packages with no vulnerabilities will indeed show `vulnerability_count: 0`. However, this is satisfied incidentally rather than by correct implementation -- the value is 0 for ALL packages, regardless of whether they have vulnerabilities or not. The hardcoded zero is not a correct implementation of vulnerability counting; it just happens to produce the right result for the zero-vulnerability case.

The test `test_package_without_vulnerabilities_has_zero_count` would pass by coincidence (hardcoded 0 matches expected 0), but the test `test_package_with_vulnerabilities_has_count` (expecting 3) would fail because the value is always 0.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- The criterion is technically satisfied for the zero-vulnerability case, but only because all values are hardcoded to 0.
